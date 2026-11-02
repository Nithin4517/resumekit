---
name: tailor-resume
description: Build tailored resumes from pasted job descriptions using the person's profile and master resumes. Screens each job against their preferences first, then builds, checks and saves the ones that pass. Use whenever job descriptions or job links are pasted.
---

# Tailor resumes from job descriptions

A pasted job description is an order to build. Don't ask "should I build this?". Screen it, then
build the ones that pass. Handle up to 5 or so per message, and make a task per job.

**Before starting**, load `profile/my_profile.yaml`, `profile/rules.yaml` and the three master
tailoring files from their folder. If there's no profile yet, run job-search-setup first.

## 1. Screen each job (fast, before building anything)

Skip a job, with a one-line reason, when any of these is true:

1. **Already applied:** run `python3 dashboard/dashboard.py check <folder>/Job_Dashboard.html "Company"`
   and also look in `resumes/` for that company. On DUPLICATE, skip. On REVIEW, look at the
   hit and decide.
2. **Location:** on-site or hybrid somewhere they won't relocate to.
3. **Pay below their floor:** judge by the top of the posted range, using the remote floor
   or the relocation floor as fits. No posted pay is not a reason to skip.
4. **Work authorization:** the posting excludes their status (for example "no sponsorship"
   when they need it, "US citizens only", "no OPT/CPT").
5. **Clearance:** it requires a security clearance they don't hold.
6. **A hard requirement they lack**, such as a required license, language, degree level,
   or years of experience far beyond theirs (3+ years over). "Preferred" items are not
   reasons to skip.
7. **Not a real fit:** the job is mostly in a field where they have no experience at all.

Report skips like: `Acme Corp: pass, requires active Secret clearance`.

## 2. Build each job that passes

1. Save the job description to `jds/<Company>.txt`.
2. Pick the closest master (main, hybrid or safety lane) and copy its tailoring file to a
   new file, `jds/<Company>.yaml`.
3. Tailor it:
   - **Headline and current-job title:** match the posting's title when it truthfully
     describes their work. Otherwise use the nearest honest title.
   - **Summary (4 to 6 bullets) and skills:** lead with what this job description stresses
     most. Use its exact wording for tools they really have ("Microsoft Entra ID", not
     "Azure AD", if that's the posting's term).
   - **Bullets:** re-order and re-word so the job description's main duties come first. Aim
     to cover about 90% of the posting's required skills that they actually have. Bold 1 to
     3 of the posting's keywords per bullet.
   - Past-job bullets in past tense, current-job bullets in present tense. No invented
     tools, numbers or duties. If the posting wants something they might have but haven't
     confirmed, **ask** before adding it, and add confirmed new skills to the profile so
     they're used next time.
4. Lint, build and check:
   ```
   resumekit lint  profile/my_profile.yaml -t jds/<Company>.yaml -r profile/rules.yaml
   resumekit build profile/my_profile.yaml -t jds/<Company>.yaml -o resumes/First_Last_Resume_<Company>.docx --pdf
   resumekit check resumes/First_Last_Resume_<Company>.pdf --max-pages 2
   ```
   Fix every lint and check problem, then rebuild. If they're open to relocating and the job
   is elsewhere, add `note: Open to relocating to <City, ST>` to the tailoring file.
5. View page 1 of the PDF as an image to confirm it looks right.
6. Save the PDF and Word file in their `resumes/` folder, and send the PDFs in chat too.

## 3. Report briefly

One block for the batch:

```
Built (3):
  Acme Corp: Systems Administrator, Dallas TX: 92% match: resumes/Jordan_Example_Resume_Acme.pdf
  ...
Skipped (2):
  Globex: pass, on-site in Seattle (not relocating there)
  ...
Next: apply, then say "update dashboard" (or "applied to Acme") and I'll log it.
```

The **match %** is the share of the posting's required skills and duties that the resume
covers. Be honest; don't round up.

Don't add dashboard rows here. A resume isn't an application. Rows are added once they've
applied (update-dashboard skill).
