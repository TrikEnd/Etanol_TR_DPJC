# vlan_manager.py
"""
File VLAN MANAGER (CRUD Logic)
Dikerjakan oleh Anggota 2 (Anda)

Fungsi:
- parse_vlan_response(response) : Memproses hasil 'show vlan brief'
- get_all_vlans()
- search_vlan(keyword)
- count_vlans()
- create_vlan(vlan_id, vlan_name)
- update_vlan(vlan_id, vlan_name)
- delete_vlan(vlan_name)
"""

import api_client
import sys
# Import utils jika Anda ingin menggunakan validasi input dan fungsi tampilan (Opsional)
# import utils 

# ==========================================================
#  HELPER: PARSING RESPONS NX-API
# ==========================================================

def parse_vlan_response(response):
    """
    Memproses respons JSON dari cli_show("show vlan brief").
    
    Menangani berbagai struktur respons: 'none' (kosong), dict (satu VLAN), 
    atau list of dicts (banyak VLAN).
    """
    vlan_list = []
    
    # Navigasi ke bagian 'body' tempat data VLAN berada
    try:
        output_body = response["ins_api"]["outputs"]["output"]["body"]
        vlan_data = output_body.get("TABLE_vlanbriefid", {}).get("ROW_vlanbriefid")
        
    except (TypeError, KeyError):
        print("[ERROR] Struktur respons API tidak terduga atau koneksi gagal.")
        return vlan_list # Mengembalikan list kosong jika ada error

    # 1. Kasus Kosong ('none')
    if vlan_data is None:
        return vlan_list

    # 2. Kasus Tunggal (dict)
    # Jika hanya ada satu VLAN, NX-API mengembalikan dict, bukan list of dicts
    if isinstance(vlan_data, dict):
        # Pastikan VLAN ID bukan '1' (default VLAN) atau VLAN khusus lainnya (1002-1005)
        # Jika Anda ingin menampilkan SEMUA, hilangkan pengecekan ini
        if vlan_data.get('vlan_id') not in ['1', '1002', '1003', '1004', '1005']:
            vlan_list.append(vlan_data)
        
    # 3. Kasus Banyak (list of dicts)
    elif isinstance(vlan_data, list):
        for vlan in vlan_data:
            # Filter VLAN ID 1 dan VLAN khusus lainnya (Opsional)
            if vlan.get('vlan_id') not in ['1', '1002', '1003', '1004', '1005']:
                vlan_list.append(vlan)

    return vlan_list

def display_vlans(vlan_list):
    """Helper untuk menampilkan daftar VLAN dalam format tabel."""
    if not vlan_list:
        print("\n[INFO] Tidak ada VLAN yang terkonfigurasi (selain default).")
        return

    print("\n---------------------------------------------------")
    print(" VLAN ID | Name                 | Status  ")
    print("---------------------------------------------------")
    for vlan in vlan_list:
        vlan_id = vlan.get('vlan_id', 'N/A').ljust(7)
        name = vlan.get('vlanname', 'N/A').ljust(20)
        status = vlan.get('state', 'N/A').ljust(7)
        print(f" {vlan_id} | {name} | {status} ")
    print("---------------------------------------------------\n")


# ==========================================================
#  OPERASI READ (R)
# ==========================================================

def get_all_vlans():
    """
    Mengambil dan menampilkan semua VLAN yang ada.
    """
    print("\n[*] Mengambil semua data VLAN...")
    response = api_client.cli_show("show vlan brief")

    if response is None:
        return # Error sudah ditangani di api_client

    vlans = parse_vlan_response(response)
    
    display_vlans(vlans)
    
    count_vlans(vlans=vlans, show_total_only=False) # Tampilkan juga totalnya

def search_vlan(keyword):
    """
    Mencari dan menampilkan VLAN berdasarkan ID atau Nama (keyword).
    """
    keyword = str(keyword).strip().lower()
    if not keyword:
        print("[ERROR] Keyword pencarian tidak boleh kosong.")
        return

    print(f"\n[*] Mencari VLAN dengan keyword '{keyword}'...")
    response = api_client.cli_show("show vlan brief")
    
    if response is None:
        return

    all_vlans = parse_vlan_response(response)
    
    # Logika Pencarian
    found_vlans = []
    for vlan in all_vlans:
        # Mencocokkan ID (jika keyword adalah angka) atau Nama
        vlan_id = vlan.get('vlan_id', '').lower()
        vlan_name = vlan.get('vlanname', '').lower()
        
        if keyword in vlan_id or keyword in vlan_name:
            found_vlans.append(vlan)
    
    if found_vlans:
        print(f"[INFO] Ditemukan {len(found_vlans)} VLAN yang cocok:")
        display_vlans(found_vlans)
    else:
        print(f"[INFO] Tidak ada VLAN yang ditemukan untuk keyword '{keyword}'.")

def count_vlans(vlans=None, show_total_only=True):
    """
    Menghitung dan menampilkan jumlah total VLAN yang dikonfigurasi.
    """
    if vlans is None:
        response = api_client.cli_show("show vlan brief")
        if response is None:
            return
        vlans = parse_vlan_response(response)
        
    total = len(vlans)
    
    if show_total_only:
        print(f"\n[INFO] Total VLAN yang dikonfigurasi (selain default): {total}\n")
    else:
         print(f"[INFO] Total VLAN ditampilkan: {total}")

# ==========================================================
#  OPERASI CREATE/UPDATE/DELETE (CUD)
# ==========================================================

def create_vlan(vlan_id, vlan_name):
    """
    Membuat VLAN baru. Jika VLAN sudah ada, perintah ini akan memperbarui namanya.
    """
    # Anda dapat menambahkan validasi dari utils.py di sini (Opsional)
    # is_valid, vid = utils.validate_vlan_id(vlan_id)
    # if not is_valid or not utils.validate_vlan_name(vlan_name):
    #     return

    # Perintah NX-OS menggunakan 'cli_conf'
    cli_command = f"configure terminal ; vlan {vlan_id} ; name {vlan_name} ; end"
    
    print(f"[*] Mengirim perintah: Membuat/Memperbarui VLAN ID {vlan_id} ({vlan_name})...")
    response = api_client.cli_conf(cli_command)

    if response is None:
        return # Error sudah ditangani di api_client
    
    # Cek sukses/gagal dari respons API (Contoh pengecekan sederhana)
# Cek sukses/gagal dari respons API (Gunakan cara yang lebih robust)
    try:
        # Dapatkan data 'output' utama
        output_data = response["ins_api"]["outputs"]["output"]
        
        # Jika output_data adalah List, ambil elemen pertama sebagai Dict utama
        if isinstance(output_data, list):
            output = output_data[0]
        else:
            output = output_data

        # Sekarang kita menggunakan .get() yang aman karena kita tahu 'output' adalah dict
        status_code = output.get("code")
        
        if status_code == '200':
            print(f"✅ SUKSES! VLAN ID {vlan_id} berhasil dibuat/diperbarui.")
        else:
            print(f"❌ GAGAL! Perangkat mengembalikan kode status {status_code}.")
            # Tampilkan pesan error detail dari 'msg' atau 'body'
            error_msg = output.get("msg") or output.get("body", "Tidak ada pesan detail.")
            print(f"   Pesan Perangkat: {error_msg}")
            
    except (TypeError, KeyError, IndexError) as e:
        # Tangani error jika struktur JSON benar-benar tidak terduga
        print(f"❌ GAGAL TOTAL! Struktur respons API tidak terduga.")
        print(f"   Detail Error Python: {e}")

def update_vlan(vlan_id, vlan_name):
    """
    Memperbarui nama VLAN yang sudah ada. Menggunakan fungsi yang sama dengan create.
    """
    # Karena NX-OS menggunakan perintah yang sama (vlan <id> ; name <new_name>)
    # untuk membuat atau memperbarui nama, kita bisa panggil fungsi create_vlan.
    print(f"\n[INFO] Memperbarui VLAN ID {vlan_id}. Ini akan menggunakan fungsi Create/Update.")
    create_vlan(vlan_id, vlan_name)


def delete_vlan(vlan_name):
    """
    Menghapus VLAN berdasarkan namanya.
    """
    # Anda dapat menambahkan validasi dari utils.py di sini (Opsional)
    # if not utils.validate_vlan_name(vlan_name):
    #     return

    # Perintah NX-OS menggunakan 'no vlan <vlan_name>'
    # Catatan: Beberapa perangkat NX-OS membutuhkan ID, tetapi nama lebih user-friendly. 
    # Kita asumsikan perangkat dapat memproses 'no vlan <name>' jika nama itu unik.
    # Jika tidak, Anda harus mencari ID VLAN terlebih dahulu.
    
    cli_command = f"configure terminal ; no vlan {vlan_name} ; end"
    
    print(f"[*] Mengirim perintah: Menghapus VLAN '{vlan_name}'...")
    response = api_client.cli_conf(cli_command)

    if response is None:
        return
    
    # Cek sukses/gagal dari respons API
    try:
        status_code = response["ins_api"]["outputs"]["output"]["code"]
        if status_code == '200':
            print(f"✅ SUKSES! VLAN '{vlan_name}' berhasil dihapus.")
        else:
            print(f"❌ GAGAL! Perangkat mengembalikan kode status {status_code}.")
            error_msg = response["ins_api"]["outputs"]["output"].get("msg")
            print(f"   Pesan Perangkat: {error_msg}")
    except (TypeError, KeyError):
        print("❌ GAGAL! Struktur respons tidak lengkap.")