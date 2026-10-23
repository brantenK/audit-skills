---
name: event-dates-cutoff
description: Confirm event or conference dates against organiser sources to test cut-off of prepaid expenses and income received in advance - use when balances relate to future events and the user needs evidence of when they take place.
---

# Event dates for cut-off

Read `audit-conventions` first.

## Why

Prepaid costs and income received in advance for an event belong to the year in which the event happens.
The event date decides whether the balance is correctly carried at year end.

## Steps

0. **Check evidence already held first.** Reuse an adequately documented organiser website date or saved source; do not request all dates again or duplicate research. Planning schedules show intended dates, not necessarily actual occurrence. Follow up only unmatched, unclear, postponed or cancelled events and document the specific limitation.

1. **List the events** from the ledger account names. Prepaid and income-in-advance accounts for the same
   event often share an account suffix; match them.
2. **Find the dates** on the organiser's own page first. Third-party listings are weaker; mark them.
3. **Evidence**: ask the user to print each page to PDF (the footer shows the URL and the print date and
   time) and keep the PDFs in the engagement's event-dates folder. Read the PDFs; scanned ones need
   rendering.
4. **Record** for each account: event, dates (conference, workshops, technical visits), venue, after year
   end (yes or no), financial year the event falls in, source file.
5. **Flag**:
   - dates not labelled as the event dates,
   - event names that do not clearly match the account (ask the client),
   - account labels whose financial year disagrees with the event date,
   - events more than 12 months after year end (non-current),
   - events before year end that still carry a balance.
6. Evidence must answer the question: an organiser page can establish a public event date; agreements/invoices can establish entitlement and service terms. A planning schedule or proforma is not necessarily proof the event occurred. Note limitations and request additional evidence only for a specific unresolved issue, not as a blanket second request.

`audit-skills cutoff table --events <events.csv> --year-end <yyyy-mm-dd>` builds the table with the
after-year-end and financial-year flags.

## Recording the source in the paper

- Add a **Source link** column to the event-dates table and put the organiser's page on each row as a
  hyperlink (short label visible, full URL embedded). The reviewer must be able to click through from
  the paper without hunting for a folder.
- Link the **direct event page**, not an "upcoming events" or "past events" index. Individual event
  pages normally stay live after the event - check before falling back to the index.
- When no page can be found, write "To confirm with client" - do not leave a date unsupported.
- Third-party listings (conference calendars, sponsor pages) are acceptable evidence but label them as
  third-party.

## Use of AI-assisted research

- Public sources may be researched with AI-assisted search. Record that in the paper (e.g. "dates
  researched using AI-assisted search of the organiser's website; source link per event; results
  reviewed by the engagement team").
- The link is the evidence; the AI is only the search tool. Never record an event date without a link or
  a client document.
