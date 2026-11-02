"""Build an ATS-friendly .docx resume from a profile (YAML/JSON/dict).

A profile describes the person; a tailoring file (optional) overrides the parts
that change per job: headline, summary, skills, bullets, job titles.

Inline markup: wrap a phrase in **double asterisks** to render it bold.
"""
from __future__ import annotations

import json
import os
from typing import Any

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

BULLET = "●"

DEFAULT_STYLE = {
    "font": "Calibri",
    "accent": "1F4E79",
    "body_size": 10.5,
    "name_size": 18,
    "margins_in": {"top": 0.45, "bottom": 0.4, "left": 0.6, "right": 0.6},
}


def load_file(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        if path.endswith((".yaml", ".yml")):
            import yaml
            return yaml.safe_load(f) or {}
        return json.load(f)


def merge(profile: dict, tailoring: dict | None) -> dict:
    """Shallow-merge a tailoring dict into a profile.

    `experience` in a tailoring file may be a dict keyed by employer name,
    overriding only `title` and/or `bullets` for that entry.
    """
    out = dict(profile)
    for k, v in (tailoring or {}).items():
        if k == "experience" and isinstance(v, dict):
            exps = [dict(e) for e in out.get("experience", [])]
            for e in exps:
                if e.get("company") in v:
                    e.update(v[e["company"]])
            out["experience"] = exps
        else:
            out[k] = v
    return out


class _Doc:
    def __init__(self, style: dict):
        self.s = {**DEFAULT_STYLE, **(style or {})}
        self.accent = RGBColor.from_string(self.s["accent"])
        self.doc = Document()
        m = self.s["margins_in"]
        for sec in self.doc.sections:
            sec.top_margin, sec.bottom_margin = Inches(m["top"]), Inches(m["bottom"])
            sec.left_margin, sec.right_margin = Inches(m["left"]), Inches(m["right"])
            self.width = sec.page_width - sec.left_margin - sec.right_margin
        normal = self.doc.styles["Normal"]
        normal.font.size = Pt(self.s["body_size"])
        normal.paragraph_format.space_after = Pt(0)
        normal.paragraph_format.line_spacing = 1.02
        self._font_xml(normal.element.get_or_add_rPr())

    def _font_xml(self, rpr):
        rf = rpr.find(qn("w:rFonts"))
        if rf is None:
            rf = OxmlElement("w:rFonts")
            rpr.append(rf)
        for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
            rf.set(qn(a), self.s["font"])

    def run(self, p, text, size=None, bold=False, italic=False, color=None):
        r = p.add_run(text)
        r.font.name = self.s["font"]
        r.font.size = Pt(size or self.s["body_size"])
        r.bold, r.italic = bold, italic
        if color is not None:
            r.font.color.rgb = color
        self._font_xml(r._element.get_or_add_rPr())
        return r

    def rich(self, p, text, size=None):
        for i, part in enumerate(text.split("**")):
            if part:
                self.run(p, part, size, bold=(i % 2 == 1))

    def para(self, align=None, before=0, after=0, keep_next=False):
        p = self.doc.add_paragraph()
        pf = p.paragraph_format
        pf.space_before, pf.space_after = Pt(before), Pt(after)
        pf.keep_together = True
        pf.keep_with_next = keep_next
        if align == "center":
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        return p

    def header(self, text):
        p = self.para(before=8, after=3, keep_next=True)
        self.run(p, text.upper(), 12, bold=True, color=self.accent)
        pbdr = OxmlElement("w:pBdr")
        b = OxmlElement("w:bottom")
        for k, v in (("w:val", "single"), ("w:sz", "8"), ("w:space", "1"), ("w:color", self.s["accent"])):
            b.set(qn(k), v)
        pbdr.append(b)
        p._p.get_or_add_pPr().append(pbdr)

    def bullet(self, text):
        p = self.para(after=3)
        p.paragraph_format.left_indent = Inches(0.25)
        p.paragraph_format.first_line_indent = Inches(-0.17)
        self.run(p, BULLET + "  ")
        self.rich(p, text)

    def entry(self, left, right, sub=None):
        p = self.para(before=5, keep_next=True)
        p.paragraph_format.tab_stops.add_tab_stop(self.width, WD_TAB_ALIGNMENT.RIGHT)
        self.run(p, left, 10.8, bold=True)
        if right:
            self.run(p, "\t" + right, 10.8, bold=True)
        if sub:
            lp = self.para(after=2, keep_next=True)
            self.run(lp, sub, 10.3, italic=True)

    def note_box(self, text):
        self.para(before=8)
        t = self.doc.add_table(rows=1, cols=1)
        cell = t.cell(0, 0)
        tcpr = cell._tc.get_or_add_tcPr()
        borders = OxmlElement("w:tcBorders")
        for side in ("top", "left", "bottom", "right"):
            el = OxmlElement(f"w:{side}")
            for k, v in (("w:val", "single"), ("w:sz", "10"), ("w:space", "0"), ("w:color", self.s["accent"])):
                el.set(qn(k), v)
            borders.append(el)
        tcpr.append(borders)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        self.run(p, text, 10.2, bold=True, color=self.accent)


def build(data: dict, out_path: str) -> str:
    """Render `data` (a merged profile) to `out_path` (.docx). Returns the path."""
    d = _Doc(data.get("style", {}))
    d.run(d.para("center", after=1, keep_next=True), data["name"].upper(), d.s["name_size"], bold=True)
    if data.get("headline"):
        d.run(d.para("center", after=1, keep_next=True), data["headline"].upper(), 12, bold=True, color=d.accent)
    contact = " | ".join(x for x in data.get("contact", []) if x)
    if contact:
        d.run(d.para("center", after=4), contact, 10.2)

    if data.get("summary"):
        d.header(data.get("summary_title", "Professional Summary"))
        for b in data["summary"]:
            d.bullet(b)

    if data.get("skills"):
        d.header("Skills")
        for cat, items in (data["skills"].items() if isinstance(data["skills"], dict) else data["skills"]):
            p = d.para(after=3)
            d.run(p, f"{cat}: ", bold=True)
            d.run(p, items if isinstance(items, str) else ", ".join(items))

    if data.get("certifications"):
        d.header("Certifications")
        for c in data["certifications"]:
            d.bullet(c)

    if data.get("experience"):
        d.header("Work Experience")
        for e in data["experience"]:
            d.entry(f"{e['company']} | {e['title']}", e.get("dates", ""), e.get("location"))
            for b in e.get("bullets", []):
                d.bullet(b)

    if data.get("education"):
        d.header("Education")
        for e in data["education"]:
            d.entry(f"{e['school']} | {e['degree']}", e.get("dates", ""), e.get("location"))

    for section in data.get("extra_sections", []):
        d.header(section["title"])
        for b in section.get("bullets", []):
            d.bullet(b)

    if data.get("note"):
        d.note_box(data["note"])

    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    d.doc.save(out_path)
    return out_path


def to_pdf(docx_path: str, out_dir: str | None = None) -> str:
    """Convert with headless LibreOffice. Returns the PDF path."""
    import subprocess
    out_dir = out_dir or os.path.dirname(os.path.abspath(docx_path))
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", out_dir, docx_path],
                   check=True, capture_output=True)
    return os.path.join(out_dir, os.path.splitext(os.path.basename(docx_path))[0] + ".pdf")


def build_from_files(profile: str, tailoring: str | None, out_path: str, pdf: bool = False) -> list[str]:
    data: dict[str, Any] = merge(load_file(profile), load_file(tailoring) if tailoring else None)
    paths = [build(data, out_path)]
    if pdf:
        paths.append(to_pdf(paths[0]))
    return paths
