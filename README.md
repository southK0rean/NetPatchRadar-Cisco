# NetPatchRadar Cisco

Cisco Software Vulnerability Assessment Tool powered by Cisco OpenVuln API.

NetPatchRadar Cisco helps network engineers quickly identify software vulnerabilities, review risk levels, and generate security assessment reports for Cisco platforms.

---

## Prerequisites

A Cisco Developer account is required to obtain OpenVuln API credentials.

Register and request API access through the Cisco Developer Portal.

Cisco Developer Portal: https://developer.cisco.com

## Features

- Cisco OpenVuln API Integration
- CVSS-Based Vulnerability Ranking
- Severity Dashboard
- Upgrade Recommendation Engine
- PDF Security Report Export

---

## Supported Products

- Cisco IOS XE
- Cisco IOS
- Cisco NX-OS
- Cisco ASA
- Cisco FTD

---

## Screenshots

### Dashboard

![Dashboard](screenshots/dashboard.png)
![Dashboard](screenshots/dashboard1.png)

### PDF Report

![PDF Report](screenshots/pdf-report.png)

---

## Installation

```bash
git clone https://github.com/southK0rean/NetPatchRadar-Cisco.git

cd NetPatchRadar-Cisco

pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root directory.

```env
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret
```

Cisco API credentials can be obtained from the Cisco Developer Portal.

---

## Run

```bash
python app.py
```

Open your browser and navigate to:

```text
http://127.0.0.1:5000
```

---

## Example Workflow

1. Select Cisco product type
2. Enter software version
3. Run vulnerability assessment
4. Review Severity Dashboard
5. Review recommended upgrade version
6. Export PDF security report

---

## Sample Output

- Vulnerability Summary
- Critical / High / Medium / Low Counts
- Recommended Upgrade Version
- Top Vulnerabilities by CVSS
- PDF Executive Summary Report

---

## Roadmap

### v1.0

- Cisco OpenVuln Integration
- PDF Report Export
- Upgrade Recommendation

### Future Plans

- Cisco EoX / Lifecycle Integration
- Suggested Release Analysis
- Configuration Parsing
- "show version" Auto Detection
- Multi-Vendor Support

---

## Disclaimer

This project is an independent tool and is not affiliated with Cisco Systems.

Cisco trademarks and product names belong to Cisco Systems, Inc.