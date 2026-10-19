---
name: financial-liabilities
description: Reconcile other financial liabilities (instalment sale agreements) between the Existence and Valuation working paper and the Analytical working paper - flexible column mapping, gap analysis, current/non-current split and tick marks. Use when an analytical schedule must be updated from an existence and valuation source.
---

# Financial liabilities reconciliation

Read `audit-conventions` first.

Excel edits follow `audit-conventions` §8: live mode edits an open workbook and needs the user's `audit-skills approve` first; show the user what will be written and wait for approval; verify after.

## Overview

Reconcile **Other Financial Liabilities** between the **Existence & Valuation** working paper (the master source of truth) and the **Analytical** working paper. Handles instalment sale agreements, the split between current and non-current portions, and the golden-thread audit trail.

Prerequisites: confirm the active workbook with the user (several may be open) and identify the sheet names, e.g. `550.45-3 Existence & Valuation` and `550.45-1 Analytical`.

## Phase 1: source sheet discovery

Locate and validate the Existence & Valuation sheet using these markers:

1. **Lender header:** a row containing the creditor/lender name.
2. **Data header row** containing columns for:
   - "Details" or "Description" (asset/vehicle name)
   - "Agreement number" (unique reference)
   - "Short term portion" or "Current portion"
   - "Long term portion" or "Non-current portion"
   - "Capital outstanding EOY" (closing balance)
3. **Tick mark pattern:** an amortization-schedule reference such as `VAMORT 550.70.1`.

Validation rules: if multiple sheets contain the markers, ask the user which to use. If the markers are not found, ask the user to confirm the correct sheet.

## Phase 2: flexible column mapping

Identify column locations dynamically - never hardcode them. Match header text against acceptable variations:

| Target column | Acceptable header text | Variable |
|--------------|------------------------|----------|
| Description | "Details", "Description", "Item", "Asset", "Vehicle" | `desc_col` |
| Agreement number | "Agreement number", "Agreement No.", "Reference" | `agmt_col` |
| Short term / current | "Short term portion", "Short-term portion", "Current portion", "Short term" | `short_col` |
| Long term / non-current | "Long term portion", "Long-term portion", "Non-current portion", "Long term" | `long_col` |
| Closing balance | "Capital outstanding EOY", "Closing balance", "Balance EOY", "Outstanding EOY" | `balance_col` |

```python
def find_column(sheet, target_row, acceptable_headers):
    """Find a column letter by matching acceptable header variations."""
    header_row = sheet.range(f'{target_row}1:{target_row}50').value
    for i, header in enumerate(header_row):
        if header:
            for variation in acceptable_headers:
                if variation.lower() in str(header).lower():
                    return chr(65 + i)   # 65 = 'A'
    return None
```

If a column cannot be found, ask the user to identify it manually.

## Phase 3: data extraction

- **Start row:** header row + 1 (first data row).
- **End row:** the first row containing totals tick marks (`^` cast, `^CC` cross-cast) - that is the totals row.

For each agreement, extract: description, agreement number, short-term amount, long-term amount and closing balance (default missing amounts to 0.0).

Special status detection:

| Status | Detection | Action |
|--------|----------|--------|
| Paid off | `closing_balance == 0.00` | Add with R 0.00 amounts, flag as "Settled" |
| New acquisition | Opening balance = 0 and new agreements > 0 | Flag for insertion into the analytical |
| Active | `closing_balance > 0.00` | Normal processing |

## Phase 4: gap analysis

Compare the Existence sheet items with the Analytical sheet items using fuzzy matching on descriptions (handles typos and abbreviations):

```python
from difflib import SequenceMatcher

def is_match(desc1, desc2, threshold=0.7):
    """True if two descriptions are similar enough to be the same agreement."""
    if not desc1 or not desc2:
        return False
    score = SequenceMatcher(None, str(desc1).lower(), str(desc2).lower()).ratio()
    return score >= threshold
```

| Category | Description | Action |
|----------|-------------|--------|
| Missing in Analytical | In Existence, not in Analytical | Insert new rows (typically new acquisitions) |
| Missing in Existence | In Analytical, not in Existence | Flag for review (paid off, or an error) |
| Matched | Found in both | Update the current-year amounts |

Notification protocol when inserting new items: identify the agreements by description, tell the user how many were found, insert the rows with **account codes left blank** (the auditor must confirm classification), then apply amounts and tick marks.

## Phase 5: update the analytical sheet

The analytical sheet has two sections - non-current and current - each with a header row and data rows.

For **matched** items, write the current-year amounts (liabilities as negatives per the TB sign convention):

```python
sheet.range(f'{col_cy}{row_nc}').value = -agreement['long_term']    # non-current
sheet.range(f'{col_cy}{row_cur}').value = -agreement['short_term']  # current
```

For **new** items: insert a row after the last data row in the section, write the description, leave the account code blank, write both amounts, and apply the tick mark. Then update subtotals and grand totals.

**Tick mark:** `BTB [Section Number]` with the standard structure - bold anchor letter (11pt, normal), superscript source part (`TB`, 10pt), and the section number on the baseline (10pt, normal - never superscript). All text black, Arial:

```python
def apply_tick_mark_formatting(sheet, cell_range, section_number):
    """Write 'BTB <section>' with the standard tick-mark structure. All black."""
    for cell in sheet.range(cell_range):
        cell.value = f'BTB {section_number}'
        c = cell.api
        c.Font.Bold = True
        anchor = c.GetCharacters(Start=1, Length=1)
        anchor.Font.Size = 11
        anchor.Font.Superscript = False
        sup = c.GetCharacters(Start=2, Length=2)          # 'TB'
        sup.Font.Size = 10
        sup.Font.Superscript = True
        num = c.GetCharacters(Start=5, Length=len(str(section_number)))
        num.Font.Size = 10
        num.Font.Superscript = False                      # section number on the baseline
```

## Phase 6: verification

Scan the Existence sheet for the totals row via tick marks (`^`, `^CC`, `BTB`). Then check:

| Check | Expected result |
|-------|-----------------|
| Existence short-term total | `=SUM(short_col range)` |
| Existence long-term total | `=SUM(long_col range)` |
| Existence grand total | Short + Long = Closing balance total |
| Analytical non-current total | Matches Existence long-term total |
| Analytical current total | Matches Existence short-term total |
| Analytical grand total | Non-current + Current = Existence grand total |

Acceptable variance: rounding differences of R 0.01. Anything larger is flagged for auditor review.

## Workflow summary

1. **Pre-flight:** timestamped backup; list open workbooks; confirm the target workbook with the user.
2. **Source discovery:** identify the Existence & Valuation and Analytical sheets via markers (lender, columns, tick marks).
3. **Column mapping:** flexible header matching; store column references in variables.
4. **Extraction:** all agreements, with special statuses (paid off, new acquisitions); detect the totals row via tick marks.
5. **Gap analysis:** fuzzy-match descriptions; identify missing items on both sides.
6. **Update:** current-year amounts for matched items; new rows (blank account codes) for new items; `BTB` tick marks; updated subtotals and totals.
7. **Verification:** reconcile all totals across the sheets; variance within R 0.01; produce a verification report.
8. **Visual confirmation:** the user checks the analytical sheet in Excel.
9. **Rollback:** restore the timestamped backup on verification failure.

## Common issues and solutions

- **Column headers do not match the standard format.** Use the flexible matching; if still not found, ask the user.
- **Totals row not found.** Scan for tick marks (`^`, `^CC`) rather than fixed row numbers; if several rows carry tick marks, ask the user.
- **Descriptions do not match between sheets.** Lower the fuzzy threshold or confirm the mapping with the user.
- **New items need account codes.** Insert with blank codes and tell the user to fill them in.
- **Paid-off items still in the analytical.** Add with R 0.00 amounts, flagged "Settled"; let the auditor decide whether to remove.

## Example notification (synthetic figures)

```
GAP ANALYSIS RESULTS

Found 2 new agreements in the Existence sheet not present in the Analytical sheet:
  1. Vehicle A (Short: R 120,000.00, Long: R 220,000.00)
  2. Vehicle B (Short: R 90,000.00, Long: R 160,000.00)

ACTION REQUIRED:
  New rows have been inserted with BLANK account codes.
  Please fill in the appropriate account codes (e.g. <account>).

Status: ready for review in the Analytical sheet.
```

## Verification report format

```
## VERIFICATION REPORT

### Reconciliation summary (synthetic illustration)
| Metric | Existence sheet | Analytical sheet | Variance |
|--------|-----------------|------------------|----------|
| Short term (current) | R 1,000,000.00 | R 1,000,000.00 | R 0.00 |
| Long term (non-current) | R 3,000,000.00 | R 3,000,000.00 | R 0.00 |
| GRAND TOTAL | R 4,000,000.00 | R 4,000,000.00 | R 0.00 |

### Changes made
- Updated N existing agreements
- Inserted N new agreements (blank account codes)
- Applied BTB tick marks with standard formatting
- Updated subtotals and grand totals

Backup: [timestamped backup path]

## VISUAL CONFIRMATION REQUIRED

Please check the Analytical sheet and confirm:
- [ ] Data in correct cells
- [ ] New agreements visible with blank account codes
- [ ] Tick marks formatted correctly (bold anchor, superscript TB, section number on baseline)
- [ ] Totals reconcile with the Existence sheet

Type "confirmed" or describe any issues.
```

## Rollback message format

```
## ROLLBACK COMPLETED

The Excel file has been restored to its state before the attempted changes.
Backup used: [backup path]
Error details: [description of what failed]

What would you like to do?
1. Review what went wrong and try again
2. Modify the approach
3. Abandon this operation
```

## Design notes

- **Flexible column mapping** prevents breakage when clients change header text.
- **Fuzzy matching** handles description variations between sheets.
- **Tick-mark detection** of totals rows is more robust than fixed row numbers.
- **Blank account codes** force the auditor to verify classification of new items.
- Compliance: ISA 230 (documentation and audit trail), Companies Act 71 of 2008 (7-year retention).
