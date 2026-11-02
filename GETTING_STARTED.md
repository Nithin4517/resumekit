# Getting started (no coding needed)

Claude walks you through everything. You answer questions and paste job descriptions; Claude
builds your resumes and keeps a dashboard of your applications.

## What you need

- A **Claude** account, using the **Claude desktop app** (best, because it can save files to a
  folder on your computer).
- A **Gmail** account you apply to jobs from (optional, but it makes the dashboard automatic).
- About **20 minutes** for the first setup.

## 1. Start a chat and paste this

Open Claude, start a new chat, and paste:

```
Set me up for my job search using github.com/Nithin4517/resumekit
```

If Claude asks to connect GitHub, follow the prompt; it only needs to read this public project.

## 2. Answer Claude's questions

Claude asks how you want to start:

| Option | Choose it if |
|---|---|
| **Upload my resume** | You already have a resume (PDF or Word) |
| **Answer questions** | No resume handy; Claude asks about your jobs, dates and duties |
| **Paste 5 job descriptions** | You're new or unsure what to target; Claude works backward from jobs you want |

It also asks about work authorization, relocation, minimum pay, and skills you **don't** have
(so they never end up on a resume).

## 3. Review your 3 master resumes

Claude builds three base resumes, one per job lane, for example:

1. **Main target:** the job you want most
2. **Hybrid:** main target plus a related role
3. **Safety lane:** the role you're most sure to land

Tell Claude anything that's wrong. Every future resume is built from these.

## 4. Make your folder

Create a folder called **JobSearch** on your Desktop, then in the Claude desktop app click
**+ / Add folder** in the chat and pick it. Claude organizes it like this:

```
JobSearch/
  profile/    your details (private)
  masters/    your 3 master resumes
  resumes/    every tailored resume
  jds/        job descriptions you pasted
  Job_Dashboard.html
```

## 5. Connect Gmail

In Claude: **Settings → Connectors → Gmail → Connect**. Claude uses it only to read
application emails (confirmations, interviews, rejections) for your dashboard.

## 6. Find jobs and paste them

Go to **[jobright.ai](https://jobright.ai)**, LinkedIn or Indeed, open jobs you like, copy the
**full job description**, and paste up to 5 at a time into the chat.

For each job, Claude:
- skips it if you already applied, it pays too little, it's somewhere you won't move, or it
  needs something you don't have, and tells you why
- builds a tailored resume for every job that fits and shows the match %
- saves it to `JobSearch/resumes/`

## Every day after that

| Say this | What happens |
|---|---|
| *(paste job descriptions)* | Tailored resumes for the ones that fit |
| **update dashboard** | Claude reads new application emails and updates your dashboard |
| **applied to Acme, Systems Admin, Dallas** | Logs one application by hand |

Double-click **Job_Dashboard.html** to see every application, with interviews, assessments and
rejections color-coded.

## Privacy

Your details, resumes and dashboard stay in **your** folder. Nothing is uploaded to this
GitHub project.
