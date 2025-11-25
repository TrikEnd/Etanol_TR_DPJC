from api_client import setup_connection
import utils

def main():
    print("=== CONFIGURE NX-API CONNECTION ===")

    base_url = input("Masukkan URL NX-API: ") \
              or "https://sbx-nxos-mgmt.cisco.com"
    username = input("Username (default: admin): ") or "admin"
    password = input("Password (default: Admin_1234!): ") or "Admin_1234!"

    setup_connection(base_url, username, password)

    print("\n[INFO] Koneksi NX-API telah disiapkan.\n")

    while True:
        utils.show_main_menu()
        choice = input("Pilih menu: ")

        if choice == "1":
            utils.menu_read()
        elif choice == "2":
            utils.menu_create()
        elif choice == "3":
            utils.menu_update()
        elif choice == "4":
            utils.menu_delete()
        elif choice == "5":
            print("Keluar...")
            break
        else:
            print("[ERROR] Pilihan tidak valid!")

if __name__ == "__main__":
    main()
