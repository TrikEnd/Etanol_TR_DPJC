"""
MAIN PROGRAM
Bagian: Anggota 3
(Tidak mengubah file teman)

Program ini:
- Menghubungkan ke NX-API (pakai api_client.py)
- Menjalankan CRUD VLAN langsung dari main.py
"""

from api_client import setup_connection, cli_show, cli_conf


# ==========================================================
#  FUNCTIONS (CRUD langsung di main)
# ==========================================================

def show_all_vlans():
    print("\n=== DAFTAR VLAN ===")
    response = cli_show("show vlan brief")

    if not response:
        print("[ERROR] Tidak dapat mengambil data VLAN.")
        return

    body = response["ins_api"]["outputs"]["output"]["body"]

    # Cek 2 kemungkinan struktur DevNet:
    table = (
        body.get("TABLE_vlanbrief", {}).get("ROW_vlanbrief") or
        body.get("TABLE_vlanbriefxbrief", {}).get("ROW_vlanbriefxbrief")
    )

    if not table:
        print("[INFO] Tidak ada VLAN.")
        return

    if isinstance(table, dict):
        table = [table]

    for v in table:
        print(f"ID: {v.get('vlanshowbr-vlanid')}  "
              f"Nama: {v.get('vlanshowbr-vlanname')}  "
              f"Status: {v.get('vlanshowbr-shutstate')}")


def search_vlan():
    keyword = input("Masukkan ID atau Nama VLAN: ").lower()
    
    response = cli_show("show vlan brief")
    if not response:
        print("[ERROR] Tidak dapat mengambil data VLAN.")
        return

    body = response["ins_api"]["outputs"]["output"]["body"]
    table = (
        body.get("TABLE_vlanbrief", {}).get("ROW_vlanbrief") or
        body.get("TABLE_vlanbriefxbrief", {}).get("ROW_vlanbriefxbrief")
    )

    if not table:
        print("[INFO] Tidak ada VLAN.")
        return

    if isinstance(table, dict):
        table = [table]

    print("\n=== HASIL PENCARIAN ===")
    found = False
    for v in table:
        if v.get("vlanshowbr-vlanid") == keyword or v.get("vlanshowbr-vlanname").lower() == keyword:
            print(f"ID: {v['vlanshowbr-vlanid']}  Nama: {v['vlanshowbr-vlanname']}")
            found = True

    if not found:
        print("[INFO] VLAN tidak ditemukan.")


def count_vlans():
    response = cli_show("show vlan brief")
    if not response:
        print("[ERROR] Tidak dapat mengambil data VLAN.")
        return

    body = response["ins_api"]["outputs"]["output"]["body"]
    table = (
        body.get("TABLE_vlanbrief", {}).get("ROW_vlanbrief") or
        body.get("TABLE_vlanbriefxbrief", {}).get("ROW_vlanbriefxbrief")
    )

    if not table:
        print("Total VLAN: 0")
        return

    if isinstance(table, dict):
        print("Total VLAN: 1")
    else:
        print("Total VLAN:", len(table))


def create_vlan():
    vid = input("Masukkan VLAN ID   : ")
    name = input("Masukkan VLAN Name : ")

    command = f"vlan {vid} ; name {name}"
    result = cli_conf(command)

    print("\n=== RESULT ===")
    print(result)


def update_vlan():
    vid = input("Masukkan VLAN ID yang ingin diupdate   : ")
    name = input("Masukkan Nama VLAN Baru                : ")

    command = f"vlan {vid} ; name {name}"
    result = cli_conf(command)

    print("\n=== RESULT ===")
    print(result)


def delete_vlan():
    name = input("Masukkan Nama VLAN yang ingin dihapus: ")
    confirm = input(f"Yakin hapus VLAN '{name}'? (y/n): ")

    if confirm.lower() != "y":
        print("[INFO] Dibatalkan.")
        return

    # Sesuai instruksi dosen (meskipun NX-OS asli pakai no vlan <id>)
    command = f"no vlan name {name}"
    result = cli_conf(command)

    print("\n=== RESULT ===")
    print(result)


# ==========================================================
#  MENU
# ==========================================================

def show_main_menu():
    print("""
============================
   CISCO VLAN CLI SYSTEM
============================
1. READ  VLAN
2. CREATE VLAN
3. UPDATE VLAN
4. DELETE VLAN
5. EXIT
============================
""")


def show_read_menu():
    print("""
------ READ VLAN ------
1. Tampilkan semua VLAN
2. Cari VLAN
3. Hitung total VLAN
4. Kembali
------------------------
""")


def menu_read():
    while True:
        show_read_menu()
        c = input("Pilih menu READ: ")

        if c == "1":
            show_all_vlans()
        elif c == "2":
            search_vlan()
        elif c == "3":
            count_vlans()
        elif c == "4":
            return
        else:
            print("[ERROR] Pilihan tidak valid!")


# ==========================================================
#  MAIN PROGRAM
# ==========================================================

def main():
    print("=== CONFIGURE NX-API CONNECTION ===")
    base_url = input("Masukkan URL NX-API (contoh: https://sandbox-nxos-1.cisco.com/ins): ")
    username = input("Username: ")
    password = input("Password: ")

    setup_connection(base_url, username, password)

    while True:
        show_main_menu()
        menu = input("Pilih menu: ")

        if menu == "1":
            menu_read()
        elif menu == "2":
            create_vlan()
        elif menu == "3":
            update_vlan()
        elif menu == "4":
            delete_vlan()
        elif menu == "5":
            print("Keluar...")
            break
        else:
            print("[ERROR] Pilihan tidak valid!")


if __name__ == "__main__":
    main()
