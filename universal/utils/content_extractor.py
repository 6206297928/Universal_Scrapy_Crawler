import re
import trafilatura


def extract_content(html: str) -> str:
    """
    Extract main content from raw HTML using trafilatura.

    trafilatura handles:
      - Boilerplate removal (nav, footer, ads, sidebars)
      - Article/main content detection
      - Table extraction
      - Comment filtering

    Returns cleaned plain text, or empty string if extraction fails.
    """

    if not html:
        return ""

    content = trafilatura.extract(
        html,
        include_tables=True,
        include_comments=False,
        include_links=False,
        favor_recall=True,  # prefer more content over precision
    )

    if content:
        return _clean_text(content)

    return ""


def _clean_text(text: str) -> str:
    """Light cleanup on trafilatura output."""

    # Remove multiple blank lines (trafilatura preserves some structure)
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove weird unicode artifacts
    text = text.replace("\xa0", " ")

    return text.strip()


# ─── Legacy function (kept for backward compatibility) ──────
def clean_content(text: str) -> str:
    """Old text cleaner — used by universal_spider_copy (old spider)."""

    if not text:
        return ""

    text = re.sub(r"\s+", " ", text)
    text = text.replace("\xa0", " ")

    return text.strip()
