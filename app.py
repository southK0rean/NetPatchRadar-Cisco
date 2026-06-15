from packaging import version
from collections import Counter
from flask import Flask, render_template, request, send_file
from pdf_report import generate_pdf_report
from cisco_openvuln import search_advisories
from version_parser import parse_show_version

app = Flask(__name__)

PRODUCT_TYPES = {
    "iosxe": "Cisco IOS XE",
    "ios": "Cisco IOS",
    "nxos": "Cisco NX-OS",
    "asa": "Cisco ASA",
    "ftd": "Cisco FTD",
}


def build_summary(advisories):
    summary = {
        "Critical": 0,
        "High": 0,
        "Medium": 0,
        "Low": 0,
        "Informational": 0,
        "Unknown": 0,
    }

    for adv in advisories:
        severity = adv.get("sir") or "Unknown"
        summary[severity] = summary.get(severity, 0) + 1

    return summary

def build_upgrade_recommendation(advisories):
    fixed_versions = []

    for adv in advisories:
        for fixed_version in adv.get("firstFixed", []):
            if fixed_version:
                fixed_versions.append(fixed_version)

    if not fixed_versions:
        return None

    counter = Counter(fixed_versions)

    valid_versions = []
    for fixed_version in fixed_versions:
        try:
            valid_versions.append(fixed_version)
        except Exception:
            pass

    recommended = max(
        valid_versions,
        key=lambda v: version.parse(v)
    )

    return {
        "recommended": recommended,
        "candidates": counter.most_common(5)
    }

def build_eox_info(selected_product, version):
    return {
        "status": "Not Checked",
        "message": "Cisco EoX API integration is pending. This card will show End-of-Sale and End-of-Support dates after API connection.",
        "product": PRODUCT_TYPES.get(selected_product, selected_product),
        "version": version,
        "end_of_sale": None,
        "end_of_support": None,
    }

@app.route("/", methods=["GET", "POST"])
def index():
    advisories = []
    summary = None
    error = None
    upgrade_recommendation = None
    eox_info = None

    selected_product = "iosxe"
    version = ""
    show_version_text = ""

    parser_result = {}
    input_source = None

    if request.method == "POST":
        selected_product = request.form.get("product_type", "iosxe")
        version = request.form.get("version", "").strip()
        show_version_text = request.form.get("show_version_text", "").strip()

        parser_result = {}

        if show_version_text:
           parser_result = parse_show_version(show_version_text)

           if parser_result.get("product"):
               selected_product = parser_result["product"]

           if parser_result.get("version"):
               version = parser_result["version"]
           
           input_source = "show version"
        
        else:
            input_source = "manual"

        if not version:
            error = "버전을 입력해주세요. 예: 17.9.4"
        else:
            try:
                advisories = search_advisories(selected_product, version)

                advisories = sorted(
                    advisories,
                    key=lambda x: float(x.get("cvssBaseScore") or 0),
                    reverse=True,
                )
                
                upgrade_recommendation = build_upgrade_recommendation(advisories)
                eox_info = build_eox_info(selected_product, version)
                summary = build_summary(advisories)

            except Exception as e:
                error = str(e)

    return render_template(
        "index.html",
        product_types=PRODUCT_TYPES,
        upgrade_recommendation=upgrade_recommendation,
        eox_info=eox_info,
        selected_product=selected_product,
        version=version,
        advisories=advisories,
        summary=summary,
        error=error,
        parser_result=parser_result,
        input_source=input_source,
        show_version_text=show_version_text,
    )

@app.route("/report/pdf", methods=["POST"])
def download_pdf():
    selected_product = request.form.get("product_type", "iosxe")
    version = request.form.get("version", "").strip()

    advisories = search_advisories(selected_product, version)

    advisories = sorted(
        advisories,
        key=lambda x: float(x.get("cvssBaseScore") or 0),
        reverse=True,
    )

    summary = build_summary(advisories)
    upgrade_recommendation = build_upgrade_recommendation(advisories)

    pdf_buffer = generate_pdf_report(
        PRODUCT_TYPES.get(selected_product, selected_product),
        version,
        summary,
        upgrade_recommendation,
        advisories,
    )

    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=f"netpatchradar-cisco-{selected_product}-{version}.pdf",
        mimetype="application/pdf",
    )

if __name__ == "__main__":
    app.run(debug=True)