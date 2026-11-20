
import re


MAX_HASH_LENGTH = 128


def analyze_hash(hash_value):
    """
    Identify common hash formats using
    hexadecimal validation and character length.
    """

    # Validate input type
    if not isinstance(hash_value, str):
        return {
            "status": "Invalid",
            "message": "Hash must be provided as text."
        }

    # Remove surrounding whitespace
    hash_value = hash_value.strip()

    # Check empty input
    if not hash_value:
        return {
            "status": "Invalid",
            "message": "Please enter a hash value."
        }

    # Check maximum length
    if len(hash_value) > MAX_HASH_LENGTH:
        return {
            "status": "Invalid",
            "message": "Hash cannot exceed 128 characters."
        }

    # Check hexadecimal characters
    if not re.fullmatch(r"[a-fA-F0-9]+", hash_value):
        return {
            "status": "Invalid",
            "message": "Hash contains invalid characters."
        }

    hash_length = len(hash_value)

    hash_types = {
        32: "MD5 (Possible)",
        40: "SHA-1 (Possible)",
        64: "SHA-256 (Possible)",
        128: "SHA-512 (Possible)"
    }

    if hash_length in hash_types:
        return {
            "status": "Success",
            "hash_type": hash_types[hash_length],
            "length": hash_length,
            "message": "Possible hash format identified."
        }

    return {
        "status": "Unknown",
        "length": hash_length,
        "message": "Hash format not recognized."
    }


# Test the analyzer
if __name__ == "__main__":

    sample_hashes = [
        "5d41402abc4b2a76b9719d911017c592",
        "a" * 40,
        "a" * 64,
        "a" * 128,
        "hello123"
    ]

    for sample in sample_hashes:
        result = analyze_hash(sample)
        print("\nInput:", sample)
        print("Result:", result)
