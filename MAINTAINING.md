# Maintaining this repo (for the owner)

The rules in this repo are a cleaned-up, personal-data-free copy of the owner's own working
setup. When a rule changes there, it should change here too, so everyone who `git pull`s gets it.

## When you add or change a rule in your own project

Tell Claude, in a chat with this repo attached:

```
Sync my new rule to resumekit: <paste or describe the rule>
```

Claude should then:
1. **Generalize it.** Replace your personal facts (your name, employers, visa details, exact
   pay, past companies) with the person's `conditions.yaml` / profile fields. A rule like
   "skip under $30/hr if I must relocate" becomes "skip under `pay.floor_relocation`".
2. **Put it in the right place:**
   | Kind of rule | File |
   |---|---|
   | A question asked at setup | `.claude/skills/job-search-setup/SKILL.md` (+ `examples/conditions.yaml`) |
   | Skip / build decision on a job | `.claude/skills/tailor-resume/SKILL.md`, gates section |
   | Resume shape (titles, bullets, bold, filename) | `.claude/skills/tailor-resume/SKILL.md`, build section |
   | Dashboard / Gmail | `.claude/skills/update-dashboard/SKILL.md` |
   | Something a script can check | `resumekit/*.py` + a test in `tests/` |
3. **Log it** at the top of `CHANGELOG.md` with the date and one line on why.
4. **Run the tests:** `pip install -e .[dev] && pytest`
5. **Commit and push** with a message that says what changed.

## Never commit

Resumes, profiles, conditions, job descriptions, the dashboard, or anything with a real name,
phone, email or employer. `.gitignore` blocks the usual paths; still check `git status` before
committing.

## Your friends get updates by

```
cd ~/Desktop/resumekit && git pull
```
(Way 1 users get them automatically: Claude reads the latest repo each new chat.)
