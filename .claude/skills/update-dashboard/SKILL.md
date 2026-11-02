---
name: update-dashboard
description: Sync the person's Job_Dashboard.html with their Gmail (application confirmations, interviews, assessments, rejections) using a checkpoint so each run only reads new mail. Also logs applications they report by hand. Use for "update dashboard", "sync applications", or "applied to X".
---

# Update the job dashboard

Files in their JobSearch folder: `Job_Dashboard.html` and `dashboard_sync_checkpoint.json`.
Always change the dashboard through `dashboard/dashboard.py`. Never paste the HTML into the
conversation, and never hand-edit it.

## Quick path: "applied to X"

Write a small JSON list and add it:

```
[{"date": "2026-11-02", "role": "Systems Administrator", "company": "Acme Corp", "location": "Dallas, TX"}]
python3 dashboard/dashboard.py add <folder>/Job_Dashboard.html rows.json
```

## Gmail sync

1. **Read the checkpoint.** If `last_processed_date` is empty, this is the first run
   (bootstrap): search the last 30 days, or what they asked for. Otherwise search **only from
   `last_processed_date` forward**, and skip messages whose ID is in
   `processed_message_ids_on_last_date`. Don't rescan the whole mailbox unless they ask for
   a full rebuild.
2. **Search Gmail** for application mail. Useful queries:
   - `"your application was sent to"` (LinkedIn), `from:indeed "application"`
   - `subject:(application received OR thank you for applying OR application submitted)`
   - `subject:(interview OR assessment OR next steps OR schedule)`
   - `subject:(unfortunately OR not moving forward OR position has been filled)`

   Read messages as plain text, not HTML, which is far smaller.
3. **Pull out** company, role, location, date and Gmail thread ID. Ignore newsletters, job
   alerts and marketing ("jobs you may like" is not an application).
4. **Match against the dashboard** with `dashboard.py check`:
   - New confirmation: add a row with status `Pending (Application Confirmed Sent)`.
   - Interview invite: `setstatus N "Interview - <date/time if given>" --gmail <threadId>`
   - Assessment or test: `setstatus N "Assessment - <what>" --gmail <threadId>`
   - Something they must do (form, availability, documents):
     `setstatus N "Action Required - <what>" --gmail <threadId>`
   - Rejection: `setstatus N "Rejected"`. The tool keeps `reachedStage` if they'd been
     interviewed.
   - Offer: `setstatus N "Offer" --gmail <threadId>`
5. **Verify:** run `dashboard.py stats`, and check the row count went up by exactly the rows
   you added.
6. **Only after the dashboard saved successfully, update the checkpoint:** newest processed
   date and message ID, the list of IDs processed on that date, `dashboard_row_count`,
   `dashboard_max_number`, and `last_sync_completed_utc`. If anything failed, leave the
   checkpoint as it was so the next run retries.

## Report in two or three lines

```
Dashboard: 142 -> 149 applications (Oct 30 - Nov 2).
New: 2 interviews (Acme, Initech), 1 assessment (Globex), 3 rejections.
```

Call out anything that needs action: interview times, assessment deadlines, or a suspicious
posting (requests for money, bank details or check deposits are scam signs).
