---
name: audit-planning-questionnaire
description: Restructure a verbose audit planning questionnaire (IT environment / gathering information) from an expanded multi-row layout into a compact, bordered three-panel table in working-paper format. Use when a sheet holds raw questionnaire text spread over many rows and must become an auditable planning document.
---

# Audit planning questionnaire transformation

Read `audit-conventions` first.

Excel edits follow `audit-conventions` §8: live mode edits an open workbook and needs the user's `audit-skills approve` first; show the user what will be written and wait for approval; verify after.

## Purpose

Transform a raw, verbose questionnaire sheet (e.g. "Sheet1") into a compact questionnaire table in the "Gathering Information" style: bordered rows, merged column panels, grey section dividers, and a three-panel response area.

## Safety protocol

- **Backup first** - always, before clearing or writing anything.
- **Terminal preview** - show the layout to the user before executing.
- **Wait for approval** - explicit "yes" / "go ahead" required.
- **Verify after** - read-back check plus error scan.
- **Rollback** - restore the backup if verification fails or the user reports issues.

## Target sheet structure

The finished sheet always uses columns **A through V (22 columns)**:

```
Col A      width 4   question number (narrow)
Col B:H    width 8   "Inquiry with management" (question text, 7 cols)
Col I:O    width 8   "Description" (management response, 7 cols)
Col P:V    width 8   "Risk" (auditor risk assessment, 7 cols)
```

### Row layout (38 rows, condensed from roughly 171 raw rows)

```
Row 1     Title row    - Merged A:V, bold, 11pt
Row 2     Empty
Row 3     Info row     - "Name of interviewee:"     label in B (bold)
Row 4     Info row     - "Position of interviewee:" label in B (bold)
Row 5     Info row     - "Date completed:"          label in B (bold)
Row 6-7   Empty
Row 8     Header row   - A8 grey | B8:H8 "Inquiry with management" |
                        I8:O8 "Description" | P8:V8 "Risk"
                        All: grey D9D9D9, bold, 11pt, all borders
Row 9     Q1
Row 10    SECTION: "Use of Information Technology"
Row 11    SECTION: "IT applications"
Row 12    Q2
Row 13    Q3
Row 14    SECTION: "IT infrastructure"
Row 15-19 Q4-Q8
Row 20    SECTION: "IT processes"
Row 21    Q9
Row 22    Q10
Row 23    SECTION: "Evaluation of complexity of the IT environment"
Row 24-34 Q11-Q21
Row 35    Empty
Row 36    SECTION: "Conclusion"
Row 37    Conclusion Q1 - "Your assessment of the complexity..."
Row 38    Conclusion Q2 - "Are specialised skills in IT required..."
```

### Formatting rules

| Element | Format |
|---------|--------|
| Title (row 1) | A:V merged, bold, 11pt |
| Info labels (rows 3-5) | Bold, 11pt, in column B only |
| Column headers (row 8) | Grey D9D9D9, bold, 11pt, all borders |
| Section dividers | A:V merged, grey D9D9D9, bold, 11pt, all borders, height 15pt |
| Question rows | A = number; B:H merged; I:O merged; P:V merged; all borders; wrap text; vertical align top; height 45pt |
| Conclusion rows | Same as question rows (column A left blank) |

## Question text reference (IT environment questionnaire)

"Consider:" sub-items are folded into the question cell as multi-line text using `\n` - exactly how the reference gathering-information sheet stores them.

```python
QUESTIONS = [
    (1,  'Select the type of risk assessment procedures performed:\n'
         '(Consider: Inquiries, Observations, Inspections)'),
    (2,  'Primary accounting software used to initiate, record, process and '
         'report transactions to prepare financial statements.'),
    (3,  'Other IT applications used to initiate, record, process and report '
         'transactions to prepare financial statements.\n'
         '(Consider: IT applications used in business operations that provides '
         'data to accounting software., Web-facing IT applications., IT applications '
         'that interacts with vendors or external parties through the internet.)'),
    (4,  'Nature of the underlying IT infrastructure affecting the financial '
         'reporting process.\n'
         '(Consider: Networks used to transmit and share data, resources and services '
         'through a common communication link., Operating system responsible for managing '
         'communications between hardware, IT applications, and other software used on '
         'the network.)'),
    (5,  'Format of how data is stored digitally, the location of data stored and how '
         'data is extracted between different data sources.\n'
         '(Consider: Local storage., Remote storage., Cloud storage., Databases, i.e. '
         'where data used by IT applications are stored., Use of data warehouses, being '
         'a central repository of integrated data from one or more disparate source such '
         'as multiple databases., Use of report-writer to extract data from various '
         'sources, such as data warehouse or application.)'),
    (6,  'Nature of access by users to data in the identified data sources.\n'
         '(Consider: IT personnel with database administration privileges., Access '
         'through IT applications, such as a data warehouse., Direct access without '
         'using the IT applications.)'),
    (7,  'Nature and extent of use of emerging technologies, such as blockchain, '
         'robotics or artificial intelligence.'),
    (8,  'Nature and extent of input of data through interfaces '
         '(i.e. input not done manually).\n'
         '(Consider: Customer or vendor input through interface such as applications., '
         'File upload.)'),
    (9,  'Number and skill level of the IT personnel that manage access, security '
         'and changes to the IT environment.'),
    (10, 'Use of internal or external service providers.\n'
         '(Consider: Third-party hosting or outsourcing of IT., Use of shared service '
         'centre for central management of IT processes in a group.)'),
    (11, 'Are accounting software developed in-house?'),
    (12, 'Are IT applications other than the primary accounting software used to '
         'initiate, record, process, correct, transfer or record transactions?'),
    (13, "Does the entity's underlying IT infrastructure include mainframe, web-facing "
         "elements, transactions involving external interfaces, or software and "
         "infrastructure as a cloud service?"),
    (14, 'Can any of the data used to prepare financial statements be accessed directly '
         'by users without using the accounting software or IT applications?'),
    (15, 'Is data stored digitally, stored in database(s) or data warehouses?'),
    (16, 'Does the entity process large volume of data or complex data?'),
    (17, 'Are processing of transactions in any of the financial reporting processes '
         'highly-automated?'),
    (18, 'Are processing of transactions in any of the financial reporting processes '
         'paperless?'),
    (19, 'Does the entity place reliance on system-generated reports to initiate and '
         'process information?'),
    (20, 'Is data used in the information system captured by external parties or through '
         'automated procedures?\n'
         '(Consider: Input by customers or vendors., File load., Interfaces.)'),
    (21, 'Is the entity using emerging technologies that affects its financial reporting?\n'
         '(Consider: Blockchain., Robotics., Artificial intelligence., To obtain a '
         'sufficient understanding of the IT applications and other relevant aspects of '
         'the IT environment., To determine the risks related to the use of IT., '
         'Identify general IT controls.)'),
]

CONCLUSION_ROWS = [
    'Your assessment of the complexity of the IT environment:',
    'Are specialised skills in IT required to obtain the understanding of the IT '
    'applications and other aspects of the IT environment?\n'
    '(Consider: To obtain a sufficient understanding of the IT applications and other '
    'relevant aspects of the IT environment., To determine the risks related to the '
    'use of IT., Identify general IT controls.)',
]
```

## Transformation script

Run as a scratch script outside the workpaper folders. Confirm the workbook and target sheet with the user, and create a timestamped backup before running.

```python
import xlwings as xw

wb = xw.Book('<workbook>.xlsx')   # confirm with the user - never assume
ws = wb.sheets['<target sheet>']

# 1. Constants
GRAY = (217, 217, 217)            # D9D9D9 - the only shading used

QUESTIONS = [...]                 # as per the reference above
CONCLUSION_ROWS = [...]

# 2. Helper functions
def apply_borders(rng, weight=2):
    for b in [7, 8, 9, 10]:       # left, top, bottom, right
        rng.api.Borders(b).LineStyle = 1
        rng.api.Borders(b).Weight = weight

def section_header(row, text):
    r = ws.range(f'A{row}:V{row}')
    r.merge()
    ws.range(f'A{row}').value = text
    r.color = GRAY
    r.api.Font.Bold = True
    r.api.Font.Size = 11
    apply_borders(r)
    ws.range(f'A{row}').row_height = 15

def question_row(row, num, text):
    a = ws.range(f'A{row}')
    a.value = num if num != '' else None
    a.api.Font.Size = 11
    apply_borders(a)
    for start, end in [('B', 'H'), ('I', 'O'), ('P', 'V')]:
        panel = ws.range(f'{start}{row}:{end}{row}')
        panel.merge()
        panel.api.WrapText = True
        if start == 'B':
            ws.range(f'B{row}').value = text
        panel.api.VerticalAlignment = -4160   # xlTop
        apply_borders(panel)
    ws.range(f'A{row}').row_height = 45

# 3. Clear and set column widths
ws.clear()
ws.range('A1').column_width = 4
for c in 'BCDEFGHIJKLMNOPQRSTUV':
    ws.range(c + '1').column_width = 8

# 4. Title and info rows
ws.range('A1:V1').merge()
ws.range('A1').value = 'Kindly assist with the following questions'
ws.range('A1').api.Font.Bold = True
ws.range('A1').api.Font.Size = 11
for row in (2, 6, 7):
    ws.range(f'A{row}').row_height = 13.8
for row, label in [(3, 'Name of interviewee:'), (4, 'Position of interviewee:'),
                   (5, 'Date completed:')]:
    ws.range(f'B{row}').value = label
    ws.range(f'B{row}').api.Font.Bold = True
    ws.range(f'B{row}').api.Font.Size = 11

# 5. Header row 8 (all panels: grey D9D9D9, bold, bordered)
for start, end, text in [('A', 'A', None), ('B', 'H', 'Inquiry with management'),
                         ('I', 'O', 'Description'), ('P', 'V', 'Risk')]:
    rng = ws.range(f'{start}8:{end}8')
    if start != end:
        rng.merge()
    if text:
        ws.range(f'{start}8').value = text
    rng.color = GRAY
    rng.api.Font.Bold = True
    rng.api.Font.Size = 11
    apply_borders(rng)

# 6. Questions and section dividers
question_row(9, 1, QUESTIONS[0][1])
section_header(10, 'Use of Information Technology')
section_header(11, 'IT applications')
question_row(12, 2, QUESTIONS[1][1])
question_row(13, 3, QUESTIONS[2][1])
section_header(14, 'IT infrastructure')
for i, idx in enumerate(range(3, 8)):        # Q4-Q8
    question_row(15 + i, QUESTIONS[idx][0], QUESTIONS[idx][1])
section_header(20, 'IT processes')
question_row(21, 9, QUESTIONS[8][1])
question_row(22, 10, QUESTIONS[9][1])
section_header(23, 'Evaluation of complexity of the IT environment')
for i, idx in enumerate(range(10, 21)):     # Q11-Q21
    question_row(24 + i, QUESTIONS[idx][0], QUESTIONS[idx][1])

# 7. Conclusion section
ws.range('A35').row_height = 13.8
section_header(36, 'Conclusion')
question_row(37, '', CONCLUSION_ROWS[0])
question_row(38, '', CONCLUSION_ROWS[1])

wb.save()
print('Done. 38 rows written.')
```

## Verification script

Run after the transformation to confirm all cells are correct:

```python
checks = [
    ('A1',  'value',  'Kindly assist with the following questions'),
    ('A1',  'merge',  '$A$1:$V$1'),
    ('B3',  'value',  'Name of interviewee:'),
    ('B8',  'value',  'Inquiry with management'),
    ('B8',  'merge',  '$B$8:$H$8'),
    ('I8',  'value',  'Description'),
    ('I8',  'merge',  '$I$8:$O$8'),
    ('P8',  'value',  'Risk'),
    ('P8',  'merge',  '$P$8:$V$8'),
    ('A9',  'value',  1.0),
    ('A10', 'value',  'Use of Information Technology'),
    ('A11', 'value',  'IT applications'),
    ('A14', 'value',  'IT infrastructure'),
    ('A20', 'value',  'IT processes'),
    ('A23', 'value',  'Evaluation of complexity of the IT environment'),
    ('A36', 'value',  'Conclusion'),
]

passed = failed = 0
for addr, check_type, expected in checks:
    cell = ws.range(addr)
    actual = (cell.api.MergeArea.Address if check_type == 'merge' else cell.value)
    ok = (actual == expected)
    passed, failed = passed + ok, failed + (not ok)
    print(f'  [{"PASS" if ok else "FAIL"}] {addr} {check_type}: {actual!r}')

errors = []
for cell in ws.range('A1:V38'):
    v = str(cell.value) if cell.value else ''
    if v in ['#REF!', '#NAME?', '#VALUE!', '#DIV/0!', '#N/A']:
        errors.append(f'{cell.address}: {v}')

print(f'\nChecks: {passed} passed, {failed} failed')
print(f'Errors: {len(errors)}')
print(f'Used range: {ws.used_range.address}')
```

## Terminal preview

Show this layout to the user before executing:

```
+---------------- AUDIT PLANNING QUESTIONNAIRE - WRITE PREVIEW ---------------+
|  Workbook: [filename.xlsx]    Sheet: [Sheet1]    Range: A1:V38             |
+------------------------------------------------------------------------------+

 A  |  B--------H (Inquiry)  |  I--------O (Description)  |  P--------V (Risk)
 ----+-----------------------+--------------------------+---------------------
 R1  | Kindly assist... [A:V merged, bold]
 R2  | (empty)
 R3  | [B] Name of interviewee: (bold)
 R4  | [B] Position of interviewee: (bold)
 R5  | [B] Date completed: (bold)
 R6-7| (empty)
 R8  | [GRAY] Inquiry...     | [GRAY] Description        | [GRAY] Risk
 R9  |  1 | Select the type...  |                        |
 R10 | [GRAY] Use of Information Technology
 R11 | [GRAY] IT applications
 R12 |  2 | Primary accounting...|                        |
 ...   ... (Q3-Q34 per the row layout)
 R35 | (empty)
 R36 | [GRAY] Conclusion
 R37 |    | Your assessment...   |                        |
 R38 |    | Are specialised...   |                        |

 38 rows total | Question rows: height 45pt, wrap, all borders
 Section headers: grey D9D9D9, bold, A:V merged, height 15pt
```

## Adapting for different questionnaires

1. **`QUESTIONS` list** - update the text and numbers.
2. **`CONCLUSION_ROWS` list** - update the conclusion question text.
3. **Section header rows** - add/remove `section_header(row, text)` calls.
4. **`question_row(row, num, text)` calls** - re-map the row numbers.

The column layout, formatting and helper functions stay the same - only the content and row assignments change.

**Variant: two-column response (no Risk column).** Change the headers to B8:H8 "Inquiry with management" and I8:V8 "Management response", and make `question_row` merge B:H for the question and I:V for the response.

## Rollback

If anything looks wrong after execution, restore the workbook from the timestamped backup taken before the run and re-examine the approach with the user.

## Quick reference

```
COLUMN MAP      A=num | B:H=Inquiry | I:O=Description | P:V=Risk
SHADING         Grey D9D9D9 only (headers and section dividers)
ROW HEIGHT      Question rows = 45pt | Section headers = 15pt | Other = 13.8pt
FONT            Size 11pt throughout
BORDERS         apply_borders() on every cell/merged range (all four sides)
SECTION ROWS    A:V merged, grey, bold, all borders
QUESTION ROWS   3 merged panels + bordered col A + wrap text + top alignment
TOTAL ROWS      38 (title + info + header + 21 Qs + 6 section dividers + conclusion)
```
