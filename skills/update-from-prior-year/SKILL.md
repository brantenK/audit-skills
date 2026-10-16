---
name: update-from-prior-year
description: Roll a prior-year audit working paper forward to the current year by editing the prior-year workbook in place - use when the user asks to prepare a current-year paper and a prior-year paper exists. Not for building a new paper from scratch.
---

# Update a working paper from the prior-year template

Read `audit-conventions` first.

## Steps

1. **Find the prior-year paper** for the section and confirm with the user which sheet is the paper
   (prior-year workbooks often carry extra scratch sheets).
2. **Check for external links** (Caseware and other workbook links):
   `audit-skills template inspect <prior-year.xlsx>`.
   - If links exist and the workbook can be opened in Excel, use live mode (needs user approval).
   - In file mode the cached link values are lost. Tell the user before you save.
3. **Copy, do not overwrite.** Create the current-year file next to where the user wants it:
   `audit-skills template roll <prior-year.xlsx> <current-year.xlsx> --sheet <name> --year <yyyy>`.
   This copies the workbook, renames the sheet to the new year and shifts year labels in the header
   and column headings.
4. **Clear only what must be re-done**:
   - risk ratings and level of risk (the auditor re-assesses them each year),
   - prior-year notes, findings and conclusion,
   - prior-year testing rows (keep the headings and column layout).
5. **Update inputs from the engagement config**: PM, trivial, individually significant, year end.
6. **Update balances** from the current-year TB and move last year's balances to the comparative column.
7. **Keep** the layout, legends, section order, grey shading and formulas. Fix formulas that break
   (`#REF!`, division by zero) by guarding them, not by deleting them.
8. **Recalculate and check**: zero errors, totals agree to the TB and lead sheet.

## Do not

- Do not delete sheets, rebuild sections or add colours without asking.
- Do not carry last year's conclusion into this year.
- Do not write explanations for movements you have not confirmed.
