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
6. Stronger evidence is the client's contract, invoice or proforma for the event. Note when only a
   printed web page is available.

`audit-skills cutoff table --events <events.csv> --year-end <yyyy-mm-dd>` builds the table with the
after-year-end and financial-year flags.
