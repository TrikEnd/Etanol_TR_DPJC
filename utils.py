import vlan_manager

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
4. Kembali
--------------------------------------
""")


def menu_read():
    while True:
        show_read_menu()
        c = input("Pilih menu READ: ")

        if c == "1":
            vlan_manager.get_all_vlans()
        elif c == "2":
            keyword = input("Masukkan ID/Nama VLAN: ")
            vlan_manager.search_vlan(keyword)
        elif c == "3":
            vlan_manager.count_vlans()
        elif c == "4":
            break
        else:
            print("[ERROR] Pilihan salah.")


def menu_create():
    vid = input("Masukkan VLAN ID: ")
    name = input("Masukkan VLAN Name: ")
    vlan_manager.create_vlan(vid, name)


def menu_update():
    vid = input("Masukkan VLAN ID: ")
    name = input("Nama baru: ")
    vlan_manager.update_vlan(vid, name)


def menu_delete():
    name = input("Masukkan Nama VLAN yang ingin dihapus: ")
    y = input(f"Yakin hapus VLAN `{name}`? (y/n): ")
    if y.lower() == "y":
        vlan_manager.delete_vlan(name)
