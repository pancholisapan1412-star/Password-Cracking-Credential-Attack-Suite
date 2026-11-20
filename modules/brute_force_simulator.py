
MAX_ATTEMPTS = 100
MAX_WORDLIST_SIZE = 500
MAX_PASSWORD_LENGTH = 256


def simulate_brute_force(target_password, wordlist, max_attempts=100):
    """
    Simulate password guessing offline using sample data.
    Maximum attempts are strictly limited.
    """

    # Validate target password
    if not isinstance(target_password, str):
        return {
            "status": "Invalid",
            "password_found": False,
            "attempts": 0,
            "message": "Target password must be text."
        }

    if not target_password.strip():
        return {
            "status": "Invalid",
            "password_found": False,
            "attempts": 0,
            "message": "Please enter a target password."
        }

    if len(target_password) > MAX_PASSWORD_LENGTH:
        return {
            "status": "Invalid",
            "password_found": False,
            "attempts": 0,
            "message": "Target password cannot exceed 256 characters."
        }

    # Validate wordlist
    if not isinstance(wordlist, list):
        return {
            "status": "Invalid",
            "password_found": False,
            "attempts": 0,
            "message": "Wordlist must be provided as a list."
        }

    if not wordlist:
        return {
            "status": "Invalid",
            "password_found": False,
            "attempts": 0,
            "message": "Please provide a wordlist."
        }

    # Keep only valid, non-empty text entries
    valid_wordlist = [
        guess for guess in wordlist
        if isinstance(guess, str) and guess.strip()
    ]

    if not valid_wordlist:
        return {
            "status": "Invalid",
            "password_found": False,
            "attempts": 0,
            "message": "Wordlist contains no valid entries."
        }

    # Validate maximum attempts
    if isinstance(max_attempts, bool) or not isinstance(max_attempts, int):
        return {
            "status": "Invalid",
            "password_found": False,
            "attempts": 0,
            "message": "Maximum attempts must be a whole number."
        }

    if max_attempts <= 0:
        return {
            "status": "Invalid",
            "password_found": False,
            "attempts": 0,
            "message": "Maximum attempts must be greater than zero."
        }

    # Apply strict safety limits
    max_attempts = min(max_attempts, MAX_ATTEMPTS)
    valid_wordlist = valid_wordlist[:MAX_WORDLIST_SIZE]

    attempts = 0

    for guess in valid_wordlist:

        if attempts >= max_attempts:
            break

        attempts += 1

        print(f"Attempt {attempts}: {guess}")

        if guess == target_password:
            return {
                "status": "Success",
                "password_found": True,
                "attempts": attempts,
                "message": "Sample password found!"
            }

    return {
        "status": "Failed",
        "password_found": False,
        "attempts": attempts,
        "message": "Password not found within the attempt limit."
    }


# Test using sample data only
if __name__ == "__main__":

    sample_password = "cricket123"

    sample_wordlist = [
        "hello",
        "python",
        "coffee",
        "cricket",
        "cricket123",
        "password123"
    ]

    result = simulate_brute_force(
        sample_password,
        sample_wordlist,
        max_attempts=100
    )

    print("\n--- Simulation Results ---")
    print(result)
