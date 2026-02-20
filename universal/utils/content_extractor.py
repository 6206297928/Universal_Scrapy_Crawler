import re


def clean_content(text: str) -> str:
    """
    Clean extracted content by removing extra whitespace,
    scripts, and useless text.
    """

    if not text:
        return ""

    # Remove multiple spaces/newlines
    text = re.sub(r'\s+', ' ', text)

    # Remove weird unicode artifacts
    text = text.replace("\xa0", " ")

    return text.strip()
