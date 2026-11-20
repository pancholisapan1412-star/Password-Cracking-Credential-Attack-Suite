
MAX_INPUT_LENGTH = 100000
MAX_RECORDS = 1000
MAX_USERNAME_LENGTH = 256
MAX_HASH_METADATA_LENGTH = 50


def analyze_windows_accounts(raw_data):
    """
    Analyze synthetic Windows account metadata.
    This module does not process actual password hashes.
    """

    # Validate input type
    if not isinstance(raw_data, str):
        return {
            "total_records": 0,
            "valid_records": 0,
            "invalid_records": 0,
            "enabled_accounts": 0,
            "disabled_accounts": 0,
            "accounts": [],
            "errors": [{
                "line": 0,
                "status": "Invalid",
                "message": "Input must be provided as text."
            }]
        }

    # Check empty input
    if not raw_data.strip():
        return {
            "total_records": 0,
            "valid_records": 0,
            "invalid_records": 0,
            "enabled_accounts": 0,
            "disabled_accounts": 0,
            "accounts": [],
            "errors": [{
                "line": 0,
                "status": "Invalid",
                "message": "Please provide sample records."
            }]
        }

    # Check maximum input size
    if len(raw_data) > MAX_INPUT_LENGTH:
        return {
            "total_records": 0,
            "valid_records": 0,
            "invalid_records": 0,
            "enabled_accounts": 0,
            "disabled_accounts": 0,
            "accounts": [],
            "errors": [{
                "line": 0,
                "status": "Invalid",
                "message": "Input exceeds the maximum allowed size."
            }]
        }

    results = []

    lines = raw_data.strip().splitlines()

    if len(lines) > MAX_RECORDS:
        return {
            "total_records": 0,
            "valid_records": 0,
            "invalid_records": 0,
            "enabled_accounts": 0,
            "disabled_accounts": 0,
            "accounts": [],
            "errors": [{
                "line": 0,
                "status": "Invalid",
                "message": "Maximum 1000 records are allowed."
            }]
        }

    for line_number, line in enumerate(lines, start=1):

        line = line.strip()

        if not line:
            continue

        parts = line.split(":")

        if len(parts) != 4:
            results.append({
                "line": line_number,
                "status": "Invalid",
                "message": "Incorrect record format."
            })
            continue

        username, rid, account_status, hash_type = parts

        username = username.strip()
        rid = rid.strip()
        account_status = account_status.strip().lower()
        hash_type = hash_type.strip()

        # Validate username
        if not username:
            results.append({
                "line": line_number,
                "status": "Invalid",
                "message": "Username is missing."
            })
            continue

        if len(username) > MAX_USERNAME_LENGTH:
            results.append({
                "line": line_number,
                "status": "Invalid",
                "message": "Username exceeds 256 characters."
            })
            continue

        # Validate RID
        if not rid.isdigit():
            results.append({
                "line": line_number,
                "status": "Invalid",
                "message": "RID must be numeric."
            })
            continue

        rid_number = int(rid)

        if not 0 <= rid_number <= 4294967295:
            results.append({
                "line": line_number,
                "status": "Invalid",
                "message": "RID is outside the allowed range."
            })
            continue

        # Validate account status
        if account_status not in ["enabled", "disabled"]:
            results.append({
                "line": line_number,
                "status": "Invalid",
                "message": "Unknown account status."
            })
            continue

        # Validate hash metadata
        if not hash_type:
            results.append({
                "line": line_number,
                "status": "Invalid",
                "message": "Hash metadata is missing."
            })
            continue

        if len(hash_type) > MAX_HASH_METADATA_LENGTH:
            results.append({
                "line": line_number,
                "status": "Invalid",
                "message": "Hash metadata exceeds 50 characters."
            })
            continue

        # Identify common accounts
        if rid_number == 500:
            account_type = "Administrator"

        elif rid_number == 501:
            account_type = "Guest"

        else:
            account_type = "Standard / Other"

        results.append({
            "line": line_number,
            "username": username,
            "rid": rid_number,
            "account_status": account_status.title(),
            "hash_type": hash_type,
            "account_type": account_type,
            "status": "Valid"
        })

    valid_records = [
        item for item in results
        if item["status"] == "Valid"
    ]

    invalid_records = [
        item for item in results
        if item["status"] == "Invalid"
    ]

    enabled_accounts = sum(
        1 for item in valid_records
        if item["account_status"] == "Enabled"
    )

    disabled_accounts = sum(
        1 for item in valid_records
        if item["account_status"] == "Disabled"
    )

    return {
        "total_records": len(results),
        "valid_records": len(valid_records),
        "invalid_records": len(invalid_records),
        "enabled_accounts": enabled_accounts,
        "disabled_accounts": disabled_accounts,
        "accounts": valid_records,
        "errors": invalid_records
    }
