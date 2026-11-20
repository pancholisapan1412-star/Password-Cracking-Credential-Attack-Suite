
MAX_KEYWORDS = 10
MAX_KEYWORD_LENGTH = 50
MAX_WORDLIST_SIZE = 500

NUMERIC_SUFFIXES = ["123", "1234", "2026"]


def generate_wordlist(keywords, include_numbers=False):
    """
    Generate a small custom sample wordlist
    for authorized, offline security testing.
    """

    # Validate keyword input
    if not isinstance(keywords, list):
        return {
            "status": "Invalid",
            "message": "Keywords must be provided as a list."
        }

    if not keywords:
        return {
            "status": "Invalid",
            "message": "Please provide at least one keyword."
        }

    if not isinstance(include_numbers, bool):
        return {
            "status": "Invalid",
            "message": "include_numbers must be True or False."
        }

    wordlist = set()

    # Limit the number of keywords
    keywords = keywords[:MAX_KEYWORDS]

    for keyword in keywords:

        # Validate individual keyword
        if not isinstance(keyword, str):
            continue

        keyword = keyword.strip()

        if not keyword:
            continue

        if len(keyword) > MAX_KEYWORD_LENGTH:
            continue

        # Original keyword
        wordlist.add(keyword)

        # Capitalized version
        wordlist.add(keyword.capitalize())

        # Uppercase version
        wordlist.add(keyword.upper())

        # Lowercase version
        wordlist.add(keyword.lower())

        # Optional numeric suffixes
        if include_numbers:
            for number in NUMERIC_SUFFIXES:
                wordlist.add(keyword + number)
                wordlist.add(keyword.capitalize() + number)

    # Check whether any valid keywords were provided
    if not wordlist:
        return {
            "status": "Invalid",
            "message": "No valid keywords were provided."
        }

    # Keep output predictable and limited
    results = sorted(wordlist)[:MAX_WORDLIST_SIZE]

    return results


# Test the generator
if __name__ == "__main__":

    sample_keywords = [
        "coffee",
        "cricket",
        "python"
    ]

    results = generate_wordlist(
        sample_keywords,
        include_numbers=True
    )

    print("Dictionary Generator Results")
    print("--------------------------------")

    if isinstance(results, dict):
        print(results["message"])
    else:
        for word in results:
            print(word)

        print("--------------------------------")
        print("Total generated words:", len(results))
