NetPatchRadar Cisco

Cisco Software Vulnerability Assessment Tool powered by Cisco OpenVuln API.

NetPatchRadar Cisco helps network engineers quickly identify software vulnerabilities, review risk levels, and generate security assessment reports for Cisco platforms.

Features
Cisco OpenVuln API Integration
CVSS-Based Vulnerability Ranking
Severity Dashboard
Upgrade Recommendation Engine
PDF Security Report Export
Cisco Product Selection Support
Supported Products
Cisco IOS XE
Cisco IOS
Cisco NX-OS
Cisco ASA
Cisco FTD


>Dashboard
![Dashboard](screenshots/dashboard.png)
![Dashboard](screenshots/dashboard1.png)

>PDF Report
![PDF Report](screenshots/pdf-report.png)

Installation
git clone https://github.com/your-github-id/netpatchradar-cisco.git

cd netpatchradar-cisco

pip install -r requirements.txt
Environment Variables

Create a .env file in the project root directory.

CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret

Cisco API credentials can be obtained from the Cisco Developer Portal.

Run
python app.py

Then open:

http://127.0.0.1:5000
Example Workflow
Select Cisco product type
Enter software version
Run vulnerability assessment
Review Severity Dashboard
Review recommended upgrade version
Export PDF security report
Sample Output
Vulnerability Summary
Critical / High / Medium / Low Counts
Recommended Upgrade Version
Top Vulnerabilities by CVSS
PDF Executive Summary Report
Roadmap
v1.0
Cisco OpenVuln Integration
PDF Report Export
Upgrade Recommendation
Future Plans
Cisco EoX / Lifecycle Integration
Suggested Release Analysis
Configuration Parsing
"show version" Auto Detection
Multi-Vendor Support
Disclaimer

This project is an independent tool and is not affiliated with Cisco Systems.

Cisco trademarks and product names belong to Cisco Systems, Inc.