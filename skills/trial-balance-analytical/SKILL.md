---
name: trial-balance-analytical
description: Restructure an analytical schedule whose subtotals sit above their detail lines - moves subtotals below the details, replaces typed subtotals with SUM formulas, strips account codes, and adds variance and materiality columns - use whenever a trial-balance analytical schedule needs rebuilding into proper working-paper form.
---

# Trial balance analytical schedule restructuring

Read `audit-conventions` first.

Live mode edits the open workbook and needs the user's `audit-skills approve` first. Show the
user what will be written and wait for approval before writing; verify afterwards; save only
when the user asks (`audit-conventions` §8).

## When to use

Use this skill when an analytical schedule has:

- subtotals ABOVE their detail lines
- group headers with embedded account codes (for example `750.750.002 Advertising`)
- detail lines carrying `BTB` tick marks in a dedicated column
- no variance or materiality columns yet, or a grand total that must reconcile to the TB

Skip it when the schedule is already correctly structured, or no clear pattern marks the groups.

## Inputs to obtain first

| Input | Example | Purpose |
|---|---|---|
| Materiality threshold | 1,000,000 (illustrative) | Column G materiality test |
| Row range | 54 to 385 | Rows containing the account groups |
| CY amount column | C | Current-year amounts |
| Tick mark column | D | BTB references - identifies detail lines |
| PY amount column | E | Prior-year amounts |
| Account code pattern | `750.750` | Text pattern that marks a header row |

Never assume the columns; ask. Section codes such as `750.750` are worked examples - use the
engagement's own code pattern.

## Target structure

Before (subtotal above the details):

```
Row X:    750.750.002 Advertising  |  | 700,000.00 |         | 560,000.00   <- subtotal
Row X+1:  43010-000-02 Advertising |  | 690,000.00 | BTB 750 | 560,000.00   <- detail
Row X+2:  43010-020-02 Advertising |  |  10,000.00 | BTB 750 |       0.00   <- detail
Row X+3:  (empty)
```

After (subtotal below the details, typed values replaced by formulas):

```
Row X:    (empty)
Row X+1:  43010-000-02 Advertising |  | 690,000.00 | BTB 750 | 560,000.00
Row X+2:  43010-020-02 Advertising |  |  10,000.00 | BTB 750 |       0.00
Row X+3:  Advertising               |  | =SUM(...)  |         | =SUM(...)
```

Standard columns: A description, C current year, D tick marks, E prior year, F percentage
variance, G materiality assessment.

## Steps

### 1. Connect and back up

Connect to the workbook the user names - never guess which open workbook is the target. Make
one master backup copy of the workbook before any change and keep it until the user confirms
the result.

### 2. Read the range and identify the groups

Read `A{start}:E{end}` and walk the rows. A header row contains the code pattern in column A;
the detail rows below it carry `BTB` in the tick mark column; the subtotal target is the first
row after the details.

```python
def identify_groups(data, start_row, code_pattern):
    """data: rows read from A{start}:E{end}. Returns one dict per account group."""
    groups = []
    i = 0
    while i < len(data):
        row_num = start_row + i
        row = data[i]
        if row[0] and isinstance(row[0], str) and code_pattern in row[0]:
            if '  ' in row[0]:                     # code separated from name by a double space
                code, name = row[0].split('  ', 1)
            else:
                code, name = row[0], row[0]
            detail_start = row_num + 1
            detail_end = detail_start
            j = i + 1
            while j < len(data):                   # detail lines carry BTB in column D (index 3)
                if data[j][3] and 'BTB' in str(data[j][3]):
                    detail_end = start_row + j
                    j += 1
                else:
                    break
            groups.append({
                'header_row': row_num,              # original (misplaced) subtotal row
                'code': code,
                'name': name,
                'detail_start': detail_start,
                'detail_end': detail_end,
                'target_row': detail_end + 1,       # first empty row after the details
                'cy_value': row[2] or 0,             # column C
                'py_value': row[4] or 0,             # column E
            })
            i = detail_end - start_row + 2
        else:
            i += 1
    return groups
```

### 3. Show the inventory and get approval

Print one line per group: header row, code, group name, detail range, target row, CY and PY
values. State the planned operations (group name plus two SUM formulas plus clearing the old
header row, per group) and wait for the user's yes before writing anything.

### 4. Restructure each group

For every group: write the name (without the code) to the target row, write SUM formulas for
CY and PY, clear the original header row, then verify immediately against the original
subtotal values.

```python
for g in groups:
    target = g['target_row']
    sheet.range(f'A{target}').value = g['name']
    sheet.range(f'C{target}').formula = f"=SUM(C{g['detail_start']}:C{g['detail_end']})"
    sheet.range(f'E{target}').formula = f"=SUM(E{g['detail_start']}:E{g['detail_end']})"
    sheet.range(f"A{g['header_row']}:E{g['header_row']}").clear_contents()

    new_cy = sheet.range(f'C{target}').value or 0
    new_py = sheet.range(f'E{target}').value or 0
    ok = abs(new_cy - g['cy_value']) < 0.01 and abs(new_py - g['py_value']) < 0.01
    print(f"{g['name']}: row {g['header_row']} -> {target} | {'OK' if ok else 'MISMATCH'}")
```

`SUM` works for single-line groups too (`=SUM(C61:C61)`). A mismatch means the original
subtotal was not the sum of its details (a missing detail line, tick marks in a different
column, or a data-entry error) - stop, list the detail values, and flag it for the auditor
rather than forcing it through.

### 5. Format the subtotal rows

Apply to columns A, C, E, F, G of every subtotal row:

| Element | Style |
|---|---|
| Font | Arial, bold, black |
| Shading | D9D9D9 |
| Top border | single, thin |
| Bottom border | double |
| Number format (C, E) | `#,##0.00` |

Implementation: set `Font.Bold`, `Borders(xlEdgeTop=8)` with `xlContinuous=1` and
`Borders(xlEdgeBottom=9)` with `xlDouble=-4119`, plus the grey shading per
`audit-conventions` §3. No other colours anywhere.

### 6. Add variance and materiality formulas

Column F - percentage variance, blank on division by zero:

```excel
=IFERROR((C{row}-E{row})/ABS(E{row})*100,"")
```

Column G - materiality test against the threshold the user gave:

```excel
=IF(ABS(C{row})>=<threshold>,"Material","Not Material")
```

Worked example: CY 700,000.00 vs PY 560,000.00 gives a variance of 25.00%; with a threshold
of 1,000,000 the row reads "Not Material". Report every "Material" row to the auditor - do not
colour-code them; grey shading and black text only.

### 7. Grand total

Ask which row holds the summary line (labels such as "Balance as per below" or "Total",
usually above the first group) and which columns carry the CY and PY totals. Sum the
non-contiguous subtotal rows:

```python
cy_formula = '=' + '+'.join(f'C{r}' for r in subtotal_rows)   # or =SUM(C58,C62,C65,...)
py_formula = '=' + '+'.join(f'E{r}' for r in subtotal_rows)
```

Format the grand total like the subtotals. Then reconcile: compare the calculated CY and PY
grand totals with the expected TB figures (tolerance 0.01). If they do not match, look for
account rows that belong to no group ("orphaned" rows with a CY value outside every group's
span) and for rounding differences, and tell the user before going further.

### 8. Final verification and hand-over

- Scan every subtotal and grand-total cell for `#REF!`, `#NAME?`, `#VALUE!`, `#DIV/0!`,
  `#N/A`.
- Report: groups processed, mismatches, material items, grand total reconciled to the TB.
- Ask the user to confirm visually in Excel. If anything is wrong, restore the master backup.

## Troubleshooting

- **No groups found:** the code pattern differs - print a few header strings and adjust the
  pattern, or use a regex such as `\d{3}\.\d{3}\.\d{3}`. Or the code and name are not separated
  by a double space.
- **Groups found but no details:** tick marks sit in another column, or read `BTB750`,
  `^BTB 750` etc. Print sample rows and loosen the test (match `BTB` case-insensitively, or
  `^`).
- **Subtotal mismatch after restructuring:** the original subtotal was typed, not summed, or a
  detail line lacks its tick mark. List the detail values and flag for auditor attention.
- **Grand total differs from the TB:** orphaned rows outside all groups, rounding, or TB
  adjustments not in the schedule. List the orphans (row, description, CY value) for review.
- **Formatting not applying:** check worksheet protection before formatting.

## Checklist

- [ ] Master backup made before any change
- [ ] Group inventory shown and approved before writing
- [ ] Subtotals moved below their details; codes stripped from names
- [ ] SUM formulas (not typed numbers) in every subtotal
- [ ] Variance (F) and materiality (G) formulas on every subtotal row
- [ ] "Material" rows flagged for the auditor
- [ ] Grand total built from the subtotal rows and reconciled to the TB
- [ ] No formula errors; user visually confirmed
