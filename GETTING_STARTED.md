# Getting started (step by step, no coding needed)

You answer a few questions and paste job descriptions. Claude screens every job against **your
conditions** (work permit, clearance, pay, location), builds tailored resumes only for the
jobs you can actually take, and keeps a dashboard of your applications.

Pick **one** of the two ways below. **Way 1 is easiest.** Way 2 is for people who already use
git and a terminal.

---

## What you need (both ways)

- A **Claude** account (Pro or higher works best for long sessions).
- A **GitHub** account (free) so Claude can read this project.
- A **Gmail** you apply to jobs from (optional, makes the dashboard automatic).
- About **25 minutes** for the first setup.

---

## Way 1: Claude desktop app (recommended)

### Step 1. Install the Claude desktop app
Download it from **claude.ai/download**, install it, and sign in.

### Step 2. Make your JobSearch folder
On your **Desktop**, create a new folder named **`JobSearch`**. Everything Claude makes for you
(resumes, dashboard, your answers) is saved here, on your computer only.

### Step 3. Start a new chat and add the folder
1. Open the Claude app and start a **new chat**.
2. Click **+** (or **Add folder**) in the chat box and pick your **`JobSearch`** folder.

### Step 4. Paste this exact message
```
Set me up for my job search using github.com/Nithin4517/resumekit
```
If Claude asks to connect GitHub, click allow. It only needs to read this public project.

### Step 5. Answer the condition questions (3 short rounds)
Claude asks these **before it builds anything**. You click an answer or type your own.

| Round | Questions |
|---|---|
| **1. Work permit & clearance** | US citizen / green card / F-1 (CPT, OPT, STEM-OPT) / H-1B? Your degree program (for CPT/OPT). Need sponsorship? Security clearance: none, public trust, Secret, Top Secret? |
| **2. Location & work style** | Your city and state. Remote OK? Will you relocate (anywhere / certain cities / no)? Field jobs (driving to customer sites) OK? US jobs only? |
| **3. Pay & targets** | Lowest pay for a remote job, a job near home, and a job you'd move for. Job titles you want (best first). Role types to never apply to (e.g. sales). Minimum match % (default 85%). Skills you **don't** have. |

Claude shows a summary table of your answers. Fix anything wrong. You can change any answer
later just by saying it, for example **"change my relocation pay to $32/hr"**.

### Step 6. Give your background
Pick one:
- **Upload your resume** (PDF or Word), or
- **Answer questions** about your jobs, dates and duties, or
- **Paste 5 job descriptions** you'd like, if you're new or unsure what to target.

### Step 7. Check your 3 master resumes
Claude builds three base resumes: **main target**, **hybrid**, **safety lane**. Read them and
tell Claude anything wrong. Every future resume is built from these.

### Step 8. Connect Gmail (optional but recommended)
In Claude: **Settings → Connectors → Gmail → Connect**, sign in with the email you apply from.

### Step 9. Paste jobs
Go to **jobright.ai**, LinkedIn or Indeed. Copy the **full job description** (with company,
location and pay) of up to 5 jobs and paste them into the chat.

For each job, Claude either:
- **skips it with one line saying why**, e.g. `Acme: pass, requires Secret clearance`,
  `Globex: pass, pay is less ($24/hr; relocation needs $30+)`, `Initech: pass, match is 72%`, or
- **builds a tailored resume**, shows its match %, and saves it in `JobSearch/resumes/`.

---

## Way 2: Git + Claude Code in a terminal

### Step 1. Install the tools (one time)
- **Git**: Mac: open Terminal and run `git --version` (it offers to install). Windows: install
  from git-scm.com.
- **Python 3.9+**: python.org/downloads (Mac usually has it: `python3 --version`).
- **Claude Code**:
  - Mac / Linux: `curl -fsSL https://claude.ai/install.sh | bash`
  - Windows (PowerShell): `irm https://claude.ai/install.ps1 | iex`
- **LibreOffice** (turns Word resumes into PDFs): libreoffice.org/download

### Step 2. Download the project
```
cd ~/Desktop
git clone https://github.com/Nithin4517/resumekit.git
cd resumekit
pip3 install -e .
```

### Step 3. Make your JobSearch folder
```
mkdir -p ~/Desktop/JobSearch
```

### Step 4. Start Claude inside the project
```
claude
```
Sign in when asked. Claude reads this project's `CLAUDE.md` automatically.

### Step 5. Paste this
```
Set me up. My JobSearch folder is ~/Desktop/JobSearch
```
Then follow **Steps 5 to 9 of Way 1** (conditions questions, background, masters, Gmail, jobs).

### Getting updates later
```
cd ~/Desktop/resumekit
git pull
```
Your own files are in `~/Desktop/JobSearch`, so pulling never touches them.

---

## Every day after setup

| Say this | What happens |
|---|---|
| *(paste job descriptions)* | Screened against your conditions; resumes for the ones that fit |
| **update dashboard** | Reads new application emails and updates your dashboard |
| **applied to Acme, Systems Admin, Dallas** | Logs one application by hand |
| **change my remote pay to $28/hr** | Updates a condition |
| **I do have Ansible, 2 years at Acme** | Adds the skill and rebuilds any job it was missing from |

Double-click **`JobSearch/Job_Dashboard.html`** to see every application, color-coded by status.

## How Claude decides to skip a job (the 10 gates)

1. Already applied / already built
2. Job is outside the US
3. Not your kind of role (e.g. sales, marketing)
4. Field job when you want an office
5. Not related to your degree (only for CPT/OPT)
6. Pay below your floor (judged on the top of the posted range; no pay listed is never skipped)
7. Needs a clearance, US citizenship, ITAR, or similar you don't have
8. Excludes your visa type (e.g. "no OPT/CPT")
9. A *required* license/cert/language you don't hold ("preferred" never counts)
10. Resume would match the job less than your minimum (default 85%)

## Privacy

Your answers, resumes and dashboard stay in **your** JobSearch folder. Nothing you enter is
uploaded to this GitHub project.

## Something went wrong?

| Problem | Fix |
|---|---|
| Claude didn't ask the condition questions | Say: **"Ask me my job conditions first"** |
| Claude can't save files | Make sure the `JobSearch` folder is added to the chat (Way 1, Step 3) |
| New chat forgot everything | Add the `JobSearch` folder again and say **"continue my job search"**. Your answers are saved in `JobSearch/profile/` |
| PDFs not created (Way 2) | Install LibreOffice and restart the terminal |
