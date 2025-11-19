#vlan_manager

from api_client import cli_show, cli_conf

# ==========================================================
#  HELPER FUNCTION (Internal)
# ==========================================================

def _print_vlan_table(vlan_data):
    """
    Fungsi internal untuk mencetak tabel VLAN dengan format rapi.
    Menerima 'data' yang bisa berupa list atau dict (jika hanya 1 VLAN)
    """
    print("\n--- HASIL ---")
    print(f"{'ID':<5} {'NAMA':<20} {'STATUS':<10} {'PORTS'}")
    print("-" * 50)

    if not vlan_data:
        print("Tidak ada data VLAN yang ditemukan.")
        return

    if isinstance(vlan_data, dict):
        vlan_list = [vlan_data]
    else:
        vlan_list = vlan_data

    for vlan in vlan_list:
        vid = vlan.get('vlanshowbr-vlanid', 'N/A')
        name = vlan.get('vlanshowbr-vlanname', 'N/A')
        status = vlan.get('vlanshowbr-vlanstate', 'N/A')
        ports = vlan.get('vlanshowbr-vlanports', '')

        print(f"{vid:<5} {name:<20} {status:<10} {ports}")
    print("-" * 50)


# ==========================================================
#  FUNGSI READ (Dipanggil oleh menu_read)
# ==========================================================

def get_all_vlans():
    """
    Mengambil semua data VLAN menggunakan 'show vlan brief'
    """
    print("[INFO] Mengambil data 'show vlan brief' dari switch...")
    result = cli_show("show vlan brief")

    if result:
        try:
            data = result["ins_api"]["outputs"]["output"]["body"]["TABLE_vlanbrief"]["ROW_vlanbrief"]
            _print_vlan_table(data)
        except KeyError:
            print("[ERROR] Gagal parsing data. Mungkin tidak ada VLAN?")
        except Exception as e:
            print(f"[ERROR] Terjadi kesalahan: {e}")
    else:
        print("[ERROR] Gagal mengambil data VLAN dari API.")


def search_vlan(key):
    """
    Mencari VLAN berdasarkan ID atau Nama.
    Fungsi ini tetap mengambil 'show vlan brief' lalu memfilternya
    secara lokal.
    """
    print(f"[INFO] Mencari VLAN dengan ID atau Nama: {key}...")
    result = cli_show("show vlan brief")

    if result:
        try:
            data = result["ins_api"]["outputs"]["output"]["body"]["TABLE_vlanbrief"]["ROW_vlanbrief"]

            if isinstance(data, dict):
                vlan_list = [data]
            else:
                vlan_list = data

            found_vlans = []
            for vlan in vlan_list:
                vid = vlan.get('vlanshowbr-vlanid')
                name = vlan.get('vlanshowbr-vlanname')

                if key == vid or key.lower() == name.lower():
                    found_vlans.append(vlan)

            if found_vlans:
                _print_vlan_table(found_vlans)
            else:
                print(f"[INFO] VLAN '{key}' tidak ditemukan.")

        except KeyError:
            print("[ERROR] Gagal parsing data.")
    else:
        print("[ERROR] Gagal mengambil data VLAN dari API.")


def count_vlans():
    """
    Menghitung total VLAN yang ada dari 'show vlan brief'
    """
    print("[INFO] Menghitung total VLAN...")
    result = cli_show("show vlan brief")
    count = 0

    if result:
        try:
            data = result["ins_api"]["outputs"]["output"]["body"]["TABLE_vlanbrief"]["ROW_vlanbrief"]
            
            if isinstance(data, dict):
                count = 1
            elif isinstance(data, list):
                count = len(data)
            
            print(f"\n[INFO] Total VLAN yang dikonfigurasi: {count}")

        except KeyError:
            print("[INFO] Tidak ada VLAN yang terkonfigurasi (selain default).")
            print("\n[INFO] Total VLAN yang dikonfigurasi: 0")
    else:
        print("[ERROR] Gagal mengambil data VLAN dari API.")


# ==========================================================
#  FUNGSI CREATE, UPDATE, DELETE (Dipanggil main.py)
# ==========================================================

def create_vlan(vid, name):
    """
    Membuat VLAN baru.
    """
    cmd = f"vlan {vid} ; name {name}"
    print(f"[INFO] Mengirim perintah: '{cmd}'")
    
    result = cli_conf(cmd)
    
    if result:
        print(f"[SUCCESS] VLAN {vid} - {name} berhasil dibuat.")
    else:
        print("[ERROR] Gagal membuat VLAN. (Mungkin ID sudah ada?)")


def update_vlan(vid, new_name):
    """
    Mengubah nama VLAN yang sudah ada.
    Perintahnya sama dengan 'create_vlan'.
    """
    cmd = f"vlan {vid} ; name {new_name}"
    print(f"[INFO] Mengirim perintah: '{cmd}'")
    
    result = cli_conf(cmd)
    
    if result:
        print(f"[SUCCESS] VLAN {vid} berhasil di-update menjadi '{new_name}'.")
    else:
        print("[ERROR] Gagal update VLAN. (Mungkin ID tidak ada?)")


def delete_vlan(vid):
    """
    Menghapus VLAN berdasarkan ID-nya.
    Catatan: main.py mengirim 'name' tapi isinya adalah ID.
    """
    cmd = f"no vlan {vid}"
    print(f"[INFO] Mengirim perintah: '{cmd}'")
    
    result = cli_conf(cmd)
    
    if result:
        print(f"[SUCCESS] VLAN {vid} berhasil dihapus.")
    else:
        print("[ERROR] Gagal menghapus VLAN. (Pastikan ID benar)")