---
name: audit-monthly-summary
description: Build a GL monthly summary by adding Net Balance and Month helper columns to a transaction detail sheet and a two-column SUMIF-driven Monthly Analysis sheet reconciled to the trial balance - use when the user asks for a monthly analysis or monthly summary of a general ledger account.
---

# Audit monthly summary

Read `audit-conventions` first.

Live mode edits the open workbook and needs the user's `audit-skills approve` first. Before
each write, show the user what will be written (columns, formulas, rows) and wait for
approval; verify after writing; save only when the user asks (`audit-conventions` §8).

## Default format

The monthly analysis has two parts:

1. **Transaction Detail sheet** - add two helper columns: Net Balance and Month.
2. **Monthly Analysis sheet** - a two-column summary: Month | Total, twelve month rows plus a
   Grand Total row.

No account-level breakdown unless the user explicitly asks for one. Never hardcode column
letters, and never assume a column is free - detect both.

## Part 1 - enhance the Transaction Detail sheet

### 1. Back up

Make a backup copy of the workbook before any change.

### 2. Ask for the column locations

Always ask; never assume:

```
To create the monthly analysis, identify these columns in the Transaction Detail sheet:
1. DATE COLUMN - which column holds transaction dates? (e.g. E)
2. DEBIT COLUMN - which column holds debit amounts? (e.g. J)
3. CREDIT COLUMN - which column holds credit amounts? (e.g. K)
```

Store the answers in variables and use the variables in every formula:

```python
date_col = 'E'      # from the user
debit_col = 'J'     # from the user
credit_col = 'K'    # from the user
```

### 3. Find the last row

```python
last_row = sheet.range('A' + str(sheet.cells.last_cell.row)).end('up').row
```

### 4. Find empty columns for the helpers (dynamic)

Search from the column after the Credit column for the first completely empty column for
Net Balance, then the next empty column for Month:

```python
def col_letter_to_index(col):
    index = 0
    for char in col:
        index = index * 26 + (ord(char.upper()) - ord('A') + 1)
    return index - 1

def col_index_to_letter(index):
    letter = ''
    while index >= 0:
        letter = chr(index % 26 + ord('A')) + letter
        index = index // 26 - 1
    return letter

def is_column_empty(sheet, col_letter, last_row):
    values = sheet.range(f'{col_letter}1:{col_letter}{last_row}').value
    return all(v is None for v in values) if isinstance(values, list) else values is None

search_start = col_letter_to_index(credit_col) + 1
net_balance_col = next(
    (c for c in (col_index_to_letter(i) for i in range(search_start, search_start + 20))
     if is_column_empty(sheet, c, last_row)), None)
if net_balance_col is None:            # fall back to the column after the last used column
    net_balance_col = col_index_to_letter(sheet.used_range.last_cell.column)

month_search = col_letter_to_index(net_balance_col) + 1
month_col = next(
    (c for c in (col_index_to_letter(i) for i in range(month_search, month_search + 20))
     if is_column_empty(sheet, c, last_row)), None)
if month_col is None:
    month_col = col_index_to_letter(col_letter_to_index(net_balance_col) + 1)
```

Report the chosen columns to the user before writing.

### 5. Add the Net Balance column

Header `Net Balance` in row 1; formula `={debit}2-{credit}2` down to the last data row:

```python
sheet.range(f'{net_balance_col}1').value = 'Net Balance'
formula = f'={debit_col}2-{credit_col}2'
sheet.range(f'{net_balance_col}2:{net_balance_col}{last_row}').formula = formula
```

The formula is built from the user's column letters, so it works with any file layout.

### 6. Detect the date format and add the Month column

Read a sample date first and pick the matching formula - never guess the format:

| Date stored as | Example | Month formula for row 2 |
|---|---|---|
| Text DD/MM/YY | `31/01/25` | `=TEXT(DATE(2000+RIGHT(E2,2), MID(E2,4,2), LEFT(E2,2)), "mmm yyyy")` |
| Text DD/MM/YYYY | `31/01/2025` | `=TEXT(DATE(RIGHT(E2,4), MID(E2,4,2), LEFT(E2,2)), "mmm yyyy")` |
| Text YYYY-MM-DD, serial number or datetime | `2025-01-31`, `44927` | `=TEXT(E2, "mmm yyyy")` |

```python
sample = sheet.range(f'{date_col}2').value
if isinstance(sample, str) and '/' in sample and len(sample.split('/')[2]) == 2:
    date_formula = (f'=TEXT(DATE(2000+RIGHT({date_col}2,2), '
                    f'MID({date_col}2,4,2), LEFT({date_col}2,2)), "mmm yyyy")')
elif isinstance(sample, str) and '/' in sample:
    date_formula = (f'=TEXT(DATE(RIGHT({date_col}2,4), '
                    f'MID({date_col}2,4,2), LEFT({date_col}2,2)), "mmm yyyy")')
else:                                   # serial, datetime or other text
    date_formula = f'=TEXT({date_col}2, "mmm yyyy")'

sheet.range(f'{month_col}1').value = 'Month'
sheet.range(f'{month_col}2:{month_col}{last_row}').formula = date_formula
```

### 7. Verify the helpers

Read back the first few rows and show the user. Expected shape (illustrative figures):

```
Headers: ['Net Balance', 'Month']
Row 2: Net Balance = 250,000.00, Month = Jan 2025
Row 3: Net Balance = 262,500.00, Month = Jan 2025
Row 4: Net Balance = 275,000.00, Month = Feb 2025
```

## Part 2 - create the Monthly Analysis sheet

### 8. Create the sheet

If `Monthly Analysis` already exists, clear it; otherwise add it after the Transaction Detail
sheet:

```python
if 'Monthly Analysis' in [s.name for s in wb.sheets]:
    ws = wb.sheets['Monthly Analysis']
    ws.clear()
else:
    ws = wb.sheets.add('Monthly Analysis', after='Transaction Detail')
```

### 9. Headers, months and SUMIF totals

- A1 `Month`, B1 `Total` - bold, Arial, grey shading D9D9D9 on the header row.
- A2:A13 the twelve months, in exactly the text format the Month helper column produces
  (`Jan 2025` ... `Dec 2025`; build the list from the period the user gives).
- One SUMIF per month row, using the dynamic helper columns:

```python
ws.range('A1').value = 'Month'
ws.range('B1').value = 'Total'

year = '2025'                         # from the period the user gives
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
ws.range('A2').value = [[f'{m} {year}'] for m in months]

for i in range(2, 14):
    ws.range(f'B{i}').formula = (
        f"=SUMIF('Transaction Detail'!{month_col}:{month_col}, A{i}, "
        f"'Transaction Detail'!{net_balance_col}:{net_balance_col})")
```

The SUMIF looks up the month label in the Month helper column and sums the matching Net
Balance values, so every total is formula-driven - never typed.

### 10. Grand total

```python
ws.range('A14').value = 'Grand Total'
ws.range('B14').formula = '=SUM(B2:B13)'
```

Bold the row, black text, grey shading D9D9D9. No other colours.

### 11. Number format

```python
ws.range('B2:B14').number_format = '#,##0.00'
```

## Part 3 - reconciliation (mandatory)

1. Ask the user for the Trial Balance total for the account.
2. Compare it with the Grand Total in B14; the variance must be nil (tolerance 0.01).
3. If a variance exists, likely causes: rows with missing or invalid dates (the Month column
   is blank or an error), transactions excluded from the source data, or month labels that do
   not match exactly (`Jan 2025` vs `January 2025` or `01/2025`). Filter the Month helper
   column for blanks and errors and investigate before signing off.

Expected layout (illustrative round figures):

```
Month        | Total
Jan 2025     |    800,000.00
Feb 2025     |    850,000.00
Mar 2025     |    900,000.00
Apr 2025     |    870,000.00
May 2025     |    880,000.00
Jun 2025     |    840,000.00
Jul 2025     |    860,000.00
Aug 2025     |    830,000.00
Sep 2025     |    865,000.00
Oct 2025     |    875,000.00
Nov 2025     |    890,000.00
Dec 2025     |    790,000.00
Grand Total  | 10,250,000.00   =SUM(B2:B13), must equal the TB total
```

## Rules

1. Ask for the Date, Debit and Credit columns - never hardcode.
2. Detect empty columns - never assume fixed positions for the helpers.
3. Keep every column reference in a variable and use it in every formula.
4. Detect the date format before writing the Month formula.
5. Totals are SUMIF/SUM formulas, never typed numbers.
6. Twelve month rows plus a Grand Total row; no account-level detail unless requested.
7. The Grand Total must reconcile to the Trial Balance.

## Checklist

- [ ] Column locations obtained from the user
- [ ] Helper columns placed in genuinely empty columns
- [ ] Net Balance and Month formulas fill every data row without errors
- [ ] Monthly Analysis sheet: Month | Total, 12 rows, Grand Total
- [ ] All totals formula-driven; numbers formatted `#,##0.00`
- [ ] Grand Total reconciles to the TB (variance nil)
- [ ] User visually confirmed the result
