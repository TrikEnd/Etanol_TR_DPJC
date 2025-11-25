import requests
import json


requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.InsecureRequestWarning
)

API_URL = None
USERNAME = None
PASSWORD = None
HEADERS = {"Content-Type": "application/json"}


def setup_connection(base_url, username, password):

    global API_URL, USERNAME, PASSWORD
    API_URL = base_url.rstrip("/")  
    USERNAME = username
    PASSWORD = password

    print("[INFO] NX-API connection configured:")
    print("      BASE URL :", API_URL)
    print("      USERNAME :", USERNAME)


def send_request(payload):

    full_url = API_URL + "/ins"  

    try:
        response = requests.post(
            full_url,
            data=json.dumps(payload),
            headers=HEADERS,
            auth=(USERNAME, PASSWORD),
            verify=False,  
            timeout=10
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.Timeout:
        print("[ERROR] Request timeout. Pastikan koneksi internet stabil.")
    except requests.exceptions.ConnectionError:
        print("[ERROR] Gagal terhubung ke NX-API. Periksa URL atau internet.")
    except Exception as e:
        print(f"[ERROR] Request failed: {str(e)}")

    return None


def cli_show(command):
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


if __name__ == "__main__":
    print("\n=== TEST NX-API CONNECTION ===")

    setup_connection(
        base_url="https://sbx-nxos-mgmt.cisco.com",  
        username="admin",
        password="Admin_1234!"
    )

    print("\n[TEST] Mengirim perintah 'show vlan brief'...")

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
