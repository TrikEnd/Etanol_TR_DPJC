import api_client

def parse_vlan_response(response):
    vlan_list = []

    try:
        output_body = response["ins_api"]["outputs"]["output"]["body"]
        vlan_data = output_body.get("TABLE_vlanbriefid", {}).get("ROW_vlanbriefid")
    except (TypeError, KeyError):
        print("[ERROR] Struktur respons API tidak terduga.")
        return vlan_list

    if vlan_data is None:
        return vlan_list

    if isinstance(vlan_data, dict):
        if vlan_data.get('vlan_id') not in ['1', '1002', '1003', '1004', '1005']:
            vlan_list.append(vlan_data)

    elif isinstance(vlan_data, list):
        for vlan in vlan_data:
            if vlan.get('vlan_id') not in ['1', '1002', '1003', '1004', '1005']:
                vlan_list.append(vlan)

    return vlan_list


def display_vlans(vlans):
    if not vlans:
        print("\n[INFO] Tidak ada VLAN yang terkonfigurasi.")
        return

    print("\n---------------------------------------------------")
    print(" VLAN ID | Name                 | Status  ")
    print("---------------------------------------------------")
    for vlan in vlans:
        vlan_id = vlan.get('vlan_id', 'N/A').ljust(7)
        name = vlan.get('vlanname', 'N/A').ljust(20)
        status = vlan.get('state', 'N/A').ljust(7)
        print(f" {vlan_id} | {name} | {status} ")
    print("---------------------------------------------------\n")


def get_all_vlans():
    print("\n[*] Mengambil semua VLAN...")
    response = api_client.cli_show("show vlan brief")

    if response is None:
        return

    vlans = parse_vlan_response(response)
    display_vlans(vlans)
    count_vlans(vlans, show_total_only=False)


def search_vlan(keyword):
    keyword = keyword.lower().strip()
    print(f"\n[*] Mencari VLAN '{keyword}'...")
    response = api_client.cli_show("show vlan brief")

    if response is None:
        return

    vlans = parse_vlan_response(response)

    found = [
        v for v in vlans
        if keyword in v.get("vlan_id", "").lower() or keyword in v.get("vlanname", "").lower()
    ]

    if found:
        display_vlans(found)
    else:
        print("[INFO] VLAN tidak ditemukan.")


def count_vlans(vlans=None, show_total_only=True):
    if vlans is None:
        response = api_client.cli_show("show vlan brief")
        if response is None:
            return
        vlans = parse_vlan_response(response)

    total = len(vlans)
    print(f"[INFO] Total VLAN: {total}")


def create_vlan(vlan_id, vlan_name):
    cmd = f"configure terminal ; vlan {vlan_id} ; name {vlan_name} ; end"

    print(f"[*] Membuat VLAN {vlan_id} ({vlan_name})...")
    response = api_client.cli_conf(cmd)

    if response is None:
        return

    try:
        output = response["ins_api"]["outputs"]["output"]
        if isinstance(output, list):
            output = output[0]

        if output.get("code") == "200":
            print(f"✅ VLAN {vlan_id} berhasil dibuat.")
        else:
            print("❌ Gagal Membuat VLAN :", output.get("msg"))

    except Exception as e:
        print(f"[ERROR] Struktur respons tidak sesuai: {e}")


def update_vlan(vlan_id, vlan_name):
    print("\n[INFO] Update VLAN menggunakan fungsi Create...")
    create_vlan(vlan_id, vlan_name)


def delete_vlan(vlan_name):
    cmd = f"configure terminal ; no vlan {vlan_name} ; end"

    print(f"[*] Menghapus VLAN {vlan_name}...")
    response = api_client.cli_conf(cmd)

    if response is None:
        return

    try:
        code = response["ins_api"]["outputs"]["output"]["code"]
        if code == "200":
            print(f"✅ VLAN {vlan_name} berhasil dihapus.")
        else:
            print("❌ Gagal :", response["ins_api"]["outputs"]["output"].get("msg"))
    except:
        print("[ERROR] Struktur respons error.")
