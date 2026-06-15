import requests
from config import CISCO_CLIENT_ID, CISCO_CLIENT_SECRET

TOKEN_URL = "https://id.cisco.com/oauth2/default/v1/token"
BASE_URL = "https://apix.cisco.com/security/advisories/v2"

PRODUCT_ENDPOINTS = {
    "ios": "OSType/ios",
    "iosxe": "OSType/iosxe",
    "nxos": "OSType/nxos",
    "asa": "OSType/asa",
    "ftd": "OSType/ftd",
}


def get_access_token():
    if not CISCO_CLIENT_ID or not CISCO_CLIENT_SECRET:
        raise ValueError("Cisco Client ID 또는 Secret이 비어 있습니다.")

    data = {
        "grant_type": "client_credentials",
        "client_id": CISCO_CLIENT_ID,
        "client_secret": CISCO_CLIENT_SECRET,
    }

    response = requests.post(TOKEN_URL, data=data, timeout=20)

    if response.status_code != 200:
        raise RuntimeError(f"토큰 발급 실패: {response.status_code} / {response.text}")

    token = response.json().get("access_token")

    print("TOKEN OK:", token[:20] + "...")

    return token


def search_advisories(product_type, version):
    token = get_access_token()

    endpoint = PRODUCT_ENDPOINTS.get(product_type)

    if not endpoint:
        raise ValueError("지원하지 않는 Cisco 제품군입니다.")

    url = f"{BASE_URL}/{endpoint}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }
    params = {
        "version": version
    }
    print("REQUEST URL:", requests.Request("GET", url, params=params).prepare().url)
    
    response = requests.get(url, headers=headers, params=params, timeout=30)

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.text)

    if response.status_code != 200:
        raise RuntimeError(f"API 조회 실패: {response.status_code} / {response.text}")

    data = response.json()
    return data.get("advisories", [])