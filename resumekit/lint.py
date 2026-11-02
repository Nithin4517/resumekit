"""Lint resume content before building: catch claims you never want to make.

Keep a list of banned patterns (tools you haven't used, certifications you
don't hold, outdated names) in a rules file, and lint every tailored profile
against it. Also flags present-tense verbs in past-role bullets and estimates
total length so a draft can be padded or trimmed before rendering.
"""
from __future__ import annotations

import re

from .builder import load_file

DEFAULT_RULES = {
    "banned": [],                # regexes (case-insensitive) that must never appear
    "min_words": 450,            # rough content-length floor
    "max_words": 1100,
    "summary_bullets": None,     # e.g. [4, 6] -> allowed range
    "bullets_per_role": None,    # e.g. [3, 8]
    "require_past_tense": True,  # bullets of past roles open with a past-tense verb
}

IRREGULAR_PAST = {
    "built", "wrote", "led", "ran", "made", "troubleshot", "held", "kept", "set", "drove", "took",
    "gave", "brought", "taught", "oversaw", "won", "sought", "met", "put", "sent", "spent", "found",
    "grew", "began", "rebuilt", "bought", "dealt", "understood", "undertook", "cut", "chose", "shut",
}
PRESENT_S = re.compile(
    r"\b(manages|maintains|provides|configures|troubleshoots|handles|resolves|ensures|performs|"
    r"coordinates|delivers|develops|deploys|oversees|implements|installs|diagnoses|validates|"
    r"automates|owns|writes|builds|creates|analyzes|trains|supports|administers|monitors)\b", re.I)


def _strip(s: str) -> str:
    return s.replace("**", "")


def _texts(data: dict):
    yield "headline", data.get("headline", "")
    for i, b in enumerate(data.get("summary", []), 1):
        yield f"summary #{i}", b
    skills = data.get("skills") or {}
    for cat, items in (skills.items() if isinstance(skills, dict) else skills):
        yield f"skills/{cat}", f"{cat}: {items if isinstance(items, str) else ', '.join(items)}"
    for e in data.get("experience", []):
        yield f"{e['company']} title", e.get("title", "")
        for i, b in enumerate(e.get("bullets", []), 1):
            yield f"{e['company']} #{i}", b


def lint(data: dict, rules: dict | None = None) -> list[str]:
    r = {**DEFAULT_RULES, **(rules or {})}
    probs = []
    for where, text in _texts(data):
        for pat in r["banned"]:
            m = re.search(pat, _strip(text), re.I)
            if m:
                probs.append(f"banned term {m.group(0)!r} in {where}")
    if r["require_past_tense"]:
        for e in data.get("experience", []):
            current = "present" in str(e.get("dates", "")).lower()
            for i, b in enumerate(e.get("bullets", []), 1):
                t = _strip(b)
                first = (re.match(r"[A-Za-z-]+", t) or [""])[0].lower()
                if not current and not (first.endswith("ed") or first in IRREGULAR_PAST):
                    probs.append(f"{e['company']} #{i} opens with {first!r} (not past tense)")
                m = PRESENT_S.search(t)
                if m and not current:
                    probs.append(f"{e['company']} #{i} uses present-tense {m.group(1)!r}")
    if r["summary_bullets"]:
        lo, hi = r["summary_bullets"]
        n = len(data.get("summary", []))
        if not lo <= n <= hi:
            probs.append(f"summary has {n} bullets (allowed {lo}-{hi})")
    if r["bullets_per_role"]:
        lo, hi = r["bullets_per_role"]
        for e in data.get("experience", []):
            n = len(e.get("bullets", []))
            if not lo <= n <= hi:
                probs.append(f"{e['company']} has {n} bullets (allowed {lo}-{hi})")
    words = sum(len(_strip(t).split()) for _, t in _texts(data))
    if words < r["min_words"]:
        probs.append(f"~{words} content words; below floor {r['min_words']}")
    if words > r["max_words"]:
        probs.append(f"~{words} content words; above cap {r['max_words']}")
    return probs


def lint_files(profile: str, tailoring: str | None, rules: str | None) -> list[str]:
    from .builder import merge
    data = merge(load_file(profile), load_file(tailoring) if tailoring else None)
    return lint(data, load_file(rules) if rules else None)
