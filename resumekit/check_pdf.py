"""Check a rendered resume PDF for layout problems a human reviewer would notice.

  P0  more pages than allowed
  P1  a page ends with a section header (header orphaned from its content)
  P2  a page ends with a job/school entry line (entry orphaned from its bullets)
  P3  a bullet looks split across a page break
  P4  word count outside the allowed range
  P5  last page is mostly empty
"""
from __future__ import annotations

import pdfplumber

from .builder import BULLET

HEADERS = {"PROFESSIONAL SUMMARY", "SUMMARY", "SKILLS", "CERTIFICATIONS", "WORK EXPERIENCE",
           "EXPERIENCE", "EDUCATION", "PROJECTS"}


def check_pdf(path: str, max_pages: int = 2, min_words: int = 0, max_words: int = 10**6,
              min_last_page_fill: float = 0.5) -> list[str]:
    with pdfplumber.open(path) as pdf:
        pages = [[l.strip() for l in (p.extract_text() or "").split("\n") if l.strip()] for p in pdf.pages]
        last = pdf.pages[-1]
        words_last = last.extract_words()
        fill = (max(w["bottom"] for w in words_last) / last.height) if words_last else 0
    probs = []
    if len(pages) > max_pages:
        probs.append(f"P0 {len(pages)} pages (max {max_pages})")
    for i in range(len(pages) - 1):
        a, b = pages[i], pages[i + 1]
        if not a or not b:
            continue
        if a[-1].upper() in HEADERS:
            probs.append(f"P1 page {i + 1} ends with section header {a[-1]!r}")
        elif " | " in a[-1] and not a[-1].startswith(BULLET):
            probs.append(f"P2 page {i + 1} ends with entry line {a[-1]!r}")
        if not b[0].startswith(BULLET) and b[0].upper() not in HEADERS and " | " not in b[0] \
                and a[-1].startswith(BULLET):
            probs.append(f"P3 bullet split across pages {i + 1}->{i + 2}: ...{b[0][:50]!r}")
    n = sum(len(" ".join(p).split()) for p in pages)
    if not min_words <= n <= max_words:
        probs.append(f"P4 {n} words (allowed {min_words}-{max_words})")
    if len(pages) > 1 and fill < min_last_page_fill:
        probs.append(f"P5 last page only {fill:.0%} filled (min {min_last_page_fill:.0%})")
    return probs
