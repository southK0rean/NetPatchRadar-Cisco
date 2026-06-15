import re


def detect_cisco_product(show_version_text: str) -> str:
    text = show_version_text.lower()

    if "ios xe" in text or "ios-xe" in text:
        return "iosxe"
    if "nx-os" in text or "nxos" in text:
        return "nxos"
    if "adaptive security appliance" in text or "asa software" in text:
        return "asa"
    if "firepower" in text or "ftd" in text:
        return "ftd"
    if "cisco ios software" in text:
        return "ios"

    return ""


def extract_cisco_version(show_version_text: str) -> str:
    patterns = [
        r"Cisco IOS XE Software,\s*Version\s+([A-Za-z0-9()._-]+)",
        r"Cisco Adaptive Security Appliance Software Version\s+([A-Za-z0-9()._-]+)",
        r"Version\s+([0-9]+\.[0-9]+\.[0-9]+[A-Za-z]?)",
        r"NXOS:\s*version\s+([A-Za-z0-9()._-]+)",
        r"ASA Version\s+([A-Za-z0-9()._-]+)",
        r"Software Version\s+([A-Za-z0-9()._-]+)",
        r"system:\s*version\s+([A-Za-z0-9()._-]+)",
        r"kickstart:\s*version\s+([A-Za-z0-9()._-]+)",
    ]

    for pattern in patterns:
        match = re.search(pattern, show_version_text, re.IGNORECASE)
        if match:
            return match.group(1)

    return ""


def parse_show_version(show_version_text: str) -> dict:
    product = detect_cisco_product(show_version_text)
    version = extract_cisco_version(show_version_text)

    return {
        "product": product,
        "version": version,
        "detected": bool(product or version),
    }