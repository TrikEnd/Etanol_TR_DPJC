# api_client.py
"""
File NX-API Client
Dikerjakan oleh Anggota 1

Fungsi:
- Setup koneksi ke NX-API
- Mengirim request (cli_show & cli_conf)
- Menangani error
"""

import requests
import json

# Disable SSL warnings (sandbox uses self-signed certificate)
requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.InsecureRequestWarning
)

# Global connection variables
API_URL = None
USERNAME = None
PASSWORD = None
HEADERS = {"Content-Type": "application/json"}


def setup_connection(base_url, username, password):
    """
    Menyimpan URL dan kredensial untuk koneksi NX-API.
    Dipanggil sekali dari main.py
    """
    global API_URL, USERNAME, PASSWORD
    API_URL = base_url
    USERNAME = username
    PASSWORD = password

    print("[INFO] NX-API connection configured:")
    print("      URL      :", API_URL)
    print("      USERNAME :", USERNAME)


def send_request(payload):
    """
    Fungsi inti untuk mengirim POST request ke NX-API.

    Jika gagal, akan menampilkan error dan mengembalikan None.
    """
    try:
        response = requests.post(
            API_URL,
            data=json.dumps(payload),
            headers=HEADERS,
            auth=(USERNAME, PASSWORD),
            verify=False,   # penting untuk sandbox
            timeout=10
        )

        # Raise error jika status code bukan 200
        response.raise_for_status()

        # Kembalikan JSON hasil API
        return response.json()

    except requests.exceptions.Timeout:
        print("[ERROR] Request timeout. Pastikan koneksi internet stabil.")
    except requests.exceptions.ConnectionError:
        print("[ERROR] Gagal terhubung ke NX-API. Periksa URL atau internet.")
    except Exception as e:
        print(f"[ERROR] Request failed: {str(e)}")

    return None


def cli_show(command):
    """
    Wrapper untuk perintah CLI SHOW (READ)
    Contoh:
        cli_show("show vlan brief")
    """
    payload = {
        "ins_api": {
            "version": "1.0",
            "type": "cli_show",
            "chunk": "0",
            "sid": "1",
            "input": command,
            "output_format": "json"
        }
    }
    return send_request(payload)


def cli_conf(command):
    """
    Wrapper untuk perintah CONFIG (CREATE, UPDATE, DELETE)
    Contoh:
        cli_conf("vlan 10 ; name SALES")
    """
    payload = {
        "ins_api": {
            "version": "1.0",
            "type": "cli_conf",
            "chunk": "0",
            "sid": "1",
            "input": command,
            "output_format": "json"
        }
    }
    return send_request(payload)


# ==========================================================
#  TEST KONEKSI — bisa langsung dijalankan file ini sendiri
# ==========================================================
if __name__ == "__main__":
    print("\n=== TEST NX-API CONNECTION ===")

    setup_connection(
        base_url="https://sandbox-nxos-1.cisco.com/ins",
        username="admin",
        password="Admin_1234!"
    )

    print("\n[TEST] Mengirim perintah 'show hostname'...")

    result = cli_show("show vlan brief")

    if result:
        try:
            hostname = result["ins_api"]["outputs"]["output"]["body"]["hostname"]
            print("[SUCCESS] Berhasil connect ke NX-API!")
            print("Hostname Switch :", hostname)
        except:
            print("[INFO] Respons diterima tetapi struktur tidak lengkap.")
            print(result)
    else:
        print("[FAILED] Tidak dapat konek ke NX-API.")
