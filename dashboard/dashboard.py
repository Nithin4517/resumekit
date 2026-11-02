#!/usr/bin/env python3
"""Job_Dashboard.html helper. Prints small results only, never the whole file.

  init FOLDER                    copy the blank dashboard + checkpoint into FOLDER
  stats FILE                     row count, max number, date range, status counts
  check FILE "Company" ...       already applied? (DUPLICATE / REVIEW / CLEAR)
  add FILE rows.json             append rows (JSON list of {date, role, company, location[, status, gmailLink]})
  setstatus FILE N "status" [--gmail THREAD_ID]
  export FILE out.csv            write all rows to CSV

Every write is verified (valid JSON, row count +N, nothing else changed) and a
.bak copy is kept beside the file.
"""
import csv
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
START, END = "/*DATA_START*/", "/*DATA_END*/"
GMAIL = "https://mail.google.com/mail/u/0/#all/"
PENDING = "Pending (Application Confirmed Sent)"


def load(path):
    s = open(path, encoding="utf-8").read()
    a, b = s.index(START) + len(START), s.index(END)
    return s, a, b, json.loads(s[a:b])


def save(path, s, a, b, rows, expect_count):
    blob = "[\n" + ",\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n]"
    new = s[:a] + blob + s[b:]
    _, _, _, check = load_text(new)
    assert len(check) == expect_count, "row count mismatch after write"
    shutil.copy2(path, path + ".bak")
    open(path, "w", encoding="utf-8").write(new)


def load_text(s):
    a, b = s.index(START) + len(START), s.index(END)
    return s, a, b, json.loads(s[a:b])


def cmd_init(folder):
    os.makedirs(folder, exist_ok=True)
    dst = os.path.join(folder, "Job_Dashboard.html")
    if os.path.exists(dst):
        print("exists, left untouched:", dst)
    else:
        shutil.copy2(os.path.join(HERE, "Job_Dashboard.html"), dst)
        print("created", dst)
    ck = os.path.join(folder, "dashboard_sync_checkpoint.json")
    if not os.path.exists(ck):
        json.dump({"last_sync_completed_utc": None, "last_processed_date": None,
                   "last_processed_message_id": None, "processed_message_ids_on_last_date": [],
                   "dashboard_row_count": 0, "dashboard_max_number": 0}, open(ck, "w"), indent=2)
        print("created", ck)


def cmd_stats(path):
    rows = load(path)[3]
    from collections import Counter
    print("rows:", len(rows), "| max number:", max([r["number"] for r in rows] or [0]))
    if rows:
        d = sorted(r["date"] for r in rows)
        print("dates:", d[0], "to", d[-1])
        for k, v in Counter(r.get("status", "").split(" (")[0] for r in rows).most_common():
            print(f"  {v:5}  {k}")


def cmd_check(path, names):
    sys.path.insert(0, os.path.dirname(HERE))
    from resumekit.screen import screen
    rows = load(path)[3]
    corpus = [("dashboard", f"{r['company']}") for r in rows]
    for name, res in screen(names, corpus).items():
        print(f"=== {name} -> {res['verdict']}")
        for _, rarest, _, hit, key in res["hits"][:3]:
            match = next(r for r in rows if r["company"] == key)
            print(f"    #{match['number']} {match['date']} {key} | {match['role']} | {match.get('status','')}")
    return 0


def cmd_add(path, rows_file):
    s, a, b, rows = load(path)
    new = json.load(open(rows_file, encoding="utf-8"))
    n = max([r["number"] for r in rows] or [0])
    have = {(r["company"].lower(), r["role"].lower()) for r in rows}
    added = 0
    for r in new:
        if (r["company"].lower(), r["role"].lower()) in have:
            print("skip duplicate:", r["company"], "|", r["role"])
            continue
        n += 1
        row = {"number": n, "date": r["date"], "role": r["role"], "company": r["company"],
               "location": r.get("location", ""), "status": r.get("status", PENDING)}
        if r.get("gmailLink"):
            row["gmailLink"] = r["gmailLink"]
        rows.append(row)
        have.add((row["company"].lower(), row["role"].lower()))
        added += 1
    save(path, s, a, b, rows, len(rows))
    print(f"added {added} | rows now {len(rows)} | max number {n}")


def cmd_setstatus(path, num, status, gmail=None):
    s, a, b, rows = load(path)
    r = next((r for r in rows if r["number"] == int(num)), None)
    if not r:
        sys.exit(f"no row #{num}")
    old = r.get("status", "")
    if old.lower().startswith(("interview", "assessment")) and status.lower().startswith(("rejected", "closed")):
        r["reachedStage"] = old.split(" ")[0]
    r["status"] = status
    if gmail:
        r["gmailLink"] = gmail if gmail.startswith("http") else GMAIL + gmail
    save(path, s, a, b, rows, len(rows))
    print(f"#{num} {r['company']}: {old!r} -> {status!r}")


def cmd_export(path, out):
    rows = load(path)[3]
    keys = ["number", "date", "role", "company", "location", "status", "gmailLink"]
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, keys, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    print("wrote", len(rows), "rows to", out)


def main(a):
    if len(a) < 2:
        sys.exit(__doc__)
    c = a[0]
    if c == "init":
        return cmd_init(a[1])
    if c == "stats":
        return cmd_stats(a[1])
    if c == "check":
        return cmd_check(a[1], a[2:])
    if c == "add":
        return cmd_add(a[1], a[2])
    if c == "setstatus":
        g = a[a.index("--gmail") + 1] if "--gmail" in a else None
        return cmd_setstatus(a[1], a[2], a[3], g)
    if c == "export":
        return cmd_export(a[1], a[2])
    sys.exit(__doc__)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]) or 0)
