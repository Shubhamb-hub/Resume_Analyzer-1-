import re
import unicodedata


def clean_text(text: str) -> str:
    """
    Clean OCR / resume text for NLP, embeddings, and extraction.

    Goals:
    - Remove OCR noise
    - Preserve semantic meaning
    - Keep emails, skills, dates intact
    """

    if not text or not isinstance(text, str):
        return ""

    # --------------------------------------------------
    # 1. Normalize unicode characters
    # --------------------------------------------------
    text = unicodedata.normalize("NFKD", text)

    # --------------------------------------------------
    # 2. Remove common OCR junk & bullets
    # --------------------------------------------------
    text = re.sub(
        r"[•●▪■◆►◦▪️▸➤]+",
        " ",
        text
    )

    # --------------------------------------------------
    # 3. Fix broken words (e.g., d a t a → data)
    # --------------------------------------------------
    text = re.sub(
        r"\b([a-zA-Z])\s+([a-zA-Z])\b",
        r"\1\2",
        text
    )

    # --------------------------------------------------
    # 4. Remove page numbers & headers
    # --------------------------------------------------
    text = re.sub(
        r"\bpage\s*\d+\b",
        " ",
        text,
        flags=re.IGNORECASE
    )

    # --------------------------------------------------
    # 5. Remove excessive punctuation (keep useful ones)
    # --------------------------------------------------
    text = re.sub(
        r"[^\w\s@.+,/:-]",
        " ",
        text
    )

    # --------------------------------------------------
    # 6. Normalize whitespace
    # --------------------------------------------------
    text = re.sub(r"\s+", " ", text)

    # --------------------------------------------------
    # 7. Lowercase (best for embeddings)
    # --------------------------------------------------
    text = text.lower()

    # --------------------------------------------------
    # 8. Strip final text
    # --------------------------------------------------
    return text.strip()
