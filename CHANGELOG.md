# Changelog

Every change to the workflow is logged here, newest first, so anyone who pulls the repo can see
what changed and why.

## 0.2.0 (2026-11-03)

**Conditions are asked first.** A new person is now asked their job conditions before any
resume work, in three short rounds:
1. Work permit (citizen / green card / F-1 CPT, OPT, STEM-OPT / H-1B), degree program for
   CPT/OPT, sponsorship, **security clearance**.
2. Home city, **remote** OK, **relocation** (anywhere / list / no), field jobs OK, US-only.
3. **Pay floors** (remote, near home, relocation), target titles, role types to skip,
   minimum JD match %, skills never to claim.

Answers are saved to `JobSearch/profile/conditions.yaml` (template: `examples/conditions.yaml`).

**10 screening gates** in the tailor skill (duplicate, outside US, off-lane, field role,
degree-related, pay, clearance/citizenship, student-visa exclusion, hard requirement, match %).
A job that fails a gate gets one line saying why, never a resume.

**Match % gate.** Each JD line is scored covered 1 / bridged 0.5 / gap 0, required lines
double. Below the person's minimum (default 85%) nothing is built.

**New command `resumekit gate`.** Pay floor check (top of range, yearly ÷ 2,080, no posted pay
never skips) and red-flag phrase scan, filtered to what applies to that person.

**Fixed closing reply**: one table per batch with Company / Match / Title / Gaps not claimed,
plus a skipped list with reasons.

**Correction rules**: a newly confirmed skill rebuilds affected postings in the same turn; a
changed condition applies from the next batch; a shape correction applies to the whole batch.

**GETTING_STARTED.md rewritten** as numbered steps for two setups: the Claude desktop app, or
`git clone` + Claude Code in a terminal.

## 0.1.0 (2026-11-02)

Initial release: build / lint / bold / check / screen, dashboard, setup and update-dashboard skills.
