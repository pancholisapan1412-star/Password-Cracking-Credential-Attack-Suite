
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
import os
from datetime import datetime


# ==========================================
# PAGE SETTINGS
# ==========================================

PAGE_WIDTH, PAGE_HEIGHT = A4

LEFT_MARGIN = 50
RIGHT_MARGIN = PAGE_WIDTH - 50


# ==========================================
# NUMBERED CANVAS
# ==========================================

class NumberedCanvas(canvas.Canvas):

    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.pages = []

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):

        self.pages.append(dict(self.__dict__))

        total_pages = len(self.pages)

        for page_data in self.pages:

            self.__dict__.update(page_data)

            self.setFont("Helvetica", 9)
            self.setFillColor(colors.grey)

            self.drawCentredString(
                PAGE_WIDTH / 2,
                30,
                f"Page {self._pageNumber} of {total_pages}"
            )

            canvas.Canvas.showPage(self)

        canvas.Canvas.save(self)


# ==========================================
# PROFESSIONAL HEADER AND FOOTER
# ==========================================

def draw_page_design(pdf, page_title):

    # Header background
    pdf.setFillColor(colors.HexColor("#142D4E"))

    pdf.rect(
        0,
        PAGE_HEIGHT - 65,
        PAGE_WIDTH,
        65,
        fill=1,
        stroke=0
    )

    # Header title
    pdf.setFillColor(colors.white)
    pdf.setFont("Helvetica-Bold", 11)

    pdf.drawString(
        LEFT_MARGIN,
        PAGE_HEIGHT - 30,
        "PASSWORD SECURITY AUDIT"
    )

    pdf.setFont("Helvetica", 9)

    pdf.drawRightString(
        RIGHT_MARGIN,
        PAGE_HEIGHT - 30,
        page_title
    )

    # Footer separator
    pdf.setStrokeColor(colors.HexColor("#D1D5DB"))
    pdf.setLineWidth(0.7)

    pdf.line(
        LEFT_MARGIN,
        50,
        RIGHT_MARGIN,
        50
    )

    # Footer text
    pdf.setFillColor(colors.grey)
    pdf.setFont("Helvetica", 8)

    pdf.drawString(
        LEFT_MARGIN,
        35,
        "Password Cracking & Credential Attack Suite"
    )

    pdf.drawRightString(
        RIGHT_MARGIN,
        35,
        datetime.now().strftime("%d-%m-%Y")
    )


# ==========================================
# GENERATE PDF REPORT
# ==========================================

def generate_report():

    os.makedirs("reports", exist_ok=True)

    file_path = "reports/security_audit_report.pdf"

    pdf = NumberedCanvas(
        file_path,
        pagesize=A4
    )

    # PDF Metadata
    pdf.setTitle("Security Audit Report")
    pdf.setAuthor("Password Cracking & Credential Attack Suite")
    pdf.setSubject("Password and Credential Security Analysis")

    # ======================================
    # PAGE 1
    # ======================================

    draw_page_design(pdf, "Security Audit Report")

    # Report title
    pdf.setFillColor(colors.HexColor("#142D4E"))
    pdf.setFont("Helvetica-Bold", 21)

    pdf.drawString(
        LEFT_MARGIN,
        750,
        "Security Audit Report"
    )

    # Project information
    pdf.setFillColor(colors.black)
    pdf.setFont("Helvetica-Bold", 14)

    pdf.drawString(
        LEFT_MARGIN,
        710,
        "Project Information"
    )

    pdf.setFont("Helvetica", 10)

    pdf.drawString(
        LEFT_MARGIN,
        685,
        "Project: Password Cracking & Credential Attack Suite"
    )

    pdf.drawString(
        LEFT_MARGIN,
        665,
        "Report Date: " + datetime.now().strftime("%d-%m-%Y")
    )

    pdf.drawString(
        LEFT_MARGIN,
        645,
        "Report Type: Security Analysis"
    )

    # Module status
    pdf.setFont("Helvetica-Bold", 14)

    pdf.drawString(
        LEFT_MARGIN,
        605,
        "Module Status"
    )

    data = [
        ["Module", "Status"],
        ["Password Strength Analyzer", "Implemented"],
        ["Hash Analyzer", "Implemented"],
        ["Dictionary Generator", "Implemented"],
        ["Brute Force Simulator", "Implemented"],
        ["Linux Shadow Analyzer", "Pending"],
        ["Windows SAM Analyzer", "Pending"],
        ["SQLite Integration", "Implemented"]
    ]

    table = Table(
        data,
        colWidths=[280, 150],
        rowHeights=25
    )

    table.setStyle(TableStyle([

        ("BACKGROUND", (0, 0), (-1, 0),
         colors.HexColor("#142D4E")),

        ("TEXTCOLOR", (0, 0), (-1, 0),
         colors.white),

        ("GRID", (0, 0), (-1, -1),
         0.5, colors.HexColor("#CBD5E1")),

        ("FONTNAME", (0, 0), (-1, 0),
         "Helvetica-Bold"),

        ("FONTSIZE", (0, 0), (-1, -1), 9),

        ("ALIGN", (0, 0), (-1, -1), "LEFT"),

        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

        ("LEFTPADDING", (0, 0), (-1, -1), 8),

        ("BACKGROUND", (0, 1), (-1, -1),
         colors.HexColor("#F1F5F9"))

    ]))

    table.wrapOn(pdf, 0, 0)
    table.drawOn(pdf, LEFT_MARGIN, 390)

    # Sample analysis results
    pdf.setFont("Helvetica-Bold", 14)

    pdf.drawString(
        LEFT_MARGIN,
        355,
        "Sample Analysis Results"
    )

    results = [
        "Password Analysis: Strong (sample input)",
        "Hash Analysis: SHA-256 format identified (sample)",
        "Dictionary Generator: Sample wordlist generated",
        "Brute Force Simulator: Bounded simulation completed",
        "Database: SQLite sample record available"
    ]

    pdf.setFont("Helvetica", 10)

    y = 330

    for result in results:

        pdf.setFillColor(colors.HexColor("#334155"))

        pdf.drawString(
            LEFT_MARGIN + 10,
            y,
            result
        )

        y -= 22

    # ======================================
    # PAGE 2
    # ======================================

    pdf.showPage()

    draw_page_design(
        pdf,
        "Security Recommendations"
    )

    # Page title
    pdf.setFillColor(colors.HexColor("#142D4E"))
    pdf.setFont("Helvetica-Bold", 20)

    pdf.drawString(
        LEFT_MARGIN,
        750,
        "Security Recommendations"
    )

    # Introduction
    pdf.setFillColor(colors.black)
    pdf.setFont("Helvetica", 10)

    pdf.drawString(
        LEFT_MARGIN,
        710,
        "Recommended practices for improving password security:"
    )

    # Recommendations
    recommendations = [
        "Use passwords with at least 12 characters.",
        "Avoid commonly used passwords.",
        "Use a unique password for every account.",
        "Enable Multi-Factor Authentication (MFA).",
        "Store passwords using secure hashing algorithms.",
        "Monitor suspicious login attempts.",
        "Regularly review account security."
    ]

    y = 670

    for index, recommendation in enumerate(recommendations, 1):

        pdf.setFillColor(colors.HexColor("#142D4E"))
        pdf.setFont("Helvetica-Bold", 10)

        pdf.drawString(
            LEFT_MARGIN,
            y,
            f"{index}."
        )

        pdf.setFillColor(colors.HexColor("#334155"))
        pdf.setFont("Helvetica", 10)

        pdf.drawString(
            LEFT_MARGIN + 25,
            y,
            recommendation
        )

        y -= 35

    # Conclusion section
    pdf.setFillColor(colors.HexColor("#142D4E"))
    pdf.setFont("Helvetica-Bold", 15)

    pdf.drawString(
        LEFT_MARGIN,
        390,
        "Conclusion"
    )

    pdf.setFillColor(colors.HexColor("#334155"))
    pdf.setFont("Helvetica", 10)

    pdf.drawString(
        LEFT_MARGIN,
        360,
        "This report summarizes the security analysis"
    )

    pdf.drawString(
        LEFT_MARGIN,
        342,
        "performed by the Password Cracking &"
    )

    pdf.drawString(
        LEFT_MARGIN,
        324,
        "Credential Attack Suite."
    )

    # ======================================
    # SAVE PDF
    # ======================================

    pdf.save()

    print("\nSecurity Audit Report Generated Successfully!")
    print("Report Location:", file_path)
    print("Total Pages: 2")


# ==========================================
# RUN PROGRAM
# ==========================================

if __name__ == "__main__":
    generate_report()
