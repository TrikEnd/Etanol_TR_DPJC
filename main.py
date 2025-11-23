"""
File MAIN PROGRAM
Dikerjakan oleh Anggota 3

Fungsi:
- Menampilkan menu utama
- Menangani input user
- Memanggil fungsi CRUD dari vlan_manager.py
- Mengatur koneksi NX-API
"""

from api_client import setup_connection, cli_show, cli_conf
import vlan_manager


# ==========================================================
#  MENU TAMPILAN
# ==========================================================

def show_main_menu():
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
    print("""
----------- READ VLAN MENU -----------
1. Tampilkan semua VLAN
2. Cari VLAN (ID/Nama)
3. Hitung total VLAN
4. Kembali ke menu utama
--------------------------------------
""")


# ==========================================================
#  MENU OPERASI
# ==========================================================

def menu_read():
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
            return
        else:
            print("[ERROR] Pilihan tidak valid!")


def menu_create():
    print("\n=== CREATE VLAN ===")
    vid = input("Masukkan VLAN ID   : ")
    name = input("Masukkan VLAN Name : ")
    vlan_manager.create_vlan(vid, name)


def menu_update():
    print("\n=== UPDATE VLAN ===")
    vid = input("Masukkan VLAN ID        : ")
    name = input("Masukkan Nama VLAN Baru : ")
    vlan_manager.update_vlan(vid, name)


def menu_delete():
    print("\n=== DELETE VLAN ===")
    name = input("Masukkan Nama VLAN yang ingin dihapus: ")

    confirm = input(f"Yakin menghapus VLAN '{name}'? (y/n): ")
    if confirm.lower() == "y":
        vlan_manager.delete_vlan(name)
    else:
        print("[INFO] Penghapusan dibatalkan.")


# ==========================================================
#  PROGRAM UTAMA
# ==========================================================

def main():
    print("=== CONFIGURE NX-API CONNECTION ===")
    base_url = input("https://sbx-nxos-mgmt.cisco.com ")
    username = input("admin")
    password = input("Admin_1234!")

    setup_connection(base_url, username, password)

    print("\n[INFO] Koneksi NX-API telah disiapkan.\n")

    while True:
        show_main_menu()
        choice = input("Pilih menu: ")

        if choice == "1":
            menu_read()
        elif choice == "2":
            menu_create()
        elif choice == "3":
            menu_update()
        elif choice == "4":
            menu_delete()
        elif choice == "5":
            print("Keluar dari program...")
            break
        else:
            print("[ERROR] Pilihan tidak valid!")


if __name__ == "__main__":
    main()
