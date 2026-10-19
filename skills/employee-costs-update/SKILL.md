---
name: employee-costs-update
description: Roll an employee costs working paper (e.g. a monthly insurance premium account) forward by locating the account in the client GL, extracting its 12 monthly transactions, and updating the ledger and WP sheets with formula-based totals. Use when an employee-cost paper must be updated from the prior year to the current year.
---

# Employee costs working paper update

Read `audit-conventions` first.

Excel edits follow `audit-conventions` §8: live mode edits an open workbook and needs the user's `audit-skills approve` first; show the user what will be written and wait for approval; verify after.

## Inputs (per engagement - confirm with the user, never assume)

- **Working paper:** `<WP file>` (e.g. `65 Employee costs <benefit>.xls`)
- **Account:** `<payroll-cost account>` code and description (e.g. an employee insurance premium account)
- **GL source:** `<Client> Detail General Ledger <date>.xls`
- **Sheets involved:** the WP sheet and its Ledger sheet

## What works and what does not

Do:
- **Locate the account via its header row.** Employee-cost data is not on a separate sheet - it sits intermixed with other accounts, often deep in the GL sheet.
- **Use formulas for totals** (`=SUM`), never hardcoded values - the audit trail depends on it.
- **Back up before every modification** so rollback is possible.

Do not:
- **Search a single expected column for the account code.** Scan the full row width and use several criteria; the account column varies by GL export format.
- **Assume a sheet structure.** Some GL exports start with transactions immediately; others bury the account header far down.
- **Hardcode totals.** It breaks the audit trail.

## Steps

### 1. Pre-flight checks

Confirm both workbooks are open and their exact names with the user before doing anything.

### 2. Locate the account in the GL

Find the account header block. Pattern:

```
Account ID :  <payroll-cost account>   Description : <description>
Jan <yy>:  (month separator)
Feb <yy>:  ...
DIST | BR | <payroll-cost account> | Date | Ref | Description | Debit | Credit
```

Record the header row number and the 12 transaction rows below it (a premium-type account typically has exactly one posting per month, with month separators between them). Re-locate these rows fresh for every engagement - never reuse row numbers from a previous year or another client.

```python
header = gl_sheet.range(f'A{header_row}:K{header_row}').value

month_separators = {'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'}  # match e.g. 'Jan 25:'
transactions = []
for row in range(first_data_row, last_data_row + 1):
    row_data = gl_sheet.range(f'A{row}:K{row}').value
    if row_data and row_data[0] and str(row_data[0]) not in month_separators:
        transactions.append(row_data)
```

### 3. Update the Ledger sheet

1. Create a backup.
2. Clear the existing transaction rows.
3. Write the header and the 12 new transactions.
4. Format: bold header, `#,##0.00` on the debit/credit columns, autofit columns, borders.

### 4. Update the WP sheet

1. Create a backup.
2. **Totals row (row 45 in the reference layout):** write the current-year total (from the extracted transactions) and the prior-year total into their columns.
3. **Variance row (row 46):** only the % change cell is a manual input. The variance cells auto-calculate from the totals row via formulas - **do not overwrite them with values.**
4. **Transaction listing (rows 51-62 in the reference layout):** clear the old transactions and write the 12 current-year transactions: Account ID, Date, Description, Debit, Credit.
5. **Total row (row 64):** must be a formula - `=SUM(E51:E62)` - not a typed number.
6. **Closing balance row (row 66):** must be a formula - `=E64` - not a typed number.

### 5. Verify

1. Read-back check: all written cells match.
2. Error scan: no `#REF!`, `#VALUE!`, etc.
3. Total validation: the sum of transactions agrees to the GL header totals.
4. Formula verification: the total and closing-balance rows contain formulas, not values.
5. Variance check: the auto-calculated variance cell equals current-year total minus prior-year total.

## Critical formulas (reference layout)

```
Variance row:   D46: =SUM(D45)     F46: =SUM(F45)     H46: =+D46-F46
                                                      J46: manual % change
Total:          E64: =SUM(E51:E62)
Closing bal:    E66: =E64
```

## Data structures

### GL ledger columns

| Col | Content | Typical value |
|-----|---------|---------------|
| A | Batch # | `<batch>` |
| B | Type | DIST |
| C | Source | BR |
| D | Account | `<payroll-cost account>` |
| E | Date | `<dd/mm/yy>` |
| F | Ref | `<ref>` |
| G | Source Ref | `<source ref>` |
| H | Source Code | `<bank/insurer code>` |
| I | Description | `<policy description>` |
| J | Debit | `<amount>` |
| K | Credit | `<amount>` |

The Ledger sheet repeats this structure, formatted as a working paper. The WP transaction listing uses: A Account ID, B Date, C Description, E Debit, F Credit.

## Common issues and solutions

- **Account not found in the GL.** Search the full row width (A:Z), not just one column; the account may sit in a different column depending on the export.
- **Totals do not agree after replacing transactions.** The total and closing-balance rows must be formulas; check for typed values and restore `=SUM(...)` / `=<total cell>`.
- **Wrong data extracted (old transactions).** Re-verify the account header row - employee accounts are intermixed with other accounts, and the header block is the only reliable reference point.
- **Variance row broken.** The auto-calculating cells were overwritten with values. Restore the formulas; only the % change cell is manual.

## Professional standards applied

1. **Golden thread:** all numbers traceable TB -> ledger -> WP sheet.
2. **Formulas over hardcoding** for the audit trail.
3. **Tick marks preserved** on the totals row (e.g. `BTB 750`, `BPYTB`).
4. **Variance analysis:** the variance row shows the movement with % change.
5. **Backup protocol:** every change backed up, with rollback available.

## Illustrative example (synthetic figures)

A monthly premium account with a mid-year premium increase:

| Item | PY total | CY total | Variance | % change |
|------|----------|----------|----------|----------|
| Total | R 10,000.00 | R 11,000.00 | R 1,000.00 | +10.0% |

| Month | Amount |
|-------|--------|
| Jan - Jun | R 833.33 per month |
| Jul - Dec | R 916.67 per month (premium increased) |

## Verification checklist

- [ ] Backup created
- [ ] Ledger sheet updated with the 12 current-year transactions
- [ ] WP totals row updated (current year and prior year)
- [ ] % change updated (manual cell only)
- [ ] Transaction listing replaced
- [ ] Total row uses `=SUM(...)` over the listing
- [ ] Closing balance row references the total cell
- [ ] Total matches the sum of transactions
- [ ] Variance auto-calculates correctly
- [ ] No Excel errors (`#REF!`, `#VALUE!`, etc.)
- [ ] Visual confirmation in Excel by the user
