import re

EMAIL_REGEX = re.compile(
    r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
)

PHONE_REGEX = re.compile(
    r"(?:\+?\d{1,3}[\s-]?)?(?:\(?\d{3}\)?[\s-]?)?\d{3}[\s-]?\d{4}"
)


def extract_emails(text):
    """
    Extract all email addresses from text.
    Returns a list.
    """
    if not text or not isinstance(text, str):
        return []

    return list(set(EMAIL_REGEX.findall(text)))


def extract_primary_email(text):
    """
    Extract the first email (primary contact).
    """
    emails = extract_emails(text)
    return emails[0] if emails else "Not found"


def extract_phone_numbers(text):
    """
    Extract possible phone numbers from text.
    Returns a list.
    """
    if not text or not isinstance(text, str):
        return []

    phones = PHONE_REGEX.findall(text)

    # Clean phone numbers
    cleaned = []
    for p in phones:
        p = re.sub(r"[^\d+]", "", p)
        if len(p) >= 10:
            cleaned.append(p)

    return list(set(cleaned))
