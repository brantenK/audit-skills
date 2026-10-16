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

## 4. Internal paper versus client output

- A working paper is internal. It may contain materiality, risk, coverage, findings and conclusions.
- Anything sent to the client (requests, extracts, lists) contains **only** what the client needs:
  the ledger lines in the ledger's own columns. No materiality, coverage, findings, bank references,
  conclusions or response boxes unless the user asks for them.
- Never save an internal paper with a name that suggests it is for the client.

## 5. Scope comes from the lead sheet

- The accounts in scope are the accounts on the lead sheet for that section. Do not add accounts that
  sit nearby in the trial balance (for example an unallocated deposits account) unless the user says so.
- Totals must agree to the lead sheet.

## 6. Say only what the evidence shows

- Do not write explanations into a working paper that you have not confirmed. If you do not know why a
  balance moved, write it as a question for the client, not as a fact.
- Auditor adjustments (AJE/RCL) from last year may not be in the client's ledger. Check before assuming
  the client posted or reversed them.

## 7. Files and folders

- Client workpaper folders are read-only unless the user names the file to change.
- Scratch files go in the tool's temp folder, never in workpaper folders.
- Do not delete files unless the user asks.

## 8. Excel mode

- If the workbook is open in Excel, live mode (xlwings) can edit it in place. Live mode needs the user's
  approval: they run `audit-skills approve <workbook>` themselves. You cannot approve it for them.
- File mode cannot keep cached values of external links (such as Caseware links). If a workbook has
  external links, prefer live mode or warn the user before saving in file mode.

## 9. Check before you hand over

- Recalculate, confirm zero formula errors, confirm totals agree to the TB or lead sheet.
- Tell the user what was checked and what was not.
