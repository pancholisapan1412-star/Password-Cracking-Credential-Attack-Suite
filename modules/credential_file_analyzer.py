
MAX_INPUT_LENGTH = 100000
MAX_RECORDS = 1000


def invalid_record(message):
    return {
        "username": "Unknown",
        "status": "Invalid",
        "message": message
    }


def validate_records(records):
    """Validate common input requirements."""

    if not isinstance(records, str):
        return None, invalid_record(
            "Input must be provided as text."
        )

    if not records.strip():
        return None, invalid_record(
            "Please provide sample records."
        )

    if len(records) > MAX_INPUT_LENGTH:
        return None, invalid_record(
            "Input exceeds the maximum allowed size."
        )

    lines = [
        line.strip()
        for line in records.splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]

    if len(lines) > MAX_RECORDS:
        return None, invalid_record(
            "Maximum 1000 records are allowed."
        )

    return lines, None


def analyze_linux_shadow(records):
    """Analyze synthetic Linux Shadow sample records."""

    lines, error = validate_records(records)

    if error:
        return [error]

    results = []

    for line in lines:

        fields = line.split(":")

        if len(fields) != 9:
            results.append(invalid_record(
                "Expected 9 fields."
            ))
            continue

        username = fields[0]
        password_field = fields[1]
        last_change = fields[2]

        if not username.strip():
            results.append(invalid_record(
                "Username cannot be empty."
            ))
            continue

        if not last_change.isdigit():
            results.append({
                "username": username,
                "status": "Invalid",
                "message": "Last change field must be numeric."
            })
            continue

        if password_field.startswith(("!", "*")):
            account_status = "Locked or disabled"
            hash_type = "Not available"

        elif password_field in (
            "$6$salt$samplehash",
            "$5$salt$samplehash",
            "$1$salt$samplehash",
            "$y$salt$samplehash"
        ):

            account_status = "Sample password field"

            if password_field.startswith("$6$"):
                hash_type = "SHA-512 crypt"
            elif password_field.startswith("$5$"):
                hash_type = "SHA-256 crypt"
            elif password_field.startswith("$1$"):
                hash_type = "MD5 crypt"
            else:
                hash_type = "yescrypt"

        else:
            results.append({
                "username": username,
                "status": "Unsupported",
                "message": "Only approved synthetic sample records are accepted."
            })
            continue

        results.append({
            "username": username,
            "status": account_status,
            "hash_type": hash_type,
            "last_change": last_change,
            "message": "Synthetic Linux Shadow record analyzed."
        })

    return results


def analyze_windows_sam(records):
    """Analyze synthetic Windows SAM-style sample records."""

    lines, error = validate_records(records)

    if error:
        return [error]

    results = []

    allowed_markers = {
        "LM_SAMPLE",
        "NT_SAMPLE",
        "SAMPLE_LM_HASH",
        "SAMPLE_NT_HASH",
        "",
        "*"
    }

    for line in lines:

        fields = line.split(":")

        if len(fields) != 7 or not fields[1].isdigit():
            results.append(invalid_record(
                "Expected username, numeric RID and 5 remaining fields."
            ))
            continue

        username = fields[0]
        rid = fields[1]
        lm_field = fields[2]
        nt_field = fields[3]

        if not username.strip():
            results.append(invalid_record(
                "Username cannot be empty."
            ))
            continue

        # Accept synthetic placeholders only.
        if lm_field not in allowed_markers or nt_field not in allowed_markers:
            results.append({
                "username": username,
                "status": "Unsupported",
                "message": "Only synthetic placeholder fields are accepted."
            })
            continue

        results.append({
            "username": username,
            "rid": rid,
            "lm_field": "Sample present" if lm_field else "Empty",
            "nt_field": "Sample present" if nt_field else "Empty",
            "status": "Success",
            "message": "Synthetic Windows SAM-style record analyzed."
        })

    return results


# Test using synthetic sample data only
if __name__ == "__main__":

    linux_sample = (
        "demo:$6$salt$samplehash:20000:0:99999:7:::"
    )

    windows_sample = (
        "demo:1001:LM_SAMPLE:NT_SAMPLE:::"
    )

    print("LINUX SHADOW ANALYSIS")
    print(analyze_linux_shadow(linux_sample))

    print("\nWINDOWS SAM ANALYSIS")
    print(analyze_windows_sam(windows_sample))
