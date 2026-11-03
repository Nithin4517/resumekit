---
name: next-batch
description: Find jobs on JobRight AI and build 5 tailored resumes with apply links, with no job descriptions pasted. Use when the person says "give me first batch", "give me next batch", "next batch", or "find me jobs".
---

# "Give me first batch" / "Give me next batch": 5 resumes from JobRight

The person doesn't paste anything. You find the jobs, screen them, and deliver **5 built
resumes plus their apply links**. Don't ask questions mid-run; just run it end to end.

**Before starting:** load `profile/conditions.yaml`, `profile/my_profile.yaml`,
`profile/rules.yaml`, the three masters, and `batch_state.json` from their JobSearch folder.
No conditions file → run Step 1 of job-search-setup first. No masters → finish setup first.

For the screening and the build itself, **follow `.claude/skills/tailor-resume/SKILL.md`
exactly**: the 10 gates, Match % at or above `target.min_match_percent`, titles, lint, build,
check, file names and the closing reply. This skill only adds *where the jobs come from*.

## Batch settings (in `conditions.yaml`, defaults shown)

```yaml
batch:
  size: 5                    # resumes per batch
  source: jobright           # jobright.ai
  company_site_only: true    # skip postings whose Apply goes to LinkedIn or Indeed
  max_age_hours: 24          # prefer postings from the last day
```

## Batch memory: `batch_state.json` in their JobSearch folder

```json
{"batch_number": 3, "query_index": 7, "seen_job_ids": ["abc123", "..."],
 "held": [{"company": "Acme", "title": "Systems Administrator", "job_id": "xyz", "match": 91}]}
```

- **"first batch"**: start with `batch_number: 1`, `query_index: 0`, empty lists (create the file
  if missing; if it exists, ask once whether to start over or continue as the next batch).
- **"next batch"**: build any `held` postings first, then continue from `query_index`.
- Skip every job id in `seen_job_ids`. After the batch, add every job looked at (built or
  skipped), advance `query_index`, increment `batch_number`, and save.

## Steps

1. **Open JobRight in a browser.** Use whichever browser tool this session has (Claude in
   Chrome or the built-in browser; load its skill first). Open **jobright.ai**. Job data loads
   without signing in. If no browser is available, say so in one line and ask them to paste up
   to 5 job descriptions instead (then use the tailor-resume skill).
2. **Search.** Build the query list from `target.lanes` plus close variants (for a Systems
   Administrator lane: Systems Administrator, IT Systems Administrator, Infrastructure
   Administrator, Microsoft 365 Administrator...; for IT Support: IT Support Specialist, Desktop
   Support, Service Desk Analyst, Help Desk Analyst, IT Support Technician...). Rotate through the
   list using `query_index`, so batches don't repeat. With the browser's JavaScript tool:
   `fetch('/jobs/search?value=<query>')`, then parse `<script id="__NEXT_DATA__">` →
   `props.pageProps.jobList` (each item has `jobResult` and `companyResult`). Prefer postings
   newer than `max_age_hours`.
3. **Pre-filter from the list** (cheap, before opening details): drop clearance, defense or
   cleared-government titles (unless they hold one); stated pay under their floor; roles
   asking far more years than they have; off-lane roles (sales, `skip_role_types`, specialist
   platforms they don't have such as ERP/HRIS/EHR); job ids already in `seen_job_ids`.
4. **Duplicate check in one call:**
   `python3 dashboard/dashboard.py check <folder>/Job_Dashboard.html "Co1" "Co2" ...`, and look
   for each company in `resumes/`. Read every DUPLICATE and REVIEW hit; false positives happen.
5. **Open details for the survivors** in one JavaScript call: `fetch('/jobs/info/<jobId>')` →
   `__NEXT_DATA__` → `props.pageProps.dataSource.jobResult`. Read `isCompanySiteLink`,
   `jobLocation`, `workModel`, `salaryDesc`, `isCitizenOnly`, `isClearanceRequired`,
   `jobSummary`, `coreResponsibilities`, `qualifications.mustHave`,
   `qualifications.preferredHave`. Wrap each in try/catch; skip a page whose `dataSource` is null.
   - `company_site_only: true` → keep only `isCompanySiteLink = true` (Apply goes to the
     company's own site, not LinkedIn or Indeed).
   - Save each posting's text to `jds/<Company>.txt` and run
     `resumekit gate profile/conditions.yaml jds/<Company>.txt --where ...` like any pasted job.
6. **Run the 10 gates and score Match %** (tailor-resume skill). Keep pulling more queries
   until **`batch.size` postings clear**. If more clear than needed, keep the best and put the
   rest in `held` for next time.
7. **Build** the cleared postings exactly as the tailor-resume skill says (lint, build, check,
   view page 1). Save to `resumes/`, send the PDFs in chat.
8. **Reply** with the tailor-resume closing reply (opening line, check line, Match % table,
   2 to 3 bullets), then:
   - **Apply links**, one per built resume: `Company: https://jobright.ai/jobs/info/<jobId>`
   - **Held for next batch** (if any), with links
   - **Skipped**, one line each with the gate reason
   - Last line: *"After you apply, say **update dashboard**. Say **next batch** for 5 more."*
9. Update and save `batch_state.json`.

## Notes

- If fewer than `batch.size` clear after ~8 queries, deliver what cleared and say why the rest
  failed (most common gate first), so they can loosen a condition if they want.
- The gaps that sink the most postings belong in the "biggest gap" bullet, with the offer to
  rebuild if they actually have that skill.
