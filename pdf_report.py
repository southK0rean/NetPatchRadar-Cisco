from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from datetime import datetime

def calculate_risk_level(summary):
    critical = summary.get("Critical", 0)
    high = summary.get("High", 0)

    if critical > 0:
        return "CRITICAL"
    elif high >= 10:
        return "HIGH"
    elif high > 0:
        return "MEDIUM"
    else:
        return "LOW"

def generate_pdf_report(product_name, version, summary, upgrade_recommendation, advisories):
    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("NetPatchRadar Cisco Report", styles["Title"]))
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M")
    risk_level = calculate_risk_level(summary)

    story.append(Paragraph(f"Generated At: {generated_at}", styles["Normal"]))
    story.append(Spacer(1, 12))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Executive Summary", styles["Heading2"]))
    story.append(Paragraph(f"Product: {product_name}", styles["Normal"]))
    story.append(Paragraph(f"Version: {version}", styles["Normal"]))
    story.append(Paragraph(f"Risk Level: {risk_level}", styles["Normal"]))

    if upgrade_recommendation:
        story.append(
            Paragraph(
                f"Recommended Upgrade: {upgrade_recommendation.get('recommended')}",
                styles["Normal"]
            )
        )

    story.append(Spacer(1, 16))

    story.append(Paragraph("Severity Summary", styles["Heading2"]))

    summary_data = [
        ["Severity", "Count"],
        ["Critical", summary.get("Critical", 0)],
        ["High", summary.get("High", 0)],
        ["Medium", summary.get("Medium", 0)],
        ["Low", summary.get("Low", 0)],
    ]

    table = Table(summary_data)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(table)
    story.append(Spacer(1, 16))

    story.append(Paragraph("Upgrade Recommendation", styles["Heading2"]))

    if upgrade_recommendation:
        story.append(
            Paragraph(
                f"Recommended Version: {upgrade_recommendation.get('recommended')}",
                styles["Normal"]
            )
        )
    else:
        story.append(Paragraph("No upgrade recommendation available.", styles["Normal"]))

    story.append(Spacer(1, 16))
    story.append(Paragraph("Top 10 Vulnerabilities by CVSS", styles["Heading2"]))

    for adv in advisories[:10]:
        title = adv.get("advisoryTitle", "No title")
        advisory_id = adv.get("advisoryId", "N/A")
        cvss = adv.get("cvssBaseScore", "N/A")
        sir = adv.get("sir", "Unknown")

        story.append(Paragraph(f"<b>{sir}</b> | {advisory_id}", styles["Normal"]))
        story.append(Paragraph(title, styles["Normal"]))
        story.append(Paragraph(f"CVSS: {cvss}", styles["Normal"]))
        story.append(Spacer(1, 8))

    doc.build(story)

    buffer.seek(0)
    return buffer