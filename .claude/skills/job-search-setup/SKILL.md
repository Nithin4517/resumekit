---
name: job-search-setup
description: First-time setup for a job seeker using resumekit. Collects their details (or a sample resume, or 5 target job descriptions), builds 3 master resumes, sets up their folder, Gmail and dashboard, then hands off to tailoring. Use when someone says start, set me up, or has no profile yet.
---

# Job-search setup

Walk the person through six steps. Before starting, check which steps are already done
(profile exists? masters exist? dashboard exists? Gmail connected?) and skip those, saying so in
one line. Create a task list with the six steps so they can follow along.

Open with one short welcome, for example:

> Hi! I'll set up your job search in six quick steps: your details, three master resumes, a
> folder to keep everything, Gmail, your tracking dashboard, and then your first tailored
> resumes. Let's start.

---

## Step 1: Get their background

Ask how they'd like to start (use AskUserQuestion when available):

- **A. "I have a resume"**: ask them to attach it (PDF or Word). Read it and pull out
  everything below. Then show a short summary and ask them to fix anything wrong or missing.
- **B. "I'll answer questions"**: ask in small groups, waiting for answers between groups:
  1. Full name as it should appear, phone, email, city and state.
  2. The job title(s) they're aiming for.
  3. Each job, most recent first: company, their title, start and end month/year, city, and
     3 to 6 things they did there (tools used, numbers, results). Keep asking "anything else
     at this job?" until they say no.
  4. Education (school, degree, dates), and certifications they actually hold.
- **C. "I don't have much experience / not sure what to target"**: ask for their basics
  (group 1 above), then ask them to paste **5 job descriptions they'd like to get**. Use
  those to figure out target titles and the skills to ask about. Then ask about their
  experience against those skills (school projects, internships, part-time work, self-study
  labs all count, as long as they're real).

Then, whichever path, ask these job-preference questions. They're used for screening, never
printed on the resume:

- Work authorization: US citizen, green card, or a visa (and which)? Do they need sponsorship?
- Open to relocating? Where? Or remote / local only?
- Lowest pay they'd accept, for remote and for a relocation job.
- Any skills or tools they do **not** have and never want listed (these become lint rules).

Save everything to `profile/my_profile.yaml` in their folder (Step 3 creates the folder; until
then keep it in the working directory and move it over). Use `examples/profile.yaml` as the
shape. Put preferences under a `preferences:` key and the never-list under `never_claim:`.
Neither is printed.

## Step 2: Build three master resumes

Masters are complete, general resumes for their three likeliest lanes. Every tailored resume
starts from the closest master, which keeps tailoring fast and consistent.

1. Pick three lanes from their target titles and any job descriptions they shared, and confirm
   them in one line. The usual pattern:
   - **Master 1, main target:** the job they want most (for example Systems Administrator).
   - **Master 2, hybrid:** main target blended with the adjacent lane (for example Systems
     Administrator / IT Support).
   - **Master 3, safety lane:** the role they're most certain to land (for example IT
     Support Specialist or Help Desk).
2. For each master, write a tailoring file: headline, 4 to 6 summary bullets, skills grouped
   by category, and job titles and bullets re-ordered and re-worded for that lane. Use only
   what's in their profile. Bullets for past jobs start with past-tense verbs, and current-job
   bullets use present tense. Bold 1 to 3 key tools per bullet with `**double asterisks**`.
3. Lint, build and check each one:
   ```
   resumekit lint  profile/my_profile.yaml -t masters/master1.yaml -r profile/rules.yaml
   resumekit build profile/my_profile.yaml -t masters/master1.yaml -o masters/First_Last_Master1_<Lane>.docx --pdf
   resumekit check masters/First_Last_Master1_<Lane>.pdf --max-pages 2
   ```
   `profile/rules.yaml` holds their `never_claim` terms under `banned:`, plus word and bullet
   limits.
4. Look at page 1 of each PDF (render it to an image and view it) before showing them. Fix
   layout problems first.
5. Send the three PDFs and ask: *"Anything wrong or missing? These are the base for every
   resume I make you."* Apply corrections to the profile, not only to one master.

## Step 3: Set up their job-search folder

Ask them to make a folder on their computer and connect it to this chat:

> Please create a folder called **JobSearch** on your Desktop. Then, in the Claude desktop
> app, click **+** (or "Add folder") in this chat and pick that folder. Tell me when it's done.

Once connected, create this layout and move the profile and masters in:

```
JobSearch/
  profile/      my_profile.yaml, rules.yaml        (your details, private)
  masters/      the 3 master resumes + their tailoring files
  resumes/      every tailored resume (PDF + Word)
  jds/          job descriptions you pasted, one text file each
  Job_Dashboard.html                               (Step 5)
  dashboard_sync_checkpoint.json                   (Step 5)
```

If they can't connect a folder (they're on the web or phone), send the files in chat, tell them
to save them, and note that they'll need to re-attach `my_profile.yaml` in future chats.

## Step 4: Connect Gmail

The dashboard updates itself from application emails ("Your application was sent", interview
invites, rejections).

> Next, connect Gmail so I can track your applications: in Claude, open **Settings →
> Connectors**, find **Gmail**, and click **Connect**. Sign in with the email you apply from.
> Tell me when it's done.

Check by running one small Gmail search, for example applications from the last 3 days. If
they'd rather not connect Gmail, that's fine: they can tell you "applied to X" and you'll log
it by hand.

## Step 5: Create their dashboard

```
python3 dashboard/dashboard.py init <JobSearch folder>
```

This creates `Job_Dashboard.html` (a page that opens in any browser) and the sync checkpoint.
If Gmail is connected, offer to fill it with the last 30 days of applications: run the
update-dashboard skill in bootstrap mode. Tell them to double-click `Job_Dashboard.html` to
open it.

## Step 6: Find jobs and paste five job descriptions

> You're all set! Now let's find jobs. Go to **jobright.ai** (or LinkedIn or Indeed), search
> for your target titles, and open 5 jobs you like. Copy each **full job description**,
> including the company name, location and pay if shown, and paste them here, all five in one
> message if you like. I'll check each one against your preferences and build a tailored resume
> for every job that fits.

Then switch to the tailor-resume skill.

## Finish setup with a short recap

- What's ready: profile, 3 masters, folder, Gmail, dashboard.
- The two things to say from now on: **paste job descriptions** to get tailored resumes, and
  **"update dashboard"** to sync applications from Gmail.
