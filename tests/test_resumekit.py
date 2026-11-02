import os

from docx import Document

from resumekit import bold_docx, build, lint, merge, screen
from resumekit.builder import load_file
from resumekit.screen import load_corpus

HERE = os.path.dirname(__file__)
EX = os.path.join(HERE, "..", "examples")


def profile():
    return load_file(os.path.join(EX, "profile.yaml"))


def test_build_writes_name_and_bold(tmp_path):
    out = build(profile(), str(tmp_path / "r.docx"))
    doc = Document(out)
    assert doc.paragraphs[0].text == "JORDAN EXAMPLE"
    assert any(r.bold and r.text == "PowerShell" for p in doc.paragraphs for r in p.runs)


def test_merge_overrides_one_role():
    data = merge(profile(), load_file(os.path.join(EX, "tailor_cloud_role.yaml")))
    assert data["headline"] == "Cloud Administrator"
    assert data["experience"][0]["title"] == "Cloud Administrator"
    assert data["experience"][1]["title"] == "IT Support Specialist"


def test_lint_catches_banned_and_tense():
    data = profile()
    data["experience"][1]["bullets"].append("Manages SCCM for the whole fleet.")
    probs = lint(data, {"banned": [r"\bSCCM\b"], "min_words": 0})
    assert any("SCCM" in p for p in probs)
    assert any("not past tense" in p for p in probs)


def test_lint_example_passes():
    assert lint(profile(), load_file(os.path.join(EX, "rules.yaml"))) == []


def test_bold_docx(tmp_path):
    data = profile()
    data["summary"] = ["Plain bullet mentioning Jira and Confluence."]
    out = build(data, str(tmp_path / "r.docx"))
    assert bold_docx(out, ["Jira", "confluence"]) == 2


def test_screen_ranks_rare_tokens():
    corpus = load_corpus(os.path.join(EX, "applications.csv"))
    r = screen(["Initech LLC", "Northside Credit Union", "Brand New Co"], corpus)
    assert r["Initech LLC"]["verdict"] == "DUPLICATE"
    assert r["Brand New Co"]["verdict"] == "CLEAR"


def test_never_claim_from_profile():
    data = profile()
    data["summary"].append("Expert in Kubernetes clusters.")
    assert any("Kubernetes" in p for p in lint(data, {"min_words": 0}))


def test_dashboard_roundtrip(tmp_path):
    import json, subprocess, sys
    tool = os.path.join(HERE, "..", "dashboard", "dashboard.py")
    run = lambda *a: subprocess.run([sys.executable, tool, *a], capture_output=True, text=True, check=True).stdout
    run("init", str(tmp_path))
    dash = str(tmp_path / "Job_Dashboard.html")
    rows = tmp_path / "rows.json"
    rows.write_text(json.dumps([
        {"date": "2026-11-01", "role": "Systems Administrator", "company": "Initech", "location": "Dallas, TX"},
        {"date": "2026-11-02", "role": "IT Support", "company": "Umbrella Health", "location": "Remote"},
        {"date": "2026-11-02", "role": "IT Support", "company": "Umbrella Health", "location": "Remote"},
    ]))
    assert "added 2" in run("add", dash, str(rows))
    run("setstatus", dash, "1", "Interview - Nov 5", "--gmail", "abc123")
    run("setstatus", dash, "1", "Rejected")
    assert "DUPLICATE" in run("check", dash, "Initech LLC")
    assert "rows: 2" in run("stats", dash)
    html = open(dash).read()
    assert '"reachedStage": "Interview"' in html and "#all/abc123" in html
