# utils.py

import sys
import vlan_manager
import api_client

# ==========================================================
#  MENU TAMPILAN
# ==========================================================

def show_main_menu():
    """Menampilkan menu utama aplikasi."""
    print("""
===================================================
            CISCO VLAN MANAGEMENT CLI
===================================================
1. READ  VLAN
2. CREATE VLAN
3. UPDATE VLAN
4. DELETE VLAN
5. EXIT
===================================================
""")

def show_read_menu():
    """Menampilkan sub-menu untuk operasi READ."""
    print("""
----------- READ VLAN MENU -----------
1. Tampilkan semua VLAN
2. Cari VLAN (ID/Nama)
3. Hitung total VLAN
4. Kembali ke menu utama
--------------------------------------
""")

# ==========================================================
#  MENU OPERASI (LOGIC)
# ==========================================================

def menu_read(api):
    """
    Menangani navigasi sub-menu READ.
    Parameter 'api' disiapkan jika vlan_manager membutuhkan akses langsung ke client,
    meskipun saat ini vlan_manager mengimport api_client secara internal.
    """
    while True:
        show_read_menu()
        choice = input("Pilih menu READ: ")

        if choice == "1":
            vlan_manager.get_all_vlans()
        elif choice == "2":
            key = input("Masukkan ID atau Nama VLAN: ")
            vlan_manager.search_vlan(key)
        elif choice == "3":
            vlan_manager.count_vlans()
        elif choice == "4":
            print("Kembali ke menu utama...")
            break
        else:
            print("[ERROR] Pilihan tidak valid!")

def menu_create(api):
    """Menangani input user untuk membuat VLAN baru."""
    print("\n=== CREATE VLAN ===")
    try:
        vid = input("Masukkan VLAN ID   : ")
        name = input("Masukkan VLAN Name : ")
        
        if not vid.isdigit():
            print("[ERROR] VLAN ID harus berupa angka.")
            return

        vlan_manager.create_vlan(vid, name)
    except Exception as e:
        print(f"[ERROR] Terjadi kesalahan input: {e}")

def menu_update(api):
    """Menangani input user untuk memperbarui Nama VLAN."""
    print("\n=== UPDATE VLAN ===")
    try:
        vid = input("Masukkan VLAN ID yang akan diedit : ")
        name = input("Masukkan Nama VLAN Baru           : ")
        
        vlan_manager.update_vlan(vid, name)
    except Exception as e:
        print(f"[ERROR] Terjadi kesalahan: {e}")

def menu_delete(api):
    """Menangani input user untuk menghapus VLAN."""
    print("\n=== DELETE VLAN ===")
    name = input("Masukkan Nama VLAN yang ingin dihapus: ")

    if not name:
        print("[ERROR] Nama VLAN tidak boleh kosong.")
        return

    confirm = input(f"Yakin menghapus VLAN '{name}'? (y/n): ")
    if confirm.lower() == "y":
        vlan_manager.delete_vlan(name)
    else:
        print("[INFO] Penghapusan dibatalkan.")

# ==========================================================
#  PROGRAM UTAMA
# ==========================================================

def main():
    """Fungsi utama yang mengatur koneksi dan loop aplikasi."""
    print("=== CONFIGURE NX-API CONNECTION ===")
    
    # Default value agar testing lebih cepat (opsional)
    default_url = "https://sandbox-nxos-1.cisco.com/ins"
    
    base_url = input(f"Enter NX-API URL (Enter untuk default: {default_url}): ") or default_url
    username = input("Username (default: admin): ") or "admin"
    password = input("Password (default: Admin_1234!): ") or "Admin_1234!"

    # Setup koneksi di api_client
    api_client.setup_connection(base_url, username, password)
    
    # Kita bisa menganggap modul api_client sebagai objek 'api' yang diteruskan
    api = api_client

    print("\n[INFO] Koneksi NX-API telah disiapkan.\n")

    while True:
        show_main_menu()
        choice = input("Pilih menu: ")

        if choice == "1":
            menu_read(api)
        elif choice == "2":
            menu_create(api)
        elif choice == "3":
            menu_update(api)
        elif choice == "4":
            menu_delete(api)
        elif choice == "5":
            print("Keluar dari program...")
            sys.exit()
        else:
            print("[ERROR] Pilihan tidak valid!")

if __name__ == "__main__":
    main()