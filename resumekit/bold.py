"""Bold job-description keywords inside the bullets of an existing .docx resume.

Only bullet paragraphs (text starting with the bullet glyph) are touched.
Matching is case-insensitive, whole-phrase, longest term first, with a cap on
how many terms get bolded per bullet so nothing turns into a wall of bold.
"""
from __future__ import annotations

import copy
import re

from docx import Document
from docx.text.run import Run

from .builder import BULLET

MAX_PER_BULLET = 3


def _pattern(terms):
    terms = sorted({t for t in terms if t.strip()}, key=len, reverse=True)
    if not terms:
        raise ValueError("no terms given")
    return re.compile(r"(?<![\w/])(" + "|".join(re.escape(t) for t in terms) + r")(?![\w/])", re.I)


def bold_docx(src: str, terms, dst: str | None = None, max_per_bullet: int = MAX_PER_BULLET) -> int:
    """Bold `terms` in bullet text of `src`; save to `dst` (or in place). Returns count bolded."""
    rx = _pattern(terms)
    doc = Document(src)
    total = 0
    for p in doc.paragraphs:
        if not p.runs or not p.runs[0].text.startswith(BULLET):
            continue
        hits = sum(1 for r in p.runs[1:] if r.bold)
        for r in list(p.runs[1:]):
            if r.bold or not rx.search(r.text):
                continue
            parts = rx.split(r.text)
            r.text = parts[0]
            prev = r._r
            for i, t in enumerate(parts[1:], 1):
                if not t:
                    continue
                is_term = i % 2 == 1
                make_bold = is_term and hits < max_per_bullet
                hits += is_term
                node = copy.deepcopy(r._r)
                prev.addnext(node)
                prev = node
                nr = Run(node, p)
                nr.text = t
                nr.bold = make_bold
                total += make_bold
    doc.save(dst or src)
    return total
