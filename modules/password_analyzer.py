
import re
import math


# Common passwords used for educational testing
COMMON_PASSWORDS = {
    "password",
    "password123",
    "123456",
    "12345678",
    "qwerty",
    "admin",
    "admin123",
    "welcome",
    "iloveyou",
    "abc123"
}

# Input validation limits
MIN_PASSWORD_LENGTH = 1
MAX_PASSWORD_LENGTH = 256


def validation_error(message):

    return {
        "score": 0,
        "strength": "Not Rated",
        "entropy": 0,
        "checks": {},
        "recommendations": [message],
        "error": message
    }


def analyze_password(password):

    # STEP 1: Validate input type

    if not isinstance(password, str):
        return validation_error(
            "Invalid input. Password must be text."
        )

    # STEP 2: Check empty input

    if not password or not password.strip():
        return validation_error(
            "Please enter a valid password."
        )

    # STEP 3: Check maximum length

    if len(password) > MAX_PASSWORD_LENGTH:
        return validation_error(
            f"Password cannot exceed {MAX_PASSWORD_LENGTH} characters."
        )

    # STEP 4: Character checks

    checks = {
        "length": len(password) >= 12,
        "uppercase": bool(re.search(r"[A-Z]", password)),
        "lowercase": bool(re.search(r"[a-z]", password)),
        "numbers": bool(re.search(r"[0-9]", password)),
        "symbols": bool(re.search(r"[^a-zA-Z0-9]", password))
    }

    # STEP 5: Estimate character pool size

    pool = 0

    if checks["lowercase"]:
        pool += 26

    if checks["uppercase"]:
        pool += 26

    if checks["numbers"]:
        pool += 10

    if checks["symbols"]:
        pool += 33

    # STEP 6: Calculate theoretical entropy

    if pool > 0:
        entropy = len(password) * math.log2(pool)
    else:
        entropy = 0

    # STEP 7: Detect predictable patterns

    lower_password = password.lower()

    common_match = lower_password in COMMON_PASSWORDS

    repeated_pattern = bool(
        re.search(r"(.)\1{3,}", password)
    )

    sequential_pattern = any(
        sequence in lower_password
        for sequence in [
            "1234",
            "abcd",
            "qwerty",
            "9876",
            "4321"
        ]
    )

    # STEP 8: Calculate strength score

    score = 0

    if len(password) >= 16:
        score += 30
    elif len(password) >= 12:
        score += 25
    elif len(password) >= 8:
        score += 15
    else:
        score += 5

    score += sum(checks.values()) * 6

    score += min(entropy / 100 * 25, 25)

    if not common_match:
        score += 10

    if not repeated_pattern and not sequential_pattern:
        score += 5

    if common_match:
        score = min(score, 15)

    score = min(round(score), 100)

    # STEP 9: Strength classification

    if score < 40:
        strength = "Weak"
    elif score < 60:
        strength = "Moderate"
    elif score < 80:
        strength = "Strong"
    else:
        strength = "Very Strong"

    # STEP 10: Recommendations

    recommendations = []

    if len(password) < 12:
        recommendations.append(
            "Use at least 12 characters. Longer is generally better."
        )

    if not checks["uppercase"]:
        recommendations.append(
            "Include uppercase letters."
        )

    if not checks["lowercase"]:
        recommendations.append(
            "Include lowercase letters."
        )

    if not checks["numbers"]:
        recommendations.append(
            "Include numbers."
        )

    if not checks["symbols"]:
        recommendations.append(
            "Consider including special characters."
        )

    if common_match:
        recommendations.append(
            "Avoid common passwords and predictable combinations."
        )

    if repeated_pattern or sequential_pattern:
        recommendations.append(
            "Avoid repeated characters and predictable sequences."
        )

    if not recommendations:
        recommendations.append(
            "Good result! Keep using unique passwords for every account."
        )

    # STEP 11: Return results

    return {
        "score": score,
        "strength": strength,
        "entropy": round(entropy, 2),
        "checks": checks,
        "recommendations": recommendations,
        "error": None
    }
