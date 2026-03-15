"""PDF parser for hedge fund investor letters."""

from __future__ import annotations

import re
from pathlib import Path


def parse_pdf(path: str) -> str:
    """Extract clean text from a PDF file.

    Handles multi-page PDFs and strips common header/footer patterns
    heuristically (page numbers, repeated title lines).

    Args:
        path: Path to the PDF file.

    Returns:
        Extracted text with pages joined by newlines.
    """
    import pdfplumber

    pages_text: list[str] = []

    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            text = _strip_header_footer(text)
            if text.strip():
                pages_text.append(text)

    return "\n\n".join(pages_text)


def parse_all(letters_dir: str = "letters") -> dict[str, str]:
    """Parse all PDF files in a directory.

    Args:
        letters_dir: Path to directory containing PDF files.
                     Defaults to "letters".

    Returns:
        Mapping of filename (without path) to extracted text.
    """
    directory = Path(letters_dir)
    results: dict[str, str] = {}

    for pdf_path in sorted(directory.glob("*.pdf")):
        results[pdf_path.name] = parse_pdf(str(pdf_path))

    return results


# Patterns that commonly appear in headers/footers of financial documents.
_PAGE_NUMBER_RE = re.compile(
    r"^\s*(?:page\s+)?\d+\s*(?:of\s+\d+)?\s*$", re.IGNORECASE
)
_CONFIDENTIAL_RE = re.compile(
    r"^\s*(?:confidential|proprietary|for\s+(?:internal|authorized)\s+use\s+only)\s*$",
    re.IGNORECASE,
)


def _strip_header_footer(text: str) -> str:
    """Remove likely header/footer lines from a page's text.

    Heuristic: drop the first and last non-empty lines if they match
    page-number or boilerplate patterns, or are very short (≤ 6 words)
    and appear to be a title/label repeated across pages.
    """
    lines = text.splitlines()

    def _is_boilerplate(line: str) -> bool:
        stripped = line.strip()
        if not stripped:
            return False
        if _PAGE_NUMBER_RE.match(stripped):
            return True
        if _CONFIDENTIAL_RE.match(stripped):
            return True
        # Short lines that are likely running headers (e.g. fund name, date)
        word_count = len(stripped.split())
        if word_count <= 4 and len(stripped) <= 60:
            return True
        return False

    # Drop leading boilerplate lines
    start = 0
    while start < len(lines) and _is_boilerplate(lines[start]):
        start += 1

    # Drop trailing boilerplate lines
    end = len(lines)
    while end > start and _is_boilerplate(lines[end - 1]):
        end -= 1

    return "\n".join(lines[start:end])
