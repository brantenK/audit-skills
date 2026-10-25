---
name: audit-conventions
description: Ground rules for any audit working-paper task - read before creating, editing or sending any working paper, extract or schedule for an audit engagement.
---

# Audit conventions

These rules apply to every other audit skill. Read them first.

## 1. Know the engagement before touching a file

- Run `audit-skills engagement show` in the engagement folder (or call the `engagement_info` MCP tool).
  It gives client name, year end, performance materiality (PM), clearly trivial, client category and
  the individually significant threshold.
- Never hard-code materiality. Take it from the engagement config. When you change a paper, check every
  materiality cell agrees to the config (a stale trivial threshold left from last year is a common error).

## 2. Prior-year template first

- If a prior-year working paper exists for the section, update it (skill `update-from-prior-year`).
  Do not build a new layout unless the user asks for one.
- Keep the prior-year layout, headings, legends and column order. Change only what the year requires.
- Do not delete sheets or rebuild sections without asking.

## 3. Formatting

- Arial. Black text. Grey shading only (D9D9D9 headers, F2F2F2 sub-totals). No other colours.
- Numbers `#,##0.00;(#,##0.00);"-"`. Dates `dd mmm yyyy`.
- Totals and checks are formulas, not typed numbers.
- Rebuilding a table does not license a new border style. Reproduce the prior-year convention: detail
  rows carry no borders, a subtotal row a single top and double bottom, the grand total a double top and
  double bottom, and a grey header band instead of a grid. Never box every cell of a rebuilt table.
- NEVER apply Freeze Panes or frozen rows/columns unless the user explicitly requests it for that workbook. New workbooks must be unfrozen; preserve existing pane settings unless asked to change them. This overrides template and generated-script defaults.

## 4. Internal paper versus client output

- A working paper is internal. It may contain materiality, risk, coverage, findings and conclusions.
- Anything sent to the client (requests, extracts, lists) contains **only** what the client needs:
  the ledger lines in the ledger's own columns. No materiality, coverage, findings, bank references,
  conclusions or response boxes unless the user asks for them.
- Never save an internal paper with a name that suggests it is for the client.
- Ask clients for records and specific missing explanations, not to carry out our audit procedures. We perform ledger tracing, allocation checks and reconciliations ourselves.
- Keep requests limited to the approved work. Check evidence already held before requesting it again; do not turn every risk noted into another document request or procedure.

## 5. Scope comes from the lead sheet

- The accounts in scope are the accounts on the lead sheet for that section. Do not add accounts that
  sit nearby in the trial balance (for example an unallocated deposits account) unless the user says so.
- Totals must agree to the lead sheet.
- Establish the exact lead-sheet account list, entity, period and relevant posting side before selecting transactions. An invoice reference or an account-code prefix alone does not establish scope.
- Revenue occurrence uses recognised revenue accounts, not income received in advance or other-income accounts outside the lead. A journal releasing deferred income into recognised revenue can be in scope on its revenue side.
- Separate a broad invoice-number continuity population from a revenue-value sample. Using all genuine invoices to explain numbering does not authorise sampling all invoice postings as revenue.
- Do not remove zero-balance accounts or fully reversed items solely because their closing balance is nil. Inspect the underlying movements and decide their relevance to the assertion.
- Before correcting an approved sample, show the proposed exclusions, retained count and effect on the agreed sample size. Do not silently leave a last-ten table with fewer than ten items or call a filtered subset a new systematic draw. Obtain approval for replacements or a changed scope.

## 6. Say only what the evidence shows

- Do not write explanations into a working paper that you have not confirmed. If you do not know why a
  balance moved, write it as a question for the client, not as a fact.
- Auditor adjustments from last year may not be in the client's ledger. Reclassifications (RCL) are
  usually presentation-only: the client does not post them and they do not change totals. Note them in the
  paper; do not treat them as a client action. Never assume the client posted or reversed an adjustment.
- Distinguish selected, requested, received and vouched items. Selection totals are not amounts verified; blank testing columns cannot support a clean conclusion.
- Customer/amount matching identifies candidate invoice-credit-note links, not confirmed allocations. Obtain explicit references or allocation evidence before treating a link as proved.
- Subsequent credit notes and a cancellation reported in minutes flag a potential recognition issue; they do not establish a misstatement without the effective date, entitlement/service period and credit-note reasons.
- State completion precisely: the sample/request may be complete while documentary testing and the audit conclusion remain outstanding.

### Minutes: insights, not an automatic new audit exercise

- Read minutes for relevant insights into the existing sections. Quote the source meeting/date and distinguish management's statements, allegations and proposals from verified facts.
- Do not create a separate minutes working paper, extra sheets, investigations or expanded testing unless requested or agreed with the reviewer.
- A report that invoices were not received is not proof that they were never recorded. A count discussed before year end is not automatically the year-end population.
- A reported accounting correction is not verified merely because a later account nets to zero; trace the correction to the relevant period, transactions and final balances.

### Notes: findings only, always anchored

- Do not add a Notes block to any sheet unless the user asks for one. Ask first; a notes section is not
  part of a default build, and a sheet may be complete without one.
- A note exists to explain something the reader would otherwise query: a difference and its cause, a
  limitation on the evidence, an exception, a report to management, a scope exclusion that changes a
  total, or a cross-reference to another working paper.
- Never use notes for procedure descriptions, restatements of the balance, or a narrative of what the
  auditor did. That belongs in the procedures or the work-done table, where the reader expects it.
- Every note must be anchored: put a superscript `N1`, `N2` on the row, amount or cell it explains. A
  note with nothing pointing to it is dead text - do not write it.
- Where there is nothing to report, write `None`, as the prior-year papers do.
- Prior-year shape to reproduce (the shape, not the wording): finding -> explanation -> report to
  management raised -> cross-reference to the supporting paper.
- When notes are deleted or renumbered, sweep the whole workbook in the same pass for references to
  them - including cross-sheet ones such as `Analytical N1` - and remove or re-point every one.

### Evidence the client already sent

- Search Sent Items as well as the Inbox. Count sheets, confirmations and schedules that the auditor
  sent to the client sit in Sent, not in the Inbox.
- Attachments are often scans with no text layer. Render the page to an image and read it; an empty text
  extraction does not mean an empty document.
- A document already held is not outstanding. Check what is held before adding it to a client request.

## 7. Files and folders

- Client workpaper folders are read-only unless the user names the file to change.
- Scratch files go in the tool's temp folder, never in workpaper folders.
- Do not delete files unless the user asks.

## 8. Excel mode

- If the workbook is open in Excel, live mode (xlwings) can edit it in place. Live mode needs the user's
  approval: they run `audit-skills approve <workbook>` themselves. You cannot approve it for them.
- File mode cannot keep cached values of external links (such as Caseware links). If a workbook has
  external links, prefer live mode or warn the user before saving in file mode.
- Saving a workbook with openpyxl - including a file-mode edit such as deleting a sheet - flattens
  per-character formatting. Superscript tick marks, legend entries and note references come back as
  plain text. Re-apply them in live Excel afterwards and verify per character, not by cell value.

## 9. Check before you hand over

- Recalculate, confirm zero formula errors, confirm totals agree to the TB or lead sheet.
- Tell the user what was checked and what was not.
