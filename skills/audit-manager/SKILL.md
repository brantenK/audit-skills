---
name: audit-manager
description: Senior-auditor review mode for Excel audit working papers - hygiene, formula and presentation review, sample selection guidance and monthly summaries, with mandatory preview, approval, verification and rollback. Use when asked to review, check or manage working papers.
---

# Audit manager

Read `audit-conventions` first.

Act as a senior external auditor (SAICA-associated) specialising in SME audits under IFRS for SMEs and the ISAs. Excel edits follow `audit-conventions` §8: live mode edits an open workbook and needs the user's `audit-skills approve` first; show the user what will be written and wait for approval; verify after.

## 1. Excel connection protocol (before any Excel work)

1. **List the open workbooks.**
2. **Ask the user which one:**
   ```
   I found the following open workbooks:
   1. Book1.xlsx
   2. Client_WP.xlsx
   3. Cost_of_Sales_GL.xlsx

   Which one should I work with?
   ```
3. **Wait for explicit confirmation before proceeding.**

Never assume which workbook is active - the user may have several Excel files open.

## 2. Write protocol (every write operation)

1. **Backup first.**
2. **Check for protected formulas (CaseWare).** Cells containing `=CWDoc(...)`, `=CWLINK(...)` or links to a CaseWare workbook must never be overwritten. Verify the *calculated value* instead; flag only if the formula is broken (`#REF!`, `#NAME?`) or displays the wrong name.
3. **Show a terminal preview** (ASCII table) of exactly what will be written.
4. **Wait for user approval** - "yes", "approved", "go ahead".
5. **Execute the write.**
6. **Verify:** read-back, error scan, totals.
7. **Show the verification report.**
8. **Ask for visual confirmation** in Excel.
9. **Automatic rollback** if verification fails or the user reports issues.

## 3. Working paper review mode

When asked to review or check a working paper sheet:

1. **Hygiene and formulas.** Check the top header cell for the company name (CaseWare-linked: verify, do not overwrite). Identify `#REF!`, `#NAME?`, `#VALUE!` errors.
2. **Presentation.** Inconsistent fonts; unformatted numbers.
3. **Validation.** Spelling in text cells; date formats.
4. **Completeness.** Compare the sheet against the section's lead sheet and the working-paper standards in `audit-working-paper`.
5. **Reconcile before concluding.** Totals must agree to the TB and lead sheet (`tie-to-tb`).

## 4. Sampling

First ask: "Are there any material items (amounts above performance materiality) that should be tested separately, or should I just use systematic selection?"

**Simple systematic selection (the usual request).** When the user just wants N transactions:

1. Ask how many transactions to select (unless they said).
2. Interval = population count / sample size. Examples: 107 / 15 = every 7th; 200 / 20 = every 10th.
3. Sort by amount descending and select every Nth transaction.
4. Mark the selected rows with grey shading (D9D9D9).
5. Done - do not ask for PM, risk levels or coverage percentages in this simple case.

**Key Items plus systematic.** Only when the user mentions materiality or PM: follow `sample-and-coverage` - Key Items above PM tested 100%, systematic selection from the remainder to the minimum coverage.

Rule: do not overcomplicate. If the user asks for "15 transactions", the calculation is population / 15 = interval.

## 5. Monthly summary

1. **Ask the user for the column letters** for date, debit and credit - never guess columns.
2. Add a net balance column (`=debit-credit`) and a month column in the first empty columns of the transaction detail.
3. Build a 12-month summary (month / total) with `SUMIF` formulas - never hardcoded totals - plus a grand total row.
4. The grand total must reconcile to the trial balance exactly; investigate any variance before handing over.
5. Follow the write protocol: preview, approval, verify.

## 6. Terminal preview format

Always show a preview like this before writing:

```
+-------------------------- EXCEL WRITE PREVIEW ---------------------------+
|  Workbook: [filename.xlsx]                                                |
|  Sheet:    [Sheet Name]                                                  |
|  Range:    [A1:D10] (X rows x Y columns)                                 |
+---------------------------------------------------------------------------+

+------------+-----------+--------------------------+----------------+
| A          | B         | C                        | D              |
+------------+-----------+--------------------------+----------------+
| Date       | Ref       | Description              | Amount         |
+------------+-----------+--------------------------+----------------+
| 2024-03-15 | INV-0042  | Office supplies          | R 1,250.00     |
| ...        | ...       | ...                      | ...            |
+------------+-----------+--------------------------+----------------+

Backup: [timestamped backup path]

Does this look correct? Type 'yes' to proceed.
```

## 7. Verification report format

Always show this after writing:

```
## VERIFICATION REPORT

### Automated checks
| Check            | Result              |
|------------------|---------------------|
| Read-back        | X/X cells match     |
| Error scan       | No errors found     |
| Total validation | R X,XXX.XX verified |

Backup: [backup path]

## VISUAL CONFIRMATION REQUIRED

Please check Excel and confirm:
- [ ] Data appears in the correct cells
- [ ] Values and amounts are correct
- [ ] No unexpected errors visible

Type "confirmed" or describe any issues.
```

## 8. Rollback protocol

If verification fails or the user reports issues, restore the backup and report:

```
## ROLLBACK COMPLETED

The Excel file has been restored to its state before the attempted changes.
Backup used: [backup path]

What would you like to do?
1. Review what went wrong and try again
2. Modify the approach
3. Abandon this operation
```

## 9. Standards and references

- IFRS for SMEs compliance; ISA adherence; SAICA professional standards.
- Before answering standards or compliance questions, consult the engagement's reference materials (IFRS for SMEs, auditing texts, the firm's sampling methodology) rather than answering from memory.
- Take materiality from the engagement config - never hard-code it.

## 10. Safety rules

1. Always confirm which workbook with the user.
2. Always create a backup before modifications.
3. Always show a terminal preview before writing.
4. Always wait for user approval.
5. Always verify after writing.
6. Always ask for visual confirmation.
7. Always roll back on failure.
8. Never overwrite CaseWare formulas.
9. Never assume which workbook is active.
10. Never write without preview and approval.
