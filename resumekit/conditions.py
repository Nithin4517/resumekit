"""Job-condition gates: pay floor and red-flag phrases in a job description.

These are the mechanical checks. Claude still reads the whole posting and makes the
final call (a "preferred" item is never a gate, an obtainable license is not a clearance).
"""
from __future__ import annotations

import re

HOURS_PER_YEAR = 2080

# (gate name, regex) - case-insensitive. Each hit is a flag for Claude to confirm.
FLAGS = {
    "clearance": [
        r"\b(active|current|secret|top secret|ts/sci|ts-sci|public trust)\b[^.\n]{0,40}\bclearance\b",
        r"\bclearance\b[^.\n]{0,40}\b(required|must|prerequisite)\b",
        r"\b(able|ability) to obtain[^.\n]{0,40}\bclearance\b",
        r"\bts/sci\b",
        r"\bcjis\b[^.\n]{0,60}\b(approval|cleared|prerequisite)\b",
    ],
    "citizenship": [
        r"\b(must be|requires?|only)\b[^.\n]{0,20}\bu\.?s\.? citizens?(hip)?\b",
        r"\bu\.?s\.? citizens? only\b",
        r"\bus person\b",
        r"\bitar\b",
        r"\bexport[- ]control",
    ],
    "sponsorship": [
        r"\b(no|not|unable to|cannot|will not|won't)\b[^.\n]{0,40}\bsponsor",
        r"\bsponsorship (is )?not (available|provided|offered)\b",
        r"\bwithout (the need for )?(current or future )?sponsorship\b",
    ],
    "student_visa": [
        r"\b(no|not|unable to|cannot|will not)\b[^.\n]{0,40}\b(opt|cpt|f-?1|stem[- ]opt)\b",
        r"\b(opt|cpt|f-?1)\b[^.\n]{0,40}\b(not eligible|ineligible|not considered)\b",
    ],
    "internal_only": [
        r"\binternal (candidates|applicants) only\b",
        r"\bcurrent employees only\b",
        r"\binternal only\b",
    ],
    "field_role": [
        r"\bfield (service )?(technician|engineer|tech)\b",
        r"\btravel to (customer|client) (sites|locations|premises)\b",
        r"\bmileage reimbursement\b",
        r"\bexposure to (extreme )?outdoor weather\b",
    ],
}

_NUM = r"\$?\s*(\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?)\s*([kK])?"
_RANGE = re.compile(_NUM + r"(?:\s*(?:-|–|—|to)\s*" + _NUM + r")?\s*(/\s*(?:hr|hour)|per hour|an hour|hourly|/\s*(?:yr|year)|per year|a year|annually|k\b)?",
                    re.I)


def _to_float(num: str, k: str | None) -> float:
    v = float(num.replace(",", ""))
    return v * 1000 if k else v


def parse_pay(text: str) -> float | None:
    """Return the TOP of the posted pay as an hourly figure, or None if no pay is found.

    Handles "$26-$29/hr", "$55,000 - $60,000", "70k-80k", "$25.00 per hour".
    Numbers under 200 are treated as hourly, 10,000+ as yearly; anything else is ignored.
    """
    best = None
    for m in _RANGE.finditer(text):
        lo = _to_float(m.group(1), m.group(2))
        hi = _to_float(m.group(3), m.group(4)) if m.group(3) else lo
        if (m.group(2) or m.group(4)) and not m.group(3):
            hi = lo
        unit = (m.group(5) or "").lower()
        has_dollar = "$" in m.group(0)
        if not (has_dollar or unit):
            continue
        top = max(lo, hi)
        if "h" in unit or (not unit and 7 <= top < 200):
            hourly = top
        elif top >= 10_000:
            hourly = top / HOURS_PER_YEAR
        else:
            continue
        if 7 <= hourly < 500:
            best = max(best or 0, hourly)
    return round(best, 2) if best else None


def floor_for(conditions: dict, where: str) -> float:
    """where: remote | near_home | relocation"""
    pay = conditions.get("pay", {})
    raw = str(pay.get(f"floor_{where}", "0"))
    m = re.search(r"[\d,.]+", raw)
    v = float(m.group(0).replace(",", "")) if m else 0.0
    return v / HOURS_PER_YEAR if v >= 1000 else v


def pay_gate(conditions: dict, pay_text: str, where: str) -> dict:
    top = parse_pay(pay_text)
    floor = floor_for(conditions, where)
    if top is None:
        return {"verdict": "PASS", "reason": "no pay listed (never a reason to skip)", "top": None, "floor": floor}
    ok = top >= floor
    return {
        "verdict": "PASS" if ok else "SKIP",
        "reason": f"top of range ${top:.2f}/hr vs {where} floor ${floor:.2f}/hr" + ("" if ok else " - pay is less"),
        "top": top, "floor": floor,
    }


def scan_jd(text: str, conditions: dict | None = None) -> dict:
    """Find red-flag phrases. Returns {gate: [matched snippets]}; only gates that apply to
    this person are reported (a US citizen with a clearance gets no clearance flags)."""
    c = conditions or {}
    auth = c.get("work_authorization", {})
    status = str(auth.get("status", "")).lower()
    held = str(c.get("security_clearance", {}).get("held", "none")).lower()
    loc = c.get("location", {})
    skip = set()
    if held not in ("", "none"):
        skip.add("clearance")
    if status == "us_citizen":
        skip.update({"citizenship", "sponsorship", "student_visa"})
    elif status in ("green_card", "ead"):
        skip.update({"sponsorship", "student_visa"})
    elif not auth.get("needs_sponsorship") and not status.startswith("f1"):
        skip.add("sponsorship")
    if status and not status.startswith("f1"):
        skip.add("student_visa")
    if loc.get("field_roles_ok"):
        skip.add("field_role")

    out = {}
    low = text.lower()
    for gate, pats in FLAGS.items():
        if gate in skip:
            continue
        hits = []
        for p in pats:
            for m in re.finditer(p, low):
                a, b = max(0, m.start() - 30), min(len(text), m.end() + 30)
                hits.append(" ".join(text[a:b].split()))
        if hits:
            out[gate] = sorted(set(hits))[:3]
    return out
