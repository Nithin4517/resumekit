---
name: tailor-resume
description: Build tailored resumes from pasted job descriptions using the person's conditions, profile and master resumes. Screens each job through 10 gates first (duplicate, outside US, off-lane, field role, degree-related, pay, clearance/citizenship, student visa, hard requirement, match %), then builds, checks and saves only the ones that pass. Use whenever job descriptions or job links are pasted.
---

# Tailor resumes from job descriptions

**A pasted job description is a build order.** Don't ask "should I build this?". Screen it, then
build every one that passes. Handle up to ~5 per message, one task per job.

**Before starting**, load from their folder: `profile/conditions.yaml`, `profile/my_profile.yaml`,
`profile/rules.yaml` and the three `masters/master*.yaml`. **No conditions file → run Step 1 of
job-search-setup first** (the conditions questions). Don't screen without them.

**Screening questions are not a build order.** If they paste an application's questions ("Do you
have 3+ years of…?"), answer each Yes/No with a one- or two-line justification from their
profile. Don't rebuild anything.

---

## 1. Screen every job first (stop at the first gate it hits)

For each posting, save the text to `jds/<Company>.txt`, then run the mechanical check:

```
resumekit gate profile/conditions.yaml jds/<Company>.txt --where remote|near_home|relocation
```

`--where`: **remote** = fully remote US job; **near_home** = on-site/hybrid in their home
state/area; **relocation** = on-site or hybrid anywhere they'd have to move (including "hybrid,
occasional on-site" in another state). The tool prints red-flag phrases and the pay verdict.
**You** make the final call by reading the posting, using the rules below.

A skipped job gets **no resume, no draft, no file**: just one line naming the gate. A warning
under a built resume is never a substitute for a gate.

1. **Duplicate.** Already applied or already built:
   `python3 dashboard/dashboard.py check <folder>/Job_Dashboard.html "Company"` **and** look in
   `resumes/` for a file with that company in its name (the folder is the one record that's
   never behind). DUPLICATE → skip, say when it was built and its dashboard status. REVIEW →
   read the hit: match on the real employer, not a shared word ("Apex Systems" is not "Apex
   Companies"). A different job at the same employer is still a duplicate. Staffing agencies
   and different hotel properties under one brand are the exceptions.
   → `Acme: pass, already built Oct 12 (dashboard: Rejected)`
2. **Outside the US** (when `location.us_only`). Check the location line before anything else:
   global employers list every country together. A US-remote job (even restricted to some
   states) is fine; "remote, worldwide/EMEA" is not. → `pass, not in the US (Canada)`
3. **Off-lane.** The day-to-day work isn't in their target lanes, or it's in
   `target.skip_role_types` (sales, marketing, retail floor, commission "management training").
   A retail or consumer *employer* is fine if the job itself is in-lane. → `pass, not a match (sales role)`
4. **Field role** (when `field_roles_ok: false`). The normal day is away from an office: field
   service tech, install crews, driving between customer sites, MSP techs who "travel to client
   locations" with mileage. Supporting a few branches, an on-call rotation, or an on-site plant
   IT desk is NOT a field role. An outdoor "physical demands" block is the strongest tell.
   → `pass, field role, not corporate office`
5. **Not degree-related** (only when `degree_related_only: true`, i.e. CPT/OPT). Generous
   judgement call: most IT support, systems, cloud and ops roles carry enough process, vendor
   or coordination work to defend. Skip only pure hands-on break/fix (bench repair, device
   refurbishment, store-floor tech). → `pass, not degree-related`
6. **Pay below the floor.** Use the floor for where the job is: remote / near home / relocation.
   Judge on the **top of the posted range**; yearly ÷ 2,080. "Below" means under, not equal.
   **No posted pay is never a reason to skip**, and never guess a figure.
   → `pass, pay is less ($24-$29/hr; relocation needs $30+)`
7. **Clearance / citizenship / adjudicated background** (skip unless they hold it). Requires US
   citizenship, "US Person"/ITAR/EAR, any security clearance (including "able to obtain within
   N days"), public trust, or CJIS approval **as a condition of the offer**. NOT this gate: a
   duty about HIPAA/CJIS *compliance*, a routine background check, a state driver's license or
   occupational work card they can get, or "must live in <US city>" (that's just location).
   → `pass, requires active Secret clearance`
8. **Student-visa exclusion** (F-1 holders). "No OPT/CPT/F-1", "not considering STEM-OPT", or a
   "no sponsorship" line when `needs_sponsorship: true`. → `pass, excludes OPT/CPT`
9. **A hard required qualification they don't have**, only when marked *required*: a language,
   a license, a named certification they haven't earned (with no "or obtain within N months"),
   a degree they don't have, required years in an industry they've never worked in, or a
   `never_claim` tool stated flatly as required. NOT a gate: anything "preferred / a plus /
   nice to have", "or similar", hedged ("basic", "exposure to", "working knowledge"), a cert
   obtainable after hire, or a tool that's merely unfamiliar (bridge it, see gate 10). The
   **qualifications block beats** the responsibilities block and a generic skills list.
   → `pass, requires RHCSA (not held)`
10. **JD match below `target.min_match_percent`** (default 85). Score BEFORE building:
    list every line of the posting (each responsibility, required and preferred qualification,
    named tool). Score each: **covered = 1** (they verifiably have it), **bridged = 0.5**
    (nearest real equivalent, e.g. ServiceNow for Freshdesk, Entra ID for Okta), **gap = 0**.
    Required lines count **double**. Match % = weighted score ÷ weighted total, rounded.
    Score honestly: never round a bridge up or quietly claim an unconfirmed tool to clear the bar.
    → `pass, match is 72% (Splunk, Proxmox and Ansible required, only bridged)`

**Before skipping on gate 9 or 10, re-check `never_claim` and the profile**: the gap list shrinks
as they confirm new skills.

If they say "build it anyway" for one posting, build it (gates 1 to 9 still name the risk in one line).

## 2. Build each job that passed

1. Pick the closest master (main, hybrid, safety) and copy its tailoring file to `jds/<Company>.yaml`.
2. Tailor it:
   - **Titles follow the JD's lane**: set the headline and current-job title to the posting's
     title when it truthfully describes their work; otherwise the nearest honest title from
     their lanes.
   - **Summary (4 to 6 bullets) and skills**: lead with what the posting stresses most, in its
     exact words for tools they really have ("Microsoft Entra ID", not "Azure AD", if that's
     the posting's term).
   - **Cover the whole JD.** Every line from the gate-10 mapping gets a home: a bullet (best,
     and required for the main focus), a skills phrase, a summary bullet for soft lines
     ("work with minimal direction"), or an honest bridge. Merge two nearby lines into one
     bullet rather than dropping one. Only true gaps are left off, and each is reported.
   - **Bullets**: re-order so the posting's main duties come first; every past-job bullet starts
     with a **past-tense action verb**; current-job bullets present tense. Bold 1 to 3 of the
     posting's keywords per bullet.
   - **No invented tools, numbers or duties.** If the posting wants something they might have
     but haven't confirmed, **ask**. "I'm aware of it" or "I can handle it" is not experience:
     leave it off, say so, and ask if they've used it hands-on.
   - **Relocation note**: on-site/hybrid job outside their home state → add
     `note: Open to relocating to <City, ST>`. Fully remote or same-state → no note. If the
     posting has no city, use the state or leave it off; never guess a city.
3. Lint, build, check (fix every problem and rebuild):
   ```
   resumekit lint  profile/my_profile.yaml -t jds/<Company>.yaml -r profile/rules.yaml
   resumekit build profile/my_profile.yaml -t jds/<Company>.yaml -o resumes/First_Last_Resume_<Company>.docx --pdf
   resumekit check resumes/First_Last_Resume_<Company>.pdf --max-pages 2
   ```
   Filename is the company name only: no job title, no dates.
4. Render page 1 of the PDF to an image and look at it.
5. Save PDF + Word in `resumes/`, and send the PDFs in chat.

## 3. Closing reply (this shape, nothing else)

1. One line: how many built, how many skipped.
2. One check line: all 2 pages, word range, bold keywords on, relocation notes added where needed.
3. One table, one row per built resume:

   | Company | Match | Title used | Gaps not claimed |
   |---|---|---|---|
   | **Acme Corp** (Dallas TX, $32-38/hr) | 92% | Systems Administrator | **Ansible (required)**, bridged with PowerShell |

   Bold any gap that was **required**. Every row is at or above the match threshold.
4. Two or three short bullets: the strongest one or two (pay and fit), the weakest that still
   cleared, and the **biggest gap across the batch** with: "If you have hands-on <X>, tell me
   and I'll rebuild."
5. **Skipped**, one line each: `Company: pass, <gate reason>`.

No recap of steps, no file list (the file cards show them). Don't add dashboard rows here: a
resume isn't an application. Rows are added once they apply (update-dashboard skill).

## 4. When they correct you

- **They confirm a new skill** ("I do have Linux, 3 years"): add it to the profile (and remove it
  from `never_claim` / `rules.yaml`) right away. Rebuild **in the same turn**, without asking,
  every posting from this batch that was skipped or understated because of that gap.
- **They change a condition** ("relocation floor $32 now"): update `conditions.yaml`. It applies
  from the next batch; don't rebuild already-delivered resumes unless they ask.
- **They correct the shape** (summary length, titles, tense, filename, a line to remove): apply
  it to every resume in the current batch and all future ones; rebuild and resend the batch.
- **They correct ONE named resume** ("for Acme remove the relocation note"): change that file only.
- **A built resume turns out to be a duplicate or should have hit a gate**: tell them which file
  to discard, in one line. Don't rebuild the others.
- **Signs of a scam posting** (asks for money, bank details, check deposits, equipment purchases):
  warn them and don't build.
