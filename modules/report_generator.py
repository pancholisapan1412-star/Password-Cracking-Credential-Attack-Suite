from io import BytesIO
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from xml.sax.saxutils import escape


def generate_audit_report(records):

    # Create an in-memory PDF file
    pdf_buffer = BytesIO()

    document = SimpleDocTemplate(
        pdf_buffer,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        textColor=colors.HexColor("#17365D"),
        fontSize=20,
        spaceAfter=8
    )

    subtitle_style = ParagraphStyle(
        "ReportSubtitle",
        parent=styles["Normal"],
        alignment=TA_CENTER,
        fontSize=9,
        textColor=colors.grey
    )

    cell_style = ParagraphStyle(
        "CellStyle",
        parent=styles["Normal"],
        fontSize=8,
        leading=11
    )

    story = []

    # Report heading
    story.append(
        Paragraph("SECURITY AUDIT REPORT", title_style)
    )

    story.append(
        Paragraph(
            "Password Cracking &amp; Credential Attack Suite",
            subtitle_style
        )
    )

    story.append(Spacer(1, 10))

    # Report information
    generated_at = datetime.now().strftime(
        "%d %B %Y, %I:%M %p"
    )

    story.append(
        Paragraph(
            f"<b>Generated on:</b> {generated_at}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Total analysis records:</b> {len(records)}",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 18))

    # Table heading
    story.append(
        Paragraph("Analysis History", styles["Heading2"])
    )

    table_data = [[
        "ID",
        "Analysis Type",
        "Result",
        "Summary",
        "Date"
    ]]

    # Add database records to the table
    for record in records:

        table_data.append([
            Paragraph(escape(str(record["id"])), cell_style),
            Paragraph(
                escape(str(record["analysis_type"])),
                cell_style
            ),
            Paragraph(
                escape(str(record["result_label"])),
                cell_style
            ),
            Paragraph(
                escape(str(record["summary"])),
                cell_style
            ),
            Paragraph(
                escape(str(record["created_at"])),
                cell_style
            )
        ])

    if not records:
        table_data.append([
            Paragraph("-", cell_style),
            Paragraph("-", cell_style),
            Paragraph("-", cell_style),
            Paragraph("No analysis records available.", cell_style),
            Paragraph("-", cell_style)
        ])

    report_table = Table(
        table_data,
        colWidths=[
            12 * mm,
            27 * mm,
            25 * mm,
            75 * mm,
            32 * mm
        ],
        repeatRows=1
    )

    report_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#17365D")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [
            colors.white,
            colors.HexColor("#EAF0F6")
        ])
    ]))

    story.append(report_table)

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "<b>Note:</b> This report contains analysis metadata "
            "only. It does not contain plaintext passwords, raw "
            "hashes, or credential records.",
            styles["Italic"]
        )
    )

    # Generate PDF
    document.build(story)

    pdf_buffer.seek(0)

    return pdf_buffer