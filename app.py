
from flask import Flask, render_template, request, Response, send_file

# Existing modules
from modules.password_analyzer import analyze_password
from modules.hash_analyzer import analyze_hash
from modules.dictionary_generator import generate_wordlist
from modules.brute_force_simulator import simulate_brute_force
from modules.report_generator import generate_audit_report
from modules.windows_hash_parser import analyze_windows_accounts

from modules.credential_file_analyzer import (
    analyze_linux_shadow,
    analyze_windows_sam
)

# Database functions
from modules.database import (
    initialize_db,
    save_analysis,
    get_history,
    get_dashboard_stats
)

app = Flask(__name__)


# =====================================
# MAIN DASHBOARD
# =====================================

@app.route("/")
def home():

    stats = get_dashboard_stats()
    records = get_history()

    return render_template(
        "index.html",
        stats=stats,
        records=records[:5]
    )

# =====================================
# PASSWORD STRENGTH ANALYZER
# =====================================

@app.route("/analyzer", methods=["GET", "POST"])
def analyzer():

    result = None

    if request.method == "POST":

        password = request.form.get("password", "")

        print("DEBUG: Password length received by Flask:", len(password))

        result = analyze_password(password)

        print("DEBUG: Analyzer error:", result.get("error"))

        if result:
            result_label = (
                result.get("strength")
                or result.get("status")
                or "Completed"
            )

            save_analysis(
                "Password",
                str(result_label),
                "Password strength analysis completed"
            )

    return render_template(
        "analyzer.html",
        result=result
    )


# =====================================
# HASH ANALYZER
# =====================================

@app.route("/hash-analyzer", methods=["GET", "POST"])
def hash_analyzer():

    result = None

    if request.method == "POST":

        hash_value = request.form.get("hash_value", "")

        if hash_value.strip():

            result = analyze_hash(hash_value)

            if result:
                result_label = result.get("status", "Completed")

                save_analysis(
                    "Hash",
                    str(result_label),
                    "Hash format analysis completed"
                )

        else:

            result = {
                "status": "Invalid",
                "message": "Please enter a hash value."
            }

    return render_template(
        "hash_analyzer.html",
        result=result
    )


# =====================================
# DICTIONARY GENERATOR
# =====================================

@app.route("/dictionary-generator", methods=["GET", "POST"])
def dictionary_generator():

    result = None

    if request.method == "POST":

        keyword_input = request.form.get("keywords", "")

        keywords = [
            word.strip()
            for word in keyword_input.replace(",", "\n").splitlines()
            if word.strip()
        ]

        include_numbers = (
            request.form.get("include_numbers") == "on"
        )

        if keywords:
            result = generate_wordlist(
                keywords,
                include_numbers
            )

    return render_template(
        "dictionary_generator.html",
        result=result
    )


# =====================================
# DOWNLOAD WORDLIST
# =====================================

@app.route("/download-wordlist", methods=["POST"])
def download_wordlist():

    wordlist = request.form.get("wordlist", "")

    return Response(
        wordlist,
        mimetype="text/plain",
        headers={
            "Content-Disposition":
            "attachment; filename=sample_wordlist.txt"
        }
    )


# =====================================
# BRUTE FORCE SIMULATOR
# =====================================

@app.route("/brute-force", methods=["GET", "POST"])
def brute_force():

    result = None

    if request.method == "POST":

        target_password = request.form.get(
            "target_password", ""
        )

        wordlist_input = request.form.get(
            "wordlist", ""
        )

        wordlist = [
            word.strip()
            for word in wordlist_input.splitlines()
            if word.strip()
        ]

        if target_password and wordlist:

            result = simulate_brute_force(
                target_password,
                wordlist,
                max_attempts=100
            )

    return render_template(
        "brute_force.html",
        result=result
    )


# =====================================
# CREDENTIAL FILE ANALYZER
# =====================================

@app.route(
    "/credential-file-analyzer",
    methods=["GET", "POST"]
)
def credential_file_analyzer():

    linux_result = None
    windows_result = None

    if request.method == "POST":

        linux_records = request.form.get(
            "linux_records", ""
        )

        windows_records = request.form.get(
            "windows_records", ""
        )

        if linux_records.strip():
            linux_result = analyze_linux_shadow(
                linux_records
            )

        if windows_records.strip():
            windows_result = analyze_windows_sam(
                windows_records
            )

    return render_template(
        "credential_file_analyzer.html",
        linux_result=linux_result,
        windows_result=windows_result
    )


# =====================================
# ANALYSIS HISTORY
# =====================================

@app.route("/history")
def history():

    records = get_history()

    return render_template(
        "history.html",
        records=records
    )
    
# =====================================
# PDF AUDIT REPORT
# =====================================

@app.route("/download-report")
def download_report():

    # Retrieve saved analysis records
    records = get_history()

    # Generate PDF
    pdf_file = generate_audit_report(records)

    # Send PDF to browser
    return send_file(
        pdf_file,
        as_attachment=True,
        download_name="security_audit_report.pdf",
        mimetype="application/pdf"
    )
# =====================================
# WINDOWS SAM SAMPLE ANALYZER
# =====================================

@app.route("/windows-sam-analyzer", methods=["GET", "POST"])
def windows_sam_analyzer():

    result = None

    if request.method == "POST":

        sam_records = request.form.get(
            "sam_records", ""
        )

        if sam_records.strip():

            result = analyze_windows_accounts(
                sam_records
            )

            save_analysis(
                "Windows SAM Sample",
                f"{result['valid_records']} valid records",
                "Synthetic Windows account metadata analyzed"
            )

    return render_template(
        "windows_sam_analyzer.html",
        result=result
    )

# =====================================
# START FLASK APPLICATION
# =====================================

if __name__ == "__main__":

    initialize_db()

    app.run(debug=True)
