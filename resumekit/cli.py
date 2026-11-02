"""Command-line entry point: `resumekit <command> ...`."""
from __future__ import annotations

import argparse
import sys


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="resumekit", description="Tailor, build and check .docx resumes.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("build", help="build a .docx (and optional PDF) from a profile")
    b.add_argument("profile")
    b.add_argument("-t", "--tailor", help="per-job overrides (YAML/JSON)")
    b.add_argument("-o", "--out", required=True, help="output .docx path")
    b.add_argument("--pdf", action="store_true", help="also convert to PDF with LibreOffice")
    b.add_argument("-r", "--rules", help="lint rules file; build is refused if lint fails")

    l = sub.add_parser("lint", help="check content against your rules before building")
    l.add_argument("profile")
    l.add_argument("-t", "--tailor")
    l.add_argument("-r", "--rules")

    k = sub.add_parser("bold", help="bold keywords inside bullets of an existing .docx")
    k.add_argument("docx")
    k.add_argument("terms", nargs="+")
    k.add_argument("--max", type=int, default=3, help="max bolded terms per bullet")

    c = sub.add_parser("check", help="check rendered PDFs for layout problems")
    c.add_argument("pdfs", nargs="+")
    c.add_argument("--max-pages", type=int, default=2)
    c.add_argument("--min-words", type=int, default=0)
    c.add_argument("--max-words", type=int, default=10**6)

    s = sub.add_parser("screen", help="check whether you've already applied to a company")
    s.add_argument("companies", nargs="+")
    s.add_argument("--log", help="CSV with a 'company' column")
    s.add_argument("--folder", help="folder of previously generated resumes")
    s.add_argument("--ignore", nargs="*", default=[], help="extra words to ignore (e.g. your name)")

    a = ap.parse_args(argv)

    if a.cmd in ("build", "lint"):
        from .lint import lint_files
        if a.cmd == "lint" or a.rules:
            probs = lint_files(a.profile, a.tailor, a.rules)
            for p in probs:
                print("  -", p)
            print(("LINT FAIL: %d issue(s)" % len(probs)) if probs else "LINT PASS")
            if probs or a.cmd == "lint":
                return 1 if probs else 0
        from .builder import build_from_files
        for p in build_from_files(a.profile, a.tailor, a.out, a.pdf):
            print("wrote", p)
        return 0

    if a.cmd == "bold":
        from .bold import bold_docx
        print("bolded", bold_docx(a.docx, a.terms, max_per_bullet=a.max), "terms")
        return 0

    if a.cmd == "check":
        from .check_pdf import check_pdf
        total = 0
        for f in a.pdfs:
            probs = check_pdf(f, a.max_pages, a.min_words, a.max_words)
            print(("FAIL " if probs else "PASS ") + f)
            for p in probs:
                print("   -", p)
            total += len(probs)
        return 1 if total else 0

    if a.cmd == "screen":
        from .screen import load_corpus, screen
        corpus = load_corpus(a.log, a.folder)
        print(f"corpus: {len(corpus)} past entries\n")
        for name, r in screen(a.companies, corpus, a.ignore).items():
            print(f"=== {name} -> {r['verdict']}")
            for score, rarest, src, hit, key in r["hits"]:
                print(f"    {src:5} {key}  <{'+'.join(hit)} | rarest df={rarest}>")
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
