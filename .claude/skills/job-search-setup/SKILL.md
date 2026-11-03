---
name: job-search-setup
description: First-time setup for a job seeker using resumekit. Asks their job conditions FIRST (work authorization, security clearance, pay floors, location, remote/relocation), then their background, builds 3 master resumes, sets up their folder, Gmail and dashboard, and hands off to tailoring. Use when someone says start, set me up, or has no conditions/profile yet.
---

# Job-search setup

Seven steps. Before starting, check what already exists in their JobSearch folder and skip
finished steps, saying so in one line:

| Step | Done when this exists |
|---|---|
| 1. Conditions | `profile/conditions.yaml` |
| 2. Background | `profile/my_profile.yaml` |
| 3. Master resumes | `masters/*Master1*.pdf`, `*Master2*`, `*Master3*` |
| 4. Folder | the JobSearch folder is connected to this chat |
| 5. Gmail | a Gmail search tool works |
| 6. Dashboard | `Job_Dashboard.html` |
| 7. First jobs | (always offered) |

If no folder is connected yet, do Step 4 (folder) **first**, so every answer is saved straight
to their computer. If they can't connect one, keep files in the working directory and send them
at the end.

Create a task list with the seven steps. Open with one short welcome:

> Hi! I'll set up your job search in seven quick steps. First, a few questions about **your
> conditions** (work permit, clearance, pay, location) so I never build a resume for a job you
> can't take. Then your background, three master resumes, your folder, Gmail, a tracking
> dashboard, and your first tailored resumes.

---

## Step 1: Job conditions (ALWAYS FIRST, before any resume work)

These decide which jobs get skipped. Ask them with AskUserQuestion (multiple choice, they can
type their own answer). Ask in **three short rounds**, waiting for answers between rounds.
Never skip this step, even if they paste a resume or job descriptions straight away: say
"Before I build anything, 3 quick rounds of questions so I skip jobs you can't take."

**Round 1: work permit and clearance**

1. *Work authorization:* US citizen / Green card / F-1 student (CPT, OPT or STEM-OPT) / H-1B
   or other visa. If F-1, ask which (Day 1 CPT, CPT, OPT, STEM-OPT) and, for CPT/OPT, the
   **degree program they're enrolled in or graduated from** (the job must relate to it).
2. *Need visa sponsorship now or later?* Yes / No.
3. *Security clearance:* None / Public Trust / Secret / Top Secret / TS/SCI.
   With **None**, every job that requires a clearance, US citizenship, "US Person"/ITAR, or
   an adjudicated background (CJIS, public trust) as a condition of the offer is skipped.

**Round 2: location and work style**

4. *Where do you live?* City and state.
5. *Remote jobs OK?* Yes / Remote only / No.
6. *Will you relocate?* Anywhere in the US / Only to certain cities (ask which) / No, stay local.
7. *Field jobs OK?* (driving between customer sites, field tech, install crews) Yes / No,
   office only.
8. *US jobs only?* Default yes. (A visa holder usually can't take a job based abroad.)

**Round 3: pay and targets**

9. *Lowest pay you'd accept,* hourly or yearly, for: a **remote** job, a job **near home**,
   and a job you'd **move for**. (Suggest the relocation floor be higher; moving costs money.)
   Tell them: "I judge against the top of the posted range, and a job with no pay listed is
   never skipped for pay."
10. *Job titles you're aiming for,* best first (these become the 3 master resumes).
11. *Role types to never build for* (default: sales, marketing, retail floor).
12. *Minimum JD match to build a resume.* Default **85%**: below that, Claude says why and
    builds nothing. They may pick 75%, 80%, 85% or 90%.
13. *Tools, skills or certifications you DON'T have* and never want on a resume.

Save the answers to `profile/conditions.yaml` using `examples/conditions.yaml` as the exact
shape (pay as `25/hr` or `60000/yr`). Then show a short recap table and ask "Anything to
change?" Example:

| Condition | Your answer |
|---|---|
| Work permit | F-1, Day 1 CPT (MBA): job must relate to business/IT operations |
| Clearance | None: skip clearance / citizen-only jobs |
| Location | Springfield IL: remote OK, relocate anywhere in US, no field jobs |
| Pay floor | Remote $25/hr, near home $25/hr, relocation $30/hr |
| Targets | Systems Administrator, SysAdmin/IT Support, IT Support Specialist |
| Build only if match is | 85%+ |

They can change any answer later ("change my relocation floor to $32"): update the file and
confirm in one line.

If they are on F-1 CPT/OPT, say **once** (not every turn) that their school's DSO decides
whether a job counts as related to their degree, and an immigration attorney is worth asking.

## Step 2: Get their background

Ask how they'd like to start (AskUserQuestion):

- **A. "I have a resume"**: ask them to attach it (PDF or Word). Read it and pull out
  everything below. Show a short summary and ask them to fix anything wrong or missing.
- **B. "I'll answer questions"**: ask in small groups, waiting between groups:
  1. Full name as it should appear, phone, email, city and state.
  2. Each job, most recent first: company, title, start and end month/year, city, and 3 to 6
     things they did there (tools used, numbers, results). Keep asking "anything else at this
     job?" until they say no.
  3. Education (school, degree, dates), and certifications they actually hold.
- **C. "Not much experience / not sure what to target"**: take their basics, then ask them to
  paste **5 job descriptions they'd like to get**. Use those to pick target titles and the
  skills to ask about, then ask about their real experience against those skills (school
  projects, internships, part-time work and home labs all count, as long as they're real).

Save to `profile/my_profile.yaml` (shape: `examples/profile.yaml`). Copy `never_claim` from the
conditions into the profile, and write `profile/rules.yaml` (shape: `examples/rules.yaml`) with
each never-claim item as a `banned:` regex.

## Step 3: Build three master resumes

Masters are complete, general resumes for their three lanes from `conditions.yaml →
target.lanes`. Every tailored resume starts from the closest master.

1. Confirm the three lanes in one line. Usual pattern:
   - **Master 1, main target** (e.g. Systems Administrator)
   - **Master 2, hybrid** (main target + adjacent lane, e.g. Systems Administrator / IT Support)
   - **Master 3, safety lane** (the role they're surest to land, e.g. IT Support Specialist)
2. For each, write a tailoring file `masters/master1.yaml` etc.: headline, 4 to 6 summary
   bullets, skills grouped by category, job titles and bullets re-ordered and re-worded for
   that lane. Only what's in their profile. **Every past-job bullet starts with a past-tense
   action verb**; current-job bullets use present tense. Bold 1 to 3 key tools per bullet with
   `**double asterisks**`.
3. Lint, build and check:
   ```
   resumekit lint  profile/my_profile.yaml -t masters/master1.yaml -r profile/rules.yaml
   resumekit build profile/my_profile.yaml -t masters/master1.yaml -o masters/First_Last_Master1_<Lane>.docx --pdf
   resumekit check masters/First_Last_Master1_<Lane>.pdf --max-pages 2
   ```
4. Render page 1 of each PDF to an image and look at it before showing them. Fix layout first.
5. Send the three PDFs: *"Anything wrong or missing? Every resume I make you starts from
   these."* Put corrections in the profile, not only in one master.

## Step 4: Their JobSearch folder

> Please create a folder called **JobSearch** on your Desktop. Then, in the Claude desktop
> app, click **+** (or "Add folder") in this chat and pick that folder. Tell me when it's done.

Once connected, create:

```
JobSearch/
  profile/      conditions.yaml, my_profile.yaml, rules.yaml   (private)
  masters/      3 master resumes + their tailoring files
  resumes/      every tailored resume (PDF + Word)
  jds/          job descriptions you pasted, one .txt + one .yaml each
  Job_Dashboard.html
  dashboard_sync_checkpoint.json
```

If they can't connect a folder (web or phone), send files in chat and tell them to re-attach
`conditions.yaml` and `my_profile.yaml` in future chats.

## Step 5: Connect Gmail

> Next, connect Gmail so I can track your applications: in Claude open **Settings →
> Connectors**, find **Gmail**, click **Connect**, and sign in with the email you apply from.
> Tell me when it's done.

Check with one small search (applications from the last 3 days). If they'd rather not, they
can say "applied to X" and you log it by hand.

## Step 6: Create the dashboard

```
python3 dashboard/dashboard.py init <JobSearch folder>
```

If Gmail is connected, offer to fill it with the last 30 days (update-dashboard skill,
bootstrap mode). Tell them to double-click `Job_Dashboard.html` to open it.

## Step 7: First jobs

> You're all set! Go to **jobright.ai**, LinkedIn or Indeed, search your target titles, and
> open up to 5 jobs. Copy each **full job description** (company, location and pay included)
> and paste them here. I'll check each against your conditions and build a resume for every
> one that fits.

Then switch to the tailor-resume skill.

## Finish with a short recap

- Ready: conditions, profile, 3 masters, folder, Gmail, dashboard.
- From now on: **paste job descriptions** for tailored resumes, **"update dashboard"** to sync
  from Gmail, **"change my <condition>"** to update a condition.
