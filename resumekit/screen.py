"""Duplicate-application screen: have I already applied to this company?

Compares company names against a log of past applications (CSV with a
`company` column) and/or a folder of previously generated resume files.

Matching is whole-word with camelCase splitting (so "Tire" never hits
"Retirement"), and hits are ranked by token rarity across the corpus, so a
match on a distinctive name outranks a match on "Credit Union".
"""
from __future__ import annotations

import csv
import glob
import os
import re
from collections import Counter

STOP = {"inc", "llc", "corp", "corporation", "company", "co", "ltd", "the", "group", "usa", "us",
        "of", "and", "resume", "cv", "cover", "letter", "pdf", "docx"}


def words(text: str) -> list[str]:
    text = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", text)
    text = re.sub(r"(?<=[A-Z])(?=[A-Z][a-z])", " ", text)
    return [w.lower() for w in re.findall(r"[A-Za-z0-9]+", text)]


def tokens(text: str, extra_stop=()) -> set[str]:
    stop = STOP | {s.lower() for s in extra_stop}
    return {w for w in words(text) if w not in stop and len(w) > 2}


def load_corpus(log_csv: str | None = None, folder: str | None = None) -> list[tuple[str, str]]:
    cands = []
    if log_csv and os.path.exists(log_csv):
        with open(log_csv, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                cands.append(("log", row.get("company", "")))
    if folder:
        for p in glob.glob(os.path.join(folder, "*")):
            if os.path.isfile(p):
                cands.append(("file", os.path.splitext(os.path.basename(p))[0]))
    return cands


def screen(names, corpus, extra_stop=(), top_n: int = 5) -> dict:
    ctoks = [tokens(k, extra_stop) for _, k in corpus]
    df = Counter(t for ts in ctoks for t in ts)
    results = {}
    for name in names:
        tk = tokens(name, extra_stop) or set(words(name))
        scored = []
        for (src, key), ct in zip(corpus, ctoks):
            hit = tk & ct
            if hit:
                score = sum(1.0 / (1 + df[t]) for t in hit)
                scored.append((score, min(df[t] for t in hit), src, sorted(hit), key))
        scored.sort(key=lambda x: -x[0])
        top = scored[0] if scored else None
        if top and ((len(top[3]) >= 2 and top[1] <= 3) or (len(tk) == 1 and top[1] <= 3)
                    or (len(top[3]) >= 3 and top[1] <= 6)):
            verdict = "DUPLICATE"
        elif top and (len(top[3]) >= 2 or top[1] <= 3):
            verdict = "REVIEW"
        else:
            verdict = "CLEAR"
        results[name] = {"verdict": verdict, "hits": scored[:top_n]}
    return results
