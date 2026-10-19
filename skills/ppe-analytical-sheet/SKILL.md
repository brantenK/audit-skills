---
name: ppe-analytical-sheet
description: Rebuilds the Analytical (movement analysis) sheet of a PPE audit working paper - exact row and column layout, border rules, tick-mark structure, group sub-totals and totals reconciliation to the trial balance - use when creating or updating the Analytical tab of any PPE working paper.
---

# PPE analytical sheet

Read `audit-conventions` first.

## Purpose

The Analytical sheet provides a movement analysis of Property, Plant and Equipment. It reconciles:

- Each GL account (Cost + Accumulated Depreciation) to the Trial Balance
- Current year (Prelim + Adjustments = Final CY) to Prior Year (PY)
- Grand total to the Balance per Financial Statements (AFS)

Do not pre-load account groups, account codes or balances. Every group, account and figure on this sheet comes from the client's source TB/analytical file for the current engagement. Treat the examples below (e.g. Land, Buildings, Vehicles, `<account>`, `<balance>`) as illustrative only.

## Prerequisites

1. Read `audit-conventions`, especially section 8 (Excel mode).
2. Confirm the active workbook with the user. Live mode edits an open workbook and needs the user's `audit-skills approve <workbook>` first; show the user what will be written, wait for approval, and verify after writing.
3. Identify the source TB/analytical file - it contains the account codes, prelim, adjustments, rep and PY figures.
4. Identify the PPE working paper target file.

## Step 0: Read the source data file

Before touching the working paper, read the source TB file to extract the account groups and figures:

```python
import xlwings as xw
# Use the source TB/analytical file confirmed with the user
wb_src = xw.Book('<Section> TB FY<yyyy>.xlsx')   # replace with actual filename
sheet_src = wb_src.sheets[0]
data = sheet_src.range('A1:H60').value
for i, row in enumerate(data, start=1):
    if any(v is not None for v in row):
        print(f'Row {i}: {row}')
```

Extract per account group:

| Column | Meaning |
|---|---|
| A | Account code + name (e.g. `<account> - <description>`) |
| C | Prelim balance |
| D | Adjustments |
| E | Rep (Final CY = Prelim + Adj) |
| G | PY comparative |

Group rows (subtotal rows) are typically prefixed with a CaseWare section number (e.g. `300.305.010 <Group>`). GL detail rows sit below the group header line.

## Step 1: Read the template's existing structure

Before clearing anything, inspect the current working paper to understand which rows contain data, where the column headers are (usually row 58), and where the conclusion block is (so you do not overwrite it):

```python
# Use the working paper filename confirmed with the user
wb = xw.Book('<Section> Testing FY<yyyy>.xlsx')   # replace with actual filename
sheet = wb.sheets['Analytical']
data = sheet.range('A55:L120').value
for i, row in enumerate(data, start=55):
    if any(v is not None for v in row):
        print(f'Row {i}: {row}')
```

Also check the column header row (row 58) to confirm:

- Col D = "Prelim"
- Col E = "Adjustments"
- Col F = CY label (e.g. `Final - <yyyy>`)
- Col I = PY label (e.g. `Rep <mm/yy>`)

## Step 2: Understand the column layout

| Column | Content |
|---|---|
| A | Account name / Group name |
| B, C | (empty) |
| D | Prelim balance |
| E | Adjustments |
| F | Final / Rep CY (= Prelim + Adj) |
| G | Tick mark CY (e.g. `BTB 305`) |
| H | (empty) |
| I | Prior Year comparative |
| J | Tick mark PY (e.g. `BPYTB`) |
| K | % Change formula |
| L | Comment / explanation |

Approximate column widths:

| Col | Width | Col | Width |
|---|---|---|---|
| A | 20.33 | G | 18.22 |
| B | 13.78 | H | 8.11 |
| C | 15.44 | I | 15.22 |
| D | 17.56 | J | 8.11 |
| E | 14.11 | K | 8.11 |
| F | 16.56 | L | 8.11 |

## Step 3: Row layout per account group

Each group follows this exact pattern:

```
Row N:     GL detail line 1 (e.g. Cost account)
Row N+1:   GL detail line 2 (e.g. Acc Depreciation account)
Row N+2:   GL detail line 3 (if applicable, e.g. Land)
...
Row X:     SUBTOTAL row (group name, bold, top+bottom borders)
Row X+1:   CARET row (^ symbols)
Row X+2:   BLANK separator row
```

Important:

- Each group starts immediately after the previous group's blank row (no extra blank before GL lines)
- Data rows start at row 59 (row 58 is the column header row)
- Groups flow continuously with only 1 blank row between them

## Step 4: Formatting rules

All text black, Arial. Grey shading only if any shading is used (D9D9D9 headers, F2F2F2 sub-totals) - see `audit-conventions` section 3.

Number format (used for D, E, F, I columns):

```python
NUM_FMT = '_(* #,##0.00_);_(* (#,##0.00);_(* "-"??_);_(@_)'
```

GL detail row:

- Font: not bold
- Number format: `NUM_FMT` for D, E, F, I; text format (`@`) for Col A
- Horizontal alignment: left for A, right for D/E/F/I
- Bottom border: single line (`xlContinuous = 1`, `Weight = 2`) on columns A through I
- No top border

```python
def set_border_bottom(api, linestyle, weight=2):
    api.Borders(9).LineStyle = linestyle
    # CRITICAL: do NOT set Weight if linestyle is DOUBLE (-4119) — COM error
    if linestyle != NONE_B and linestyle != DOUBLE:
        api.Borders(9).Weight = weight
```

Subtotal row:

- Font: bold
- Number format: `NUM_FMT` for D, E, F, I; `@` for A
- Horizontal alignment: left for A, right for D/E/F/I/G
- Top border: single line on A through I (Weight = 2)
- Bottom border: double line on A through I (`LineStyle = -4119`, NO weight - setting weight on a double border causes a COM error)
- Col K: % change formula, format `0%`, bold

Caret row:

- Values: `^` in columns D, E, F, I only
- Font: black, bold
- Alignment: center (`-4108`)
- Top border: double line on D, E, F, I (carries the double bottom from the subtotal above)
- No Weight on double borders

Tick mark cells (Col G = CY, Col J = PY):

- GL detail rows: `BTB [section]` in G (e.g. `BTB 305`), `BPYTB` in J
- Subtotal rows: G is blank (bold, with borders), J is blank
- Totals rows: `BTB` in G, `BPYTB` in J (Balance per above); `BAFS` in G, `BPYAFS` in J (Balance per FS)

## Step 5: Tick mark formatting

Tick mark structure per `audit-conventions` / `methodology/conventions.yaml`: bold anchor letter (B or V, 11pt), superscript source part (TB, PYTB, AFS, GL - 10pt, superscript), CaseWare reference number on the baseline (10pt, never superscripted). All text black - no colour values.

Apply the formatting to all tick mark cells after writing:

```python
XLBOTTOM = -4107

def apply_tick_fmt(sheet, addr):
    cell = sheet.range(addr)
    value = str(cell.value) if cell.value else ''
    if not value or len(value) < 2 or value[0] not in ['B', 'V']:
        return

    # Find where letters end and digits begin
    letter_end = 0
    number_start = -1
    for i, ch in enumerate(value):
        if ch.isdigit():
            number_start = i
            break
        elif ch == ' ' and i + 1 < len(value) and value[i+1].isdigit():
            number_start = i
            break
        else:
            letter_end = i + 1

    api = cell.api
    api.Font.Bold = True   # black text only - never set a font colour

    # Anchor character (B or V): 11pt, normal
    ch_a = api.GetCharacters(Start=1, Length=1)
    ch_a.Font.Size = 11
    ch_a.Font.Superscript = False

    # Superscript letters (TB, PYTB, AFS, GL etc): 10pt, superscript
    if letter_end > 1:
        ch_s = api.GetCharacters(Start=2, Length=letter_end - 1)
        ch_s.Font.Size = 10
        ch_s.Font.Superscript = True

    # Reference number (e.g. 305, 420): 10pt, NOT superscript, on the baseline
    if number_start > 0:
        ch_n = api.GetCharacters(Start=number_start + 1, Length=len(value) - number_start)
        ch_n.Font.Size = 10
        ch_n.Font.Superscript = False

    api.VerticalAlignment = XLBOTTOM

# Apply to all tick columns after writing:
for r in range(59, last_row + 1):
    for col in ['G', 'J']:
        val = sheet.range(f'{col}{r}').value
        if val and str(val)[0] in ['B', 'V']:
            apply_tick_fmt(sheet, f'{col}{r}')
```

## Step 6: Balance totals rows

Two rows appear after all groups (with a blank separator row):

Balance per above:

- Col A: `Balance per above`
- Col D/E/F/I: SUM of all group subtotal values (use `=SUM()` formulas)
- Col G: `BTB`; Col J: `BPYTB`
- No borders

Balance per financial statements:

- Col A: `Balance per financial statements`
- Col D/E/F/I: mirrors Balance per above (formulas referencing the row above)
- Col D/E/F/I/A: bottom single border
- Col G: `BAFS`; Col J: `BPYAFS`
- Col K: % change formula, bold, `0%` format
- Col L: overall movement explanation

Apply tick mark formatting to G and J on both rows.

## Step 7: Conclusion block

After the totals rows, add (with blank rows between):

```
[blank]
[blank]
Summary of fixed asset register
[blank]
Refer to [FAR cross-reference]   <- e.g. "305.40"
[blank]
Conclusion                        <- bold
[blank]
Based on procedures performed and results obtained, we have reasonable assurance that
there were no significant or unusual movements in property, plant and equipment for
[Client] for the year ended [Year End]. The overall [increase/decrease] of X.XX%
is attributable to [explanation]. No material misstatements were identified.
```

## Step 8: Comments (column L)

Add comments on subtotal rows only (not GL detail rows):

| Movement | Comment template |
|---|---|
| Increase | `Increase due to capitalisation of <category> during the year.` |
| Decrease (depreciation only) | `Decrease due to depreciation charged during the year.` |
| Decrease (disposal + depreciation) | `Decrease due to depreciation and disposal of <category> during the year.` |
| Large decrease (>30%) | Note if assets reaching end of useful life |

Do not write an explanation you have not confirmed - if the reason for a movement is unknown, write it as a question for the client (`audit-conventions` section 6).

## Step 9: Reconciliation check

Always verify before handing over:

```python
# Read back the subtotal row values from the sheet and sum them
# Compare against the known grand total from the source TB file
subtotal_rows = [r for r in group_rows]  # list of subtotal row numbers
cy_total = sum(sheet.range(f'F{r}').value for r in subtotal_rows)
py_total = sum(sheet.range(f'I{r}').value for r in subtotal_rows)

# Compare to expected totals from source file
assert abs(cy_total - expected_cy_total) < 0.05, f'CY total mismatch: {cy_total} vs {expected_cy_total}'
assert abs(py_total - expected_py_total) < 0.05, f'PY total mismatch: {py_total} vs {expected_py_total}'
print(f'Grand total reconciles: CY={cy_total:,.2f}, PY={py_total:,.2f}')
```

## Critical gotchas

1. **Double border + Weight = COM error.** Never set `Weight` when `LineStyle = -4119` (xlDouble); set the LineStyle only - the weight is implicit for double borders.
2. **ClearFormats before rewriting.** Always clear both contents AND formats before writing to a range: `sheet.range('A59:L130').clear_contents()` then `...api.ClearFormats()`.
3. **Write long scripts to a .py file, not inline.** For scripts longer than about 30 lines, write to a file in the tool's temp folder and run it - this avoids shell quoting/escaping errors.
4. **Always read the backup first.** Before rebuilding, read from the backup/original to verify the original row structure (which rows had blank separators), border styles per row type, and number formats per column.
5. **Col J PY tick marks** (`BPYTB`) on GL detail rows are bold black text like all other tick marks; the superscript formatting is applied separately via `apply_tick_fmt()`.
6. **Col A on subtotal rows uses `@` (text) format**, not `General` - this preserves the text value and stops Excel treating it as a number.

## Full working code template

Black text only; grey fills only (D9D9D9 / F2F2F2) if shading is needed.

```python
import xlwings as xw

NUM_FMT  = '_(* #,##0.00_);_(* (#,##0.00);_(* "-"??_);_(@_)'
PCT_FMT  = '0%'
TEXT_FMT = '@'
XLEFT    = -4131
XRIGHT   = -4152
XCENTER  = -4108
XLBOTTOM = -4107
CONT     = 1       # xlContinuous
DOUBLE   = -4119   # xlDouble
NONE_B   = -4142   # xlNone

def set_border_bottom(api, linestyle, weight=2):
    api.Borders(9).LineStyle = linestyle
    if linestyle != NONE_B and linestyle != DOUBLE:
        api.Borders(9).Weight = weight

def set_border_top(api, linestyle, weight=2):
    api.Borders(8).LineStyle = linestyle
    if linestyle != NONE_B and linestyle != DOUBLE:
        api.Borders(8).Weight = weight

def write_gl_detail(sheet, row, acct_name, prelim, adj, rep_cy, tick_cy, py, tick_py):
    a = sheet.range(f'A{row}')
    a.value = acct_name
    a.api.Font.Bold = False
    a.number_format = TEXT_FMT
    a.api.HorizontalAlignment = XLEFT
    set_border_bottom(a.api, CONT)

    for col, val in [('D', prelim), ('E', adj), ('F', rep_cy)]:
        c = sheet.range(f'{col}{row}')
        c.value = val
        c.api.Font.Bold = False
        c.number_format = NUM_FMT
        c.api.HorizontalAlignment = XRIGHT
        set_border_bottom(c.api, CONT)

    if tick_cy:
        g = sheet.range(f'G{row}')
        g.value = tick_cy
        g.api.Font.Bold = False
        g.api.HorizontalAlignment = XLEFT
        g.number_format = 'General'
        set_border_bottom(g.api, CONT)

    ic = sheet.range(f'I{row}')
    ic.value = py
    ic.api.Font.Bold = False
    ic.number_format = NUM_FMT
    ic.api.HorizontalAlignment = XRIGHT
    set_border_bottom(ic.api, CONT)

    if tick_py:
        j = sheet.range(f'J{row}')
        j.value = tick_py
        j.api.Font.Bold = False
        j.api.HorizontalAlignment = XLEFT
        j.number_format = 'General'

def write_subtotal(sheet, row, name, prelim, adj, rep_cy, py):
    a = sheet.range(f'A{row}')
    a.value = name
    a.api.Font.Bold = True
    a.number_format = TEXT_FMT
    a.api.HorizontalAlignment = XLEFT
    set_border_top(a.api, CONT)
    set_border_bottom(a.api, DOUBLE)

    for col, val in [('D', prelim), ('E', adj), ('F', rep_cy)]:
        c = sheet.range(f'{col}{row}')
        c.value = val
        c.api.Font.Bold = True
        c.number_format = NUM_FMT
        c.api.HorizontalAlignment = XRIGHT
        set_border_top(c.api, CONT)
        set_border_bottom(c.api, DOUBLE)

    g = sheet.range(f'G{row}')
    g.api.Font.Bold = True
    g.api.HorizontalAlignment = XRIGHT
    g.number_format = NUM_FMT
    set_border_top(g.api, CONT)
    set_border_bottom(g.api, DOUBLE)

    ic = sheet.range(f'I{row}')
    ic.value = py
    ic.api.Font.Bold = True
    ic.number_format = NUM_FMT
    ic.api.HorizontalAlignment = XRIGHT
    set_border_top(ic.api, CONT)
    set_border_bottom(ic.api, DOUBLE)

    # % change as a formula, not a typed number
    k = sheet.range(f'K{row}')
    k.formula = f'=IF(I{row}=0,"",(F{row}-I{row})/ABS(I{row}))'
    k.api.Font.Bold = True
    k.number_format = PCT_FMT

def write_caret_row(sheet, row):
    for col in ['D', 'E', 'F', 'I']:
        c = sheet.range(f'{col}{row}')
        c.value = '^'
        c.api.Font.Bold = True   # black text only
        c.api.HorizontalAlignment = XCENTER
        c.number_format = NUM_FMT
        c.api.Borders(8).LineStyle = DOUBLE  # top border = double (no weight!)

def apply_tick_fmt(sheet, addr):
    cell = sheet.range(addr)
    value = str(cell.value) if cell.value else ''
    if not value or len(value) < 2 or value[0] not in ['B', 'V']:
        return
    letter_end = 0
    number_start = -1
    for i, ch in enumerate(value):
        if ch.isdigit():
            number_start = i; break
        elif ch == ' ' and i + 1 < len(value) and value[i+1].isdigit():
            number_start = i; break
        else:
            letter_end = i + 1
    try:
        api = cell.api
        api.Font.Bold = True
        ch_a = api.GetCharacters(Start=1, Length=1)
        ch_a.Font.Size = 11; ch_a.Font.Superscript = False
        if letter_end > 1:
            ch_s = api.GetCharacters(Start=2, Length=letter_end - 1)
            ch_s.Font.Size = 10; ch_s.Font.Superscript = True
        if number_start > 0:
            ch_n = api.GetCharacters(Start=number_start + 1, Length=len(value) - number_start)
            ch_n.Font.Size = 10; ch_n.Font.Superscript = False
        api.VerticalAlignment = XLBOTTOM
    except Exception as e:
        print(f'Tick error {addr}: {e}')
```
