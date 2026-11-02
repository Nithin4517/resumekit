# resumekit

Tailor, build and check ATS-friendly `.docx` resumes from a single YAML profile.

Applying to many jobs means making many slightly different resumes. `resumekit` keeps your
real history in one profile file, lets you write small per-job override files, and catches the
mistakes that slip in when you're on resume number forty:

- **build**: render a clean, single-column, ATS-readable `.docx` (and PDF via LibreOffice)
- **lint**: refuse to build if the content mentions tools or certifications you've banned, uses
  present tense for past jobs, or is too long/short
- **bold**: bold job-description keywords inside bullets (capped per bullet, so it stays readable)
- **check**: inspect the rendered PDF for orphaned headers, split bullets, page overflow and
  an underfilled last page
- **screen**: before tailoring, check whether you've already applied to that company, with
  rarity-ranked fuzzy matching so "Credit Union" doesn't flag every credit union

![Example output](docs/example.png)

## Install

```bash
pip install git+https://github.com/Nithin4517/resumekit.git
```

PDF conversion needs [LibreOffice](https://www.libreoffice.org/) (`soffice` on your PATH).

## Quick start

```bash
cp examples/profile.yaml my_profile.yaml        # my_*.yaml is gitignored
resumekit lint  my_profile.yaml -r examples/rules.yaml
resumekit build my_profile.yaml -t examples/tailor_cloud_role.yaml -o out/Resume_Acme.docx --pdf
resumekit check out/Resume_Acme.pdf --max-pages 2
```

### Profile

```yaml
name: Jordan Example
headline: Systems Administrator
contact: ["(555) 010-0000", jordan.example@example.com, Springfield, USA]
summary:
  - "Comfortable administering **Active Directory** and **Intune** ..."   # **x** = bold
skills:
  Identity & Access: Active Directory, Microsoft Entra ID
certifications: [ ... ]
experience:
  - company: Acme Corp
    title: Systems Administrator
    dates: Jan 2022 – Present
    location: Springfield, USA
    bullets: [ ... ]
education:
  - {school: State University, degree: B.S. in IT, dates: 2015 – 2019}
note: Open to relocating          # optional boxed line at the bottom
style: {font: Calibri, accent: 1F4E79}
```

### Per-job tailoring

A tailoring file overrides only what changes. Experience entries are matched by company:

```yaml
headline: Cloud Administrator
summary: [ ... ]                 # replace the summary for this job
experience:
  Acme Corp:
    title: Cloud Administrator
    bullets: [ ... ]
```

### Lint rules

```yaml
banned: ['\bSCCM\b', 'Security\+']   # regexes, case-insensitive
min_words: 450
max_words: 1100
summary_bullets: [4, 6]
bullets_per_role: [3, 8]
require_past_tense: true             # roles whose dates don't say "Present"
```

`resumekit build ... -r rules.yaml` refuses to build when lint fails.

### Bold keywords after the fact

```bash
resumekit bold out/Resume_Acme.docx "ServiceNow" "Intune" "PowerShell" --max 3
```

### Duplicate-application screen

```bash
resumekit screen "Initech" "Umbrella Corp" --log applications.csv --folder out/ --ignore yourname
```

Verdicts are `DUPLICATE`, `REVIEW` or `CLEAR`. The log is any CSV with a `company` column.

## Python API

```python
from resumekit import build, merge, lint, bold_docx, check_pdf
from resumekit.builder import load_file

data = merge(load_file("my_profile.yaml"), load_file("tailor.yaml"))
assert not lint(data, load_file("rules.yaml"))
build(data, "out/Resume.docx")
```

## Contributing

Issues and pull requests are welcome, especially new layout checks, templates and
non-English verb lists for the tense check. Run `pip install -e .[dev] && pytest` before
opening a PR.

## License

MIT
