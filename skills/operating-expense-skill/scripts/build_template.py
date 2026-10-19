"""
Expense Testing Working Paper Template Builder
===============================================
Self-contained script. Fill in the PARAMS dict below and run: python build_template.py

Creates an 8-sheet audit working paper template:
  1. Procedures
  2. Analytical
  3. Occurrence - Material
  4. Occurrence - Sensitive
  5. Completeness
  6. Cut-off
  7. Journals
  8. Presentation

Formatting: Arial, black text, grey shading only (D9D9D9 headers, F2F2F2 sub-totals).
"""

import xlwings as xw
import re
import sys
from datetime import datetime
from dateutil.relativedelta import relativedelta

# ============================================================
# PARAMETERS — EDIT THIS BLOCK ONLY
# ============================================================
PARAMS = {
    'section_number': '750.55',           # e.g., '750.55', '750.40', '620.10'
    'section_name': 'Other expenses',     # e.g., 'Other expenses', 'Employee costs'
    'client_name': 'Test Client Ltd',     # from the engagement config
    'year_end': '2025-12-31',             # YYYY-MM-DD format
    'performance_materiality': 1000000,   # from the engagement config — synthetic example
    'clearly_trivial': 50000,             # from the engagement config — synthetic example, must be < PM
    'mode': 'placeholder',                # 'caseware' or 'placeholder'
    'category_type': 'Category A',        # 'Category A' or 'Category C'
    'risk_level': 'Low',                  # 'Low', 'Medium', or 'High'
}
# ============================================================


# ============================================================
# CONSTANTS
# ============================================================
FONT_NAME = 'Arial'
FONT_SIZE = 10
# Repo convention: grey shading only. Hex values are the only allowed fills.
HEADER_FILL = 0xD9D9D9    # section headers and table column headers
SUBTOTAL_FILL = 0xF2F2F2 # sub-total rows
NUM_FMT_ACCOUNTING = '_(* #,##0.00_);_(* (#,##0.00);_(* "-"??_);_(@_)'
NUM_FMT_PERCENT = '0.00%'
XLBOTTOM = -4107
XL_EDGE_TOP = 8
XL_EDGE_BOTTOM = 9
XL_CONTINUOUS = 1
XL_DOUBLE = -4119
XL_THIN = 2

COLUMN_WIDTHS = {
    'A': 25, 'B': 12, 'C': 15, 'D': 12, 'E': 15, 'F': 12,
    'G': 15, 'H': 12, 'I': 12, 'J': 12, 'K': 18, 'L': 18,
    'M': 15, 'N': 10, 'O': 15, 'P': 12,
    'R': 10, 'S': 10, 'T': 10, 'U': 10, 'V': 10, 'W': 10, 'X': 10,
}

# Standard audit procedures (Sheet 1)
PROCEDURES = [
    {
        'number': '1',
        'text': 'Significant risk responses',
        'sub_items': [
            ('a', 'Consider whether lease assessment is applicable to this expense category'),
            ('b', 'Evaluate management judgments and estimates'),
        ],
        'ref': '',
        'assertion': 'Risk assessment',
    },
    {
        'number': '2',
        'text': 'Obtain list of {section_name} with comparatives and perform analytical review',
        'sub_items': [
            ('a', 'Obtain the list of {section_name} for the current year and prior year'),
            ('b', 'Compare current year to prior year and investigate significant fluctuations'),
            ('c', 'Agree totals to the trial balance'),
            ('d', 'Agree totals to the annual financial statements'),
        ],
        'ref': 'Analytical',
        'assertion': 'Accuracy, Valuation',
    },
    {
        'number': '3',
        'text': 'Completeness of population',
        'sub_items': [
            ('a', 'Obtain the general ledger for {section_name}'),
            ('b', 'Trace the GL closing balance to the trial balance'),
            ('c', 'Verify completeness of the population by checking sequential references'),
        ],
        'ref': 'Completeness',
        'assertion': 'Completeness',
    },
    {
        'number': '4',
        'text': 'Select material and/or sensitive items for testing',
        'sub_items': [
            ('a', 'Identify all material items (individual amounts >= Performance Materiality)'),
            ('b', 'Identify sensitive items (e.g., related party, unusual nature)'),
            ('c', 'Select additional items using systematic selection if required'),
            ('d', 'Test selected items to supporting documentation'),
        ],
        'ref': 'Occurence - Material\nOccurence - Sensitive',
        'assertion': 'Occurrence, Accuracy',
    },
    {
        'number': '5',
        'text': 'Perform cut-off testing',
        'sub_items': [
            ('a', 'Select expenses recorded shortly before and after year-end'),
            ('b', 'Verify that transactions are recorded in the correct financial period'),
            ('c', 'Check supporting documentation for date accuracy'),
        ],
        'ref': 'Cut off',
        'assertion': 'Cut-off',
    },
    {
        'number': '6',
        'text': 'Review journal entries',
        'sub_items': [
            ('a', 'Identify material or unusual journal entries for {section_name}'),
            ('b', 'Check approval and authorization evidence'),
            ('c', 'Verify supporting documentation for journals'),
        ],
        'ref': 'Journals',
        'assertion': 'Occurrence, Accuracy',
    },
    {
        'number': '7',
        'text': 'Presentation and disclosure',
        'sub_items': [
            ('a', 'Review draft AFS for compliance with IFRS for SMEs'),
            ('b', 'Verify expense classification and aggregation'),
            ('c', 'Check related party disclosures'),
            ('d', 'Verify accounting policy disclosures'),
        ],
        'ref': 'Presentation',
        'assertion': 'Presentation, Classification',
    },
    {
        'number': '8',
        'text': 'Extended tests of detail (if required)',
        'sub_items': [
            ('a', 'Perform additional testing based on risk assessment results'),
            ('b', 'Document findings and any exceptions'),
        ],
        'ref': '',
        'assertion': 'As required',
    },
    {
        'number': '9',
        'text': 'Scrutinise the general ledger',
        'sub_items': [
            ('a', 'Review the GL for unusual entries, large balances, or abnormal patterns'),
            ('b', 'Investigate any unusual or unexpected items identified'),
        ],
        'ref': '',
        'assertion': 'All assertions',
    },
    {
        'number': '10',
        'text': 'Scrutinise source documents',
        'sub_items': [
            ('a', 'Review supporting documentation for reasonableness'),
            ('b', 'Verify authorization and approval'),
        ],
        'ref': '',
        'assertion': 'Occurrence, Accuracy',
    },
]


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def validate_parameters(params):
    """Validate all parameters. Returns list of error strings."""
    errors = []
    if not re.match(r'^\d+\.\d+$', str(params.get('section_number', ''))):
        errors.append("section_number must match Digits.Digits (e.g., '750.55')")
    if not params.get('section_name', '').strip():
        errors.append("section_name must be a non-empty string")
    if not params.get('client_name', '').strip():
        errors.append("client_name must be a non-empty string")
    try:
        datetime.strptime(str(params.get('year_end', '')), '%Y-%m-%d')
    except (ValueError, TypeError):
        errors.append("year_end must be YYYY-MM-DD format")
    pm = None
    try:
        pm = float(params.get('performance_materiality', 0))
        if pm <= 0:
            errors.append("performance_materiality must be > 0")
    except (ValueError, TypeError):
        errors.append("performance_materiality must be a positive number")
    try:
        ct = float(params.get('clearly_trivial', 0))
        if ct <= 0:
            errors.append("clearly_trivial must be > 0")
        elif pm is not None and ct >= pm:
            errors.append("clearly_trivial must be < performance_materiality")
    except (ValueError, TypeError):
        errors.append("clearly_trivial must be a positive number")
    if params.get('mode', '') not in ('caseware', 'placeholder'):
        errors.append("mode must be 'caseware' or 'placeholder'")
    if params.get('category_type', '') not in ('Category A', 'Category C'):
        errors.append("category_type must be 'Category A' or 'Category C'")
    if params.get('risk_level', '') not in ('Low', 'Medium', 'High'):
        errors.append("risk_level must be 'Low', 'Medium', or 'High'")
    return errors


def apply_font(cell, bold=False, size=FONT_SIZE, name=FONT_NAME):
    """Apply font settings to a cell. Text is always black (repo convention)."""
    cell.api.Font.Name = name
    cell.api.Font.Size = size
    if bold:
        cell.api.Font.Bold = True


def apply_header_fill(cell):
    """Grey D9D9D9 shading + bold, for section headers and table column headers."""
    cell.api.Interior.Color = HEADER_FILL
    cell.api.Font.Bold = True


def apply_subtotal_fill(cell):
    """Grey F2F2F2 shading + bold, for sub-total rows."""
    cell.api.Interior.Color = SUBTOTAL_FILL
    cell.api.Font.Bold = True


def set_single_bottom(cell_api):
    """Apply single thin bottom border."""
    cell_api.Borders(XL_EDGE_BOTTOM).LineStyle = XL_CONTINUOUS
    cell_api.Borders(XL_EDGE_BOTTOM).Weight = XL_THIN


def set_double_bottom(cell_api):
    """Apply double bottom border. Do NOT set Weight — causes COM crash."""
    cell_api.Borders(XL_EDGE_BOTTOM).LineStyle = XL_DOUBLE


def set_single_top(cell_api):
    """Apply single thin top border."""
    cell_api.Borders(XL_EDGE_TOP).LineStyle = XL_CONTINUOUS
    cell_api.Borders(XL_EDGE_TOP).Weight = XL_THIN


def set_all_borders(sheet, range_str):
    """Apply thin borders on all edges of every cell in range."""
    rng = sheet.range(range_str)
    for border_id in [7, 8, 9, 10]:  # Left, Top, Bottom, Right
        rng.api.Borders(border_id).LineStyle = XL_CONTINUOUS
        rng.api.Borders(border_id).Weight = XL_THIN


def set_column_widths(sheet):
    """Apply standard column widths."""
    for col, width in COLUMN_WIDTHS.items():
        sheet.range(f'{col}:{col}').column_width = width


def write_header_rows(sheet, params):
    """Write rows 1-3 (client info, sign-off, section). Mode-dependent."""
    mode = params['mode']
    sn = params['section_number']

    # Row 1: Client name + sign-off labels
    if mode == 'caseware':
        sheet.range('A1').formula = "=[1]!'CWEval|active|CLP2|'"
    else:
        sheet.range('A1').value = params['client_name']
        sheet.range('A1').api.Font.Bold = True

    sheet.range('G1').value = 'Prepared by'
    sheet.range('H1').value = 'First review'
    sheet.range('I1').value = 'Performed by'
    sheet.range('J1').value = 'Final review'
    sheet.range('K1').value = sn
    sheet.range('L1').value = sn

    # Row 2: Year End + user names
    sheet.range('A2').value = 'Year End:'
    if mode == 'caseware':
        sheet.range('B2').formula = "=[1]!'CWEval|active|SDATE(CLP13)|'"
        for col, idx in [('G', 1), ('H', 2), ('I', 3), ('J', 4)]:
            sheet.range(f'{col}2').formula = (
                f'=IF([1]!\'CWEval|active|CWDIUser{idx}("FILENAME")|\'=0,"",'
                f'[1]!\'CWEval|active|CWDIUser{idx}("FILENAME")|\')'
            )
    else:
        sheet.range('B2').value = params['year_end']
        for col in ['G', 'H', 'I', 'J']:
            sheet.range(f'{col}2').value = ''

    # Row 3: Section + user dates
    sheet.range('A3').value = 'Section:'
    sheet.range('B3').value = params['section_name']
    sheet.range('B3').api.Font.Bold = True
    if mode == 'caseware':
        for col, idx in [('G', 1), ('H', 2), ('I', 3), ('J', 4)]:
            sheet.range(f'{col}3').formula = (
                f'=IF([1]!\'CWEval|active|CWDIDate{idx}("FILENAME")|\'=0,"",'
                f'[1]!\'CWEval|active|CWDIDate{idx}("FILENAME")|\')'
            )
    else:
        for col in ['G', 'H', 'I', 'J']:
            sheet.range(f'{col}3').value = ''


def write_title_block(sheet, title):
    """Write rows 4-6: sheet title."""
    sheet.range('A4').value = title
    sheet.range('A4').api.Font.Bold = True
    sheet.range('A4').api.Font.Size = 11
    # Rows 5-6 blank


def write_objective_block(sheet, objective_text):
    """Write rows 7-10: Objective section."""
    apply_header_fill(sheet.range('A7'))
    sheet.range('A7').value = 'Objective:'
    # Row 8 blank
    sheet.range('A9').value = objective_text
    # Row 10 blank


def write_risk_assessment(sheet, params):
    """Write rows 11-18: Audit risk block."""
    risk = params['risk_level']

    sheet.range('A11').value = 'Audit risk:'
    sheet.range('A11').api.Font.Bold = True
    # Row 12 blank
    sheet.range('A13').value = (
        'The risk assessment is based on inherent risk, fraud risk and control risk. '
        'The overall risk assessment is the aggregate of these risks. '
        'The risk assessment determines the nature, timing and extent of further audit procedures.'
    )

    # Row 14-16: Risk components
    labels = ['Inherent risk assessment', 'Fraud risk assessment', 'Control risk assessment']
    for i, (row, label) in enumerate(zip([14, 15, 16], labels)):
        sheet.range(f'B{row}').value = label
        sheet.range(f'B{row}').api.Font.Bold = True
        sheet.range(f'D{row}').value = risk
        sheet.range(f'E{row}').formula = f'=VLOOKUP(D{row},$F$14:$G$16,2,FALSE)'

    # Lookup table F14:G16
    sheet.range('F14').value = 'Low'
    sheet.range('G14').value = 1
    sheet.range('F15').value = 'Medium'
    sheet.range('G15').value = 2
    sheet.range('F16').value = 'High'
    sheet.range('G16').value = 3

    # Row 17: Material misstatement
    sheet.range('B17').value = 'Risk of material misstatement'
    sheet.range('B17').api.Font.Bold = True
    sheet.range('D17').formula = '=IF(E17<=3,"Low",IF(E17<=6,"Medium","High"))'
    sheet.range('E17').formula = '=SUM(E14:E16)'

    # Row 18: Explanation
    sheet.range('A18').value = (
        'Based on the risk assessment above, the risk of material misstatement is determined. '
        'The higher the risk assessment, the more extensive the audit procedures required.'
    )


def write_sample_matrix(sheet, params):
    """Write rows 19-28: Sample size matrix."""
    cat = params['category_type']
    risk = params['risk_level']

    # Row 19: blank
    # Row 20: Headers
    sheet.range('A20').value = 'Sample Size:'
    sheet.range('A20').api.Font.Bold = True
    sheet.range('D20').value = 'Category A'
    sheet.range('G20').value = 'Category C'

    # Row 21: Sub-headers
    for col in ['D', 'E', 'G', 'H']:
        sheet.range(f'{col}21').api.Font.Bold = True
    sheet.range('D21').value = 'Size'
    sheet.range('E21').value = 'Coverage'
    sheet.range('G21').value = 'Size'
    sheet.range('H21').value = 'Coverage'

    # Rows 22-24: Matrix data
    matrix = {
        22: ('Low',    10, 0.4,  8,  0.4),
        23: ('Medium', 20, 0.55, 15, 0.5),
        24: ('High',   30, 0.7,  25, 0.6),
    }
    for row, (label, ca_s, ca_c, cc_s, cc_c) in matrix.items():
        sheet.range(f'A{row}').value = label
        sheet.range(f'D{row}').value = ca_s
        sheet.range(f'E{row}').value = ca_c
        sheet.range(f'E{row}').number_format = '0%'
        sheet.range(f'G{row}').value = cc_s
        sheet.range(f'H{row}').value = cc_c
        sheet.range(f'H{row}').number_format = '0%'

    # Row 25: Reason
    sheet.range('A25').value = 'Reason for sample size selected:'
    # Row 26: blank

    # Row 27: Number VLOOKUP
    sheet.range('A27').value = '  -  Number'
    if cat == 'Category A':
        sheet.range('D27').formula = f'=VLOOKUP("{risk}",A22:D24,4,FALSE)'
    else:
        sheet.range('D27').formula = f'=VLOOKUP("{risk}",A22:G24,7,FALSE)'

    # Row 28: Coverage VLOOKUP
    sheet.range('A28').value = '  -  Coverage'
    if cat == 'Category A':
        sheet.range('D28').formula = f'=VLOOKUP("{risk}",A22:E24,5,FALSE)'
    else:
        sheet.range('D28').formula = f'=VLOOKUP("{risk}",A22:H24,8,FALSE)'
    sheet.range('D28').number_format = '0%'


def write_materiality(sheet, params, is_procedures_sheet=False):
    """Write rows 29-30: PM and Clearly Trivial."""
    mode = params['mode']
    sn = params['section_number']

    sheet.range('A29').value = 'Performance materiality:'
    sheet.range('A30').value = 'Clearly trivial:'

    if mode == 'caseware' and not is_procedures_sheet:
        sheet.range('D29').formula = f"='{sn} Procedures'!D29"
        sheet.range('D30').formula = f"='{sn} Procedures'!D30"
    else:
        sheet.range('D29').value = params['performance_materiality']
        sheet.range('D30').value = params['clearly_trivial']

    sheet.range('D29').number_format = NUM_FMT_ACCOUNTING
    sheet.range('D30').number_format = NUM_FMT_ACCOUNTING


def write_universal_skeleton(sheet, params, title, objective, is_procedures_sheet=False):
    """Write rows 1-30 (universal skeleton) on any sheet."""
    write_header_rows(sheet, params)
    write_title_block(sheet, title)
    write_objective_block(sheet, objective)
    write_risk_assessment(sheet, params)
    write_sample_matrix(sheet, params)
    write_materiality(sheet, params, is_procedures_sheet)
    set_column_widths(sheet)

    # Set font on all used cells so far
    for row in range(1, 31):
        for col_letter in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']:
            cell = sheet.range(f'{col_letter}{row}')
            if cell.value is not None:
                cell.api.Font.Name = FONT_NAME
                cell.api.Font.Size = FONT_SIZE


def write_footer(sheet, start_row, params):
    """Write universal footer: Notes, Legends, Conclusion, Results."""
    r = start_row + 2  # 2 blank rows
    sn = params['section_name']
    ye = params['year_end']

    # Notes
    apply_header_fill(sheet.range(f'A{r}'))
    sheet.range(f'A{r}').value = 'Notes:'
    r += 2  # blank + blank

    # Legends
    apply_header_fill(sheet.range(f'A{r}'))
    sheet.range(f'A{r}').value = 'Legends:'
    r += 1

    # Tick marks: bold anchor, superscript source part, baseline reference number.
    # All text black — no colour values (repo convention).
    legends = [
        ('BTB', 'Agreed to trial balance'),
        ('BAFS', 'Agreed to annual financial statements'),
        ('BPYTB', 'Agreed to prior year trial balance'),
        ('BPYAFS', 'Agreed to prior year annual financial statements'),
        ('\u2211', 'Recalculated'),
        ('^CC', 'Cross Casts'),
        ('^', 'Casts'),
    ]
    for tick, desc in legends:
        cell = sheet.range(f'A{r}')
        cell.value = f'{tick} - {desc}'
        cell.api.Font.Bold = True
        cell.api.Font.Name = FONT_NAME
        cell.api.Font.Size = FONT_SIZE
        r += 1

    r += 1  # blank

    # Conclusion
    apply_header_fill(sheet.range(f'A{r}'))
    sheet.range(f'A{r}').value = 'Conclusion:'
    r += 1

    sheet.range(f'A{r}').value = (
        f'Based on the procedures performed and results obtained, {sn} '
        f'are not materially misstated for the relevant assertions for the year ended '
        f'{ye}. No material misstatements were identified.'
    )
    sheet.range(f'A{r}').api.Font.Name = FONT_NAME
    sheet.range(f'A{r}').api.Font.Size = FONT_SIZE
    r += 2

    # Results
    sheet.range(f'A{r}').value = 'Results:'
    sheet.range(f'A{r}').api.Font.Bold = True
    r += 1
    for line in [
        '  Auditors journals raised: N/A',
        '  Management letter points: N/A',
        '  Overs and unders journals raised: N/A',
        '  Other considerations: N/A',
    ]:
        sheet.range(f'A{r}').value = line
        sheet.range(f'A{r}').api.Font.Name = FONT_NAME
        sheet.range(f'A{r}').api.Font.Size = FONT_SIZE
        r += 1

    return r


def apply_tick_mark_formatting(sheet, cell_range):
    """Apply tick mark formatting to cells in range.

    Structure kept per repo convention: bold anchor letter (B or V, 11pt),
    superscript source part (TB, PYTB, GL, AFS, 10pt), CaseWare reference
    number on the baseline (10pt, never superscripted). All text black.
    """
    for cell in sheet.range(cell_range):
        value = str(cell.value) if cell.value else ''
        if not value or len(value) < 2 or value[0] not in ['B', 'V']:
            continue

        letter_end = 0
        number_start = -1
        for i, char in enumerate(value):
            if char.isdigit():
                number_start = i
                break
            elif char == ' ' and i + 1 < len(value) and value[i + 1].isdigit():
                number_start = i
                break
            else:
                letter_end = i + 1

        try:
            ec = cell.api
            ec.Font.Bold = True

            # Anchor: 11pt, normal
            ch = ec.GetCharacters(Start=1, Length=1)
            ch.Font.Size = 11
            ch.Font.Superscript = False

            # Superscript letters
            if letter_end > 1:
                ch2 = ec.GetCharacters(Start=2, Length=letter_end - 1)
                ch2.Font.Size = 10
                ch2.Font.Superscript = True

            # Reference number: baseline, never superscripted
            if number_start > 0:
                ch3 = ec.GetCharacters(Start=number_start + 1, Length=len(value) - number_start)
                ch3.Font.Size = 10
                ch3.Font.Superscript = False

            ec.VerticalAlignment = XLBOTTOM
        except Exception:
            pass


def calculate_cutoff_dates(year_end_str):
    """Calculate pre/post year-end date windows."""
    ye = datetime.strptime(year_end_str, '%Y-%m-%d')
    pre_start = ye - relativedelta(months=1)
    post_end = ye + relativedelta(months=1)
    return {
        'pre_start': pre_start.strftime('%d %B %Y'),
        'pre_end': ye.strftime('%d %B %Y'),
        'post_start': ye.strftime('%d %B %Y'),
        'post_end': post_end.strftime('%d %B %Y'),
        'year_end': ye.strftime('%d %B %Y'),
    }


# ============================================================
# SHEET BUILDERS
# ============================================================

def build_procedures_sheet(wb, params):
    """Build Sheet 1: Procedures."""
    sn = params['section_number']
    sec = params['section_name']
    sheet_name = f'{sn} Procedures'
    sheet = wb.sheets.add(sheet_name)

    title = f'{sec}: Procedures'
    objective = f'To ensure that {sec} are complete, occurred and accounted for correctly.'
    write_universal_skeleton(sheet, params, title, objective, is_procedures_sheet=True)

    r = 32
    apply_header_fill(sheet.range(f'A{r}'))
    sheet.range(f'A{r}').value = 'Audit work:'
    r += 2

    # Column headers
    sheet.range(f'A{r}').value = 'Procedure'
    sheet.range(f'L{r}').value = 'Reference'
    sheet.range(f'M{r}').value = 'Assertion'
    for col in ['A', 'L', 'M']:
        apply_header_fill(sheet.range(f'{col}{r}'))
    r += 1

    # Procedures
    for proc in PROCEDURES:
        text = proc['text'].replace('{section_name}', sec)
        sheet.range(f'A{r}').value = f"{proc['number']}. {text}"
        sheet.range(f'A{r}').api.Font.Bold = True
        sheet.range(f'L{r}').value = proc['ref']
        sheet.range(f'M{r}').value = proc['assertion']
        r += 1
        for letter, sub_text in proc['sub_items']:
            sub_text = sub_text.replace('{section_name}', sec)
            sheet.range(f'A{r}').value = f"  {letter}) {sub_text}"
            r += 1
        r += 1  # blank between procedures

    write_footer(sheet, r, params)
    return sheet


def build_analytical_sheet(wb, params):
    """Build Sheet 2: Analytical."""
    sn = params['section_number']
    sec = params['section_name']
    sheet_name = f'{sn}-1 Analytical'
    sheet = wb.sheets.add(sheet_name)

    title = f'{sec}: Analytical'
    objective = 'To perform an analytical review to identify any unusual items for further investigation.'
    write_universal_skeleton(sheet, params, title, objective)

    r = 32
    apply_header_fill(sheet.range(f'A{r}'))
    sheet.range(f'A{r}').value = 'Audit work:'
    r += 2

    sheet.range(f'A{r}').value = 'Work performed:'
    sheet.range(f'A{r}').api.Font.Bold = True
    r += 1
    sheet.range(f'A{r}').value = f'1. Agreed the total of {sec} per the trial balance to the analytical review.'
    r += 1
    sheet.range(f'A{r}').value = '2. Compared current year to prior year and investigated significant fluctuations.'
    r += 1
    sheet.range(f'A{r}').value = '3. Agreed totals per below to the annual financial statements.'
    r += 2

    # Analytical Review header
    apply_header_fill(sheet.range(f'A{r}'))
    sheet.range(f'A{r}').value = 'Analytical Review:'
    sheet.range(f'D{r}').value = 'CY Year'
    sheet.range(f'D{r}').api.Font.Bold = True
    sheet.range(f'F{r}').value = 'PY Year'
    sheet.range(f'F{r}').api.Font.Bold = True
    r += 2

    # Balance rows
    first_detail = r + 6  # first detail row after header rows
    last_detail = first_detail + 14  # 15 detail rows

    sheet.range(f'A{r}').value = 'Balance as per trial balance'
    sheet.range(f'D{r}').value = ''  # user populates CY
    sheet.range(f'F{r}').value = 'BPYTB'
    sheet.range(f'G{r}').formula = f'=IFERROR((C{r}-E{r})/ABS(E{r}),"")'
    sheet.range(f'G{r}').number_format = NUM_FMT_PERCENT
    r += 1

    sheet.range(f'A{r}').value = 'Balance as per below'
    sheet.range(f'C{r}').formula = f'=SUM(C{first_detail}:C{last_detail})'
    sheet.range(f'E{r}').formula = f'=SUM(E{first_detail}:E{last_detail})'
    r += 1

    sheet.range(f'A{r}').value = 'Difference'
    sheet.range(f'C{r}').formula = f'=C{r-2}-C{r-1}'
    sheet.range(f'E{r}').formula = f'=E{r-2}-E{r-1}'
    r += 1

    sheet.range(f'G{r}').value = '^'
    sheet.range(f'G{r}').api.Font.Bold = True
    r += 2

    # Detail breakdown
    sheet.range(f'A{r}').value = 'Detail breakdown:'
    sheet.range(f'A{r}').api.Font.Bold = True
    r += 1

    # Column headers
    for col, header in [('A', 'Account'), ('C', 'CY Amount'), ('E', 'PY Amount'), ('G', 'Variance %')]:
        sheet.range(f'{col}{r}').value = header
        apply_header_fill(sheet.range(f'{col}{r}'))
    r += 1

    # 15 empty detail rows with formulas
    for i in range(15):
        row_num = r + i
        sheet.range(f'G{row_num}').formula = f'=IFERROR((C{row_num}-E{row_num})/ABS(E{row_num}),"")'
        sheet.range(f'G{row_num}').number_format = NUM_FMT_PERCENT
        sheet.range(f'C{row_num}').number_format = NUM_FMT_ACCOUNTING
        sheet.range(f'E{row_num}').number_format = NUM_FMT_ACCOUNTING
    r += 15

    # Subtotal row
    first = r - 15
    last = r - 1
    sheet.range(f'A{r}').value = 'Total'
    sheet.range(f'A{r}').api.Font.Bold = True
    sheet.range(f'C{r}').formula = f'=SUM(C{first}:C{last})'
    sheet.range(f'E{r}').formula = f'=SUM(E{first}:E{last})'
    sheet.range(f'C{r}').number_format = NUM_FMT_ACCOUNTING
    sheet.range(f'E{r}').number_format = NUM_FMT_ACCOUNTING
    sheet.range(f'G{r}').formula = f'=IFERROR((C{r}-E{r})/ABS(E{r}),"")'
    sheet.range(f'G{r}').number_format = NUM_FMT_PERCENT
    for col in ['A', 'C', 'E', 'G']:
        apply_subtotal_fill(sheet.range(f'{col}{r}'))
        set_double_bottom(sheet.range(f'{col}{r}').api)
    r += 1

    write_footer(sheet, r, params)
    return sheet


def _build_occurrence_sheet(wb, params, sheet_suffix, testing_label, procedure_text):
    """Shared builder for Occurrence-Material and Occurrence-Sensitive sheets."""
    sn = params['section_number']
    sec = params['section_name']
    sheet_name = f'{sn}-{sheet_suffix}'
    sheet = wb.sheets.add(sheet_name)

    title = f'{sec}: Occurrence'
    objective = f'To ensure that {sec} are not materially misstated for Occurrence, Accuracy and Classification.'
    write_universal_skeleton(sheet, params, title, objective)

    r = 32
    apply_header_fill(sheet.range(f'A{r}'))
    sheet.range(f'A{r}').value = 'Audit work:'
    r += 2

    sheet.range(f'A{r}').value = 'Procedure 4a-d:'
    sheet.range(f'A{r}').api.Font.Bold = True
    r += 1
    sheet.range(f'A{r}').value = procedure_text
    r += 2

    apply_header_fill(sheet.range(f'A{r}'))
    sheet.range(f'A{r}').value = testing_label
    r += 2

    # Merged header row (panel titles)
    sheet.range(f'A{r}').value = 'Per the GL'
    sheet.range(f'I{r}').value = 'Per the Supporting documents'
    sheet.range(f'R{r}').value = 'Work done'
    for col in ['A', 'I', 'R']:
        sheet.range(f'{col}{r}').api.Font.Bold = True
    r += 1

    # Column headers
    gl_headers = {'A': 'GL code', 'B': 'Date', 'C': 'Ref', 'D': 'Ref',
                  'E': 'Ref', 'F': 'Description', 'G': 'Amount excl VAT', 'H': ''}
    doc_headers = {'I': 'Date', 'J': 'Invoice #', 'K': 'Supplier', 'L': 'Description',
                   'M': 'Amount excl VAT', 'N': 'VAT', 'O': 'Amount incl VAT', 'P': 'Difference'}
    work_headers = {'R': 'VAT treated\ncorrectly', 'S': 'Recalculate\nVAT', 'T': 'Invoice\ncasts',
                    'U': 'Is expense\ncapital', 'V': 'In name of\ncompany', 'W': 'SARS\nrequirements',
                    'X': 'Classification\ncorrect'}

    for col, header in {**gl_headers, **doc_headers, **work_headers}.items():
        if header:
            sheet.range(f'{col}{r}').value = header
            apply_header_fill(sheet.range(f'{col}{r}'))
            sheet.range(f'{col}{r}').api.WrapText = True

    data_start = r + 1

    # 20 empty data rows with borders and difference formula
    for i in range(20):
        row_num = data_start + i
        sheet.range(f'P{row_num}').formula = f'=G{row_num}-O{row_num}'
        sheet.range(f'G{row_num}').number_format = NUM_FMT_ACCOUNTING
        sheet.range(f'M{row_num}').number_format = NUM_FMT_ACCOUNTING
        sheet.range(f'N{row_num}').number_format = NUM_FMT_ACCOUNTING
        sheet.range(f'O{row_num}').number_format = NUM_FMT_ACCOUNTING
        sheet.range(f'P{row_num}').number_format = NUM_FMT_ACCOUNTING

    data_end = data_start + 19

    # Borders on data range
    set_all_borders(sheet, f'A{data_start}:X{data_end}')

    r = data_end + 1

    # Subtotal row
    sheet.range(f'A{r}').value = 'Subtotal'
    sheet.range(f'A{r}').api.Font.Bold = True
    sheet.range(f'G{r}').formula = f'=SUM(G{data_start}:G{data_end})'
    sheet.range(f'O{r}').formula = f'=SUM(O{data_start}:O{data_end})'
    sheet.range(f'P{r}').formula = f'=SUM(P{data_start}:P{data_end})'
    for col in ['A', 'G', 'O', 'P']:
        apply_subtotal_fill(sheet.range(f'{col}{r}'))
        sheet.range(f'{col}{r}').number_format = NUM_FMT_ACCOUNTING
        set_double_bottom(sheet.range(f'{col}{r}').api)
    r += 2

    # Methodology block
    sheet.range(f'A{r}').value = 'Sample methodology:'
    sheet.range(f'A{r}').api.Font.Bold = True
    r += 1
    sheet.range(f'A{r}').value = 'Selection method: Systematic selection'
    r += 1
    sheet.range(f'A{r}').value = 'Reason:'
    r += 1
    sheet.range(f'A{r}').value = 'Total transactions in population:'
    sheet.range(f'G{r}').value = ''  # user populates
    r += 1
    sheet.range(f'A{r}').value = 'Sample size:'
    sheet.range(f'G{r}').value = ''  # user links to VLOOKUP
    r += 1
    sheet.range(f'A{r}').value = 'Interval:'
    pop_row = r - 2
    size_row = r - 1
    sheet.range(f'G{r}').formula = f'=IF(G{size_row}=0,"",G{pop_row}/G{size_row})'
    r += 1

    write_footer(sheet, r, params)
    return sheet


def build_occurrence_material_sheet(wb, params):
    """Build Sheet 3: Occurrence - Material."""
    return _build_occurrence_sheet(
        wb, params,
        sheet_suffix='2 Occurence - Material',
        testing_label='Material Items Testing:',
        procedure_text='Select material items (>= Performance Materiality) and test to supporting documentation.',
    )


def build_occurrence_sensitive_sheet(wb, params):
    """Build Sheet 4: Occurrence - Sensitive."""
    return _build_occurrence_sheet(
        wb, params,
        sheet_suffix='3 Occurence - Sensitive',
        testing_label='Sensitive Items Testing:',
        procedure_text='Select sensitive items (entertainment, fines, donations, related party, etc.) and test to supporting documentation.',
    )


def build_completeness_sheet(wb, params):
    """Build Sheet 5: Completeness."""
    sn = params['section_number']
    sec = params['section_name']
    sheet_name = f'{sn}-4 Completeness'
    sheet = wb.sheets.add(sheet_name)

    title = f'{sec}: Completeness'
    objective = f'To ensure that {sec} are not materially misstated for Completeness.'
    write_universal_skeleton(sheet, params, title, objective)

    r = 32
    apply_header_fill(sheet.range(f'A{r}'))
    sheet.range(f'A{r}').value = 'Audit work:'
    r += 2

    sheet.range(f'A{r}').value = 'Procedure 3:'
    sheet.range(f'A{r}').api.Font.Bold = True
    r += 1
    sheet.range(f'A{r}').value = f'Document the completeness and accuracy of the {sec} population.'
    r += 2

    apply_header_fill(sheet.range(f'A{r}'))
    sheet.range(f'A{r}').value = 'Work performed:'
    r += 1
    sheet.range(f'A{r}').value = f'1. Obtained the general ledger for {sec} from the client.'
    r += 1
    sheet.range(f'A{r}').value = '2. Traced the GL closing balance to the trial balance.'
    r += 1
    sheet.range(f'A{r}').value = '3. Verified that the total per the GL agrees to the total per the analytical review.'
    r += 2

    apply_header_fill(sheet.range(f'A{r}'))
    sheet.range(f'A{r}').value = 'Completeness Check:'
    r += 2

    # Table headers
    sheet.range(f'A{r}').value = 'Description'
    sheet.range(f'C{r}').value = 'Amount'
    for col in ['A', 'C']:
        apply_header_fill(sheet.range(f'{col}{r}'))
    r += 1

    sheet.range(f'A{r}').value = 'Balance per GL'
    sheet.range(f'C{r}').number_format = NUM_FMT_ACCOUNTING
    r += 1
    sheet.range(f'A{r}').value = 'Balance per Trial Balance'
    sheet.range(f'C{r}').number_format = NUM_FMT_ACCOUNTING
    r += 1
    sheet.range(f'A{r}').value = 'Difference'
    sheet.range(f'C{r}').formula = f'=C{r-2}-C{r-1}'
    sheet.range(f'C{r}').number_format = NUM_FMT_ACCOUNTING
    set_double_bottom(sheet.range(f'C{r}').api)
    r += 2

    sheet.range(f'A{r}').value = 'Result:'
    sheet.range(f'A{r}').api.Font.Bold = True
    r += 1
    sheet.range(f'A{r}').value = 'The balance per the GL agrees/differs to the balance per the trial balance.'
    r += 1
    sheet.range(f'A{r}').value = 'The population is therefore considered complete/incomplete.'
    r += 1

    write_footer(sheet, r, params)
    return sheet


def build_cutoff_sheet(wb, params):
    """Build Sheet 6: Cut-off."""
    sn = params['section_number']
    sec = params['section_name']
    sheet_name = f'{sn}-5 Cut off'
    sheet = wb.sheets.add(sheet_name)

    title = f'{sec}: Cut Off'
    objective = f'To ensure that {sec} are not materially misstated for Cut-off.'
    write_universal_skeleton(sheet, params, title, objective)

    dates = calculate_cutoff_dates(params['year_end'])

    r = 32
    apply_header_fill(sheet.range(f'A{r}'))
    sheet.range(f'A{r}').value = 'Audit work:'
    r += 2

    sheet.range(f'A{r}').value = 'Procedure 5:'
    sheet.range(f'A{r}').api.Font.Bold = True
    r += 1
    sheet.range(f'A{r}').value = (
        f'Select expenses recorded from {dates["pre_start"]} to {dates["post_end"]} '
        f'and verify correct period allocation.'
    )
    r += 2

    apply_header_fill(sheet.range(f'A{r}'))
    sheet.range(f'A{r}').value = 'Work performed:'
    r += 1
    sheet.range(f'A{r}').value = f'1. Selected expenses recorded in the period {dates["pre_start"]} to {dates["pre_end"]} (pre year-end).'
    r += 1
    sheet.range(f'A{r}').value = f'2. Selected expenses recorded in the period {dates["post_start"]} to {dates["post_end"]} (post year-end).'
    r += 1
    sheet.range(f'A{r}').value = '3. Verified that all selected expenses are recorded in the correct financial period.'
    r += 1
    sheet.range(f'A{r}').value = '4. Checked supporting documentation for date accuracy.'
    r += 2

    # Pre year-end testing
    apply_header_fill(sheet.range(f'A{r}'))
    sheet.range(f'A{r}').value = f'Pre Year-End Testing ({dates["pre_start"]} to {dates["pre_end"]}):'
    r += 2

    cutoff_headers = {'A': 'GL code', 'B': 'Date', 'C': 'Ref', 'D': 'Description',
                      'E': 'Amount excl VAT', 'F': 'Correct period (Y/N)', 'G': 'Comments'}
    for col, header in cutoff_headers.items():
        sheet.range(f'{col}{r}').value = header
        apply_header_fill(sheet.range(f'{col}{r}'))

    pre_header_row = r
    r += 1

    # 15 empty data rows
    pre_data_start = r
    for i in range(15):
        sheet.range(f'E{r + i}').number_format = NUM_FMT_ACCOUNTING
    pre_data_end = r + 14
    set_all_borders(sheet, f'A{pre_data_start}:G{pre_data_end}')
    r = pre_data_end + 2

    # Post year-end testing
    apply_header_fill(sheet.range(f'A{r}'))
    sheet.range(f'A{r}').value = f'Post Year-End Testing ({dates["post_start"]} to {dates["post_end"]}):'
    r += 2

    for col, header in cutoff_headers.items():
        sheet.range(f'{col}{r}').value = header
        apply_header_fill(sheet.range(f'{col}{r}'))
    r += 1

    post_data_start = r
    for i in range(15):
        sheet.range(f'E{r + i}').number_format = NUM_FMT_ACCOUNTING
    post_data_end = r + 14
    set_all_borders(sheet, f'A{post_data_start}:G{post_data_end}')
    r = post_data_end + 2

    sheet.range(f'A{r}').value = 'Result:'
    sheet.range(f'A{r}').api.Font.Bold = True
    r += 1
    sheet.range(f'A{r}').value = 'All expenses tested were recorded in the correct financial period / Exceptions noted above.'
    r += 1

    write_footer(sheet, r, params)
    return sheet


def build_journals_sheet(wb, params):
    """Build Sheet 7: Journals."""
    sn = params['section_number']
    sec = params['section_name']
    sheet_name = f'{sn}-6 Journals'
    sheet = wb.sheets.add(sheet_name)

    title = f'{sec}: Journals'
    objective = f'To ensure that {sec} are not materially misstated due to journals processed.'
    write_universal_skeleton(sheet, params, title, objective)

    r = 32
    apply_header_fill(sheet.range(f'A{r}'))
    sheet.range(f'A{r}').value = 'Audit work:'
    r += 2

    sheet.range(f'A{r}').value = 'Procedure 6:'
    sheet.range(f'A{r}').api.Font.Bold = True
    r += 1
    sheet.range(f'A{r}').value = f'Identify material or unusual journal entries for {sec} and verify approval and supporting evidence.'
    r += 2

    apply_header_fill(sheet.range(f'A{r}'))
    sheet.range(f'A{r}').value = 'Work performed:'
    r += 1
    sheet.range(f'A{r}').value = f'1. Obtained the list of journal entries affecting {sec} for the year.'
    r += 1
    sheet.range(f'A{r}').value = '2. Identified material journals (>= Performance Materiality).'
    r += 1
    sheet.range(f'A{r}').value = '3. Identified unusual journals (related party, round numbers, period-end entries).'
    r += 1
    sheet.range(f'A{r}').value = '4. Verified authorization and approval for selected journals.'
    r += 1
    sheet.range(f'A{r}').value = '5. Verified supporting documentation for selected journals.'
    r += 2

    apply_header_fill(sheet.range(f'A{r}'))
    sheet.range(f'A{r}').value = 'Journal Entry Testing:'
    r += 2

    # Table headers
    journal_headers = {
        'A': 'Journal #', 'B': 'Date', 'C': 'Description', 'D': 'Debit', 'E': 'Credit',
        'F': 'Prepared by', 'G': 'Approved by', 'H': 'Supporting docs (Y/N)',
        'I': 'Classification correct', 'J': 'Comments',
    }
    for col, header in journal_headers.items():
        sheet.range(f'{col}{r}').value = header
        apply_header_fill(sheet.range(f'{col}{r}'))
    r += 1

    # 20 empty data rows
    data_start = r
    for i in range(20):
        sheet.range(f'D{r + i}').number_format = NUM_FMT_ACCOUNTING
        sheet.range(f'E{r + i}').number_format = NUM_FMT_ACCOUNTING
    data_end = r + 19
    set_all_borders(sheet, f'A{data_start}:J{data_end}')
    r = data_end + 2

    sheet.range(f'A{r}').value = 'Result:'
    sheet.range(f'A{r}').api.Font.Bold = True
    r += 1
    sheet.range(f'A{r}').value = 'All journals tested were properly authorized and supported / Exceptions noted above.'
    r += 1

    write_footer(sheet, r, params)
    return sheet


def build_presentation_sheet(wb, params):
    """Build Sheet 8: Presentation."""
    sn = params['section_number']
    sec = params['section_name']
    sheet_name = f'{sn}-7 Presentation'
    sheet = wb.sheets.add(sheet_name)

    title = f'{sec}: Presentation and Disclosure'
    objective = f'To ensure that {sec} are presented and disclosed appropriately in the annual financial statements.'
    write_universal_skeleton(sheet, params, title, objective)

    r = 32
    apply_header_fill(sheet.range(f'A{r}'))
    sheet.range(f'A{r}').value = 'Audit work:'
    r += 2

    sheet.range(f'A{r}').value = 'Procedure 7:'
    sheet.range(f'A{r}').api.Font.Bold = True
    r += 1
    sheet.range(f'A{r}').value = f'Review the draft annual financial statements for appropriate presentation and disclosure of {sec}.'
    r += 2

    apply_header_fill(sheet.range(f'A{r}'))
    sheet.range(f'A{r}').value = 'Work performed:'
    r += 1
    sheet.range(f'A{r}').value = f'7a. Verified that {sec} are presented in the correct line item of the income statement.'
    r += 1
    sheet.range(f'A{r}').value = f'7b. Verified that {sec} are classified correctly between operating and non-operating items.'
    r += 1
    sheet.range(f'A{r}').value = '7c. Verified that related party transactions are disclosed in accordance with IFRS for SMEs Section 33.'
    r += 1
    sheet.range(f'A{r}').value = f'7d. Verified that accounting policies relevant to {sec} are disclosed.'
    r += 1
    sheet.range(f'A{r}').value = f'7e. Verified that any contingent liabilities arising from {sec} are disclosed.'
    r += 1
    sheet.range(f'A{r}').value = f'7f. Verified that the aggregation and offsetting of {sec} complies with IFRS for SMEs.'
    r += 2

    apply_header_fill(sheet.range(f'A{r}'))
    sheet.range(f'A{r}').value = 'Presentation and Disclosure Checklist:'
    r += 2

    # Checklist headers
    for col, header in [('A', 'Checklist Item'), ('B', 'IFRS for SMEs Ref'), ('C', 'Compliant (Y/N)'), ('D', 'Comments')]:
        sheet.range(f'{col}{r}').value = header
        apply_header_fill(sheet.range(f'{col}{r}'))
    r += 1

    # Checklist items
    checklist = [
        ('Correct line item in income statement', 'Section 5'),
        ('Classification (operating vs non-operating)', 'Section 5'),
        ('Related party disclosures', 'Section 33'),
        ('Accounting policy disclosures', 'Section 3'),
        ('Contingent liability disclosures', 'Section 21'),
        ('Aggregation and offsetting', 'Section 3.16'),
    ]
    for item, ref in checklist:
        sheet.range(f'A{r}').value = item
        sheet.range(f'B{r}').value = ref
        r += 1

    r += 1
    sheet.range(f'A{r}').value = 'Result:'
    sheet.range(f'A{r}').api.Font.Bold = True
    r += 1
    sheet.range(f'A{r}').value = f'Presentation and disclosure of {sec} is in accordance with IFRS for SMEs / Exceptions noted above.'
    r += 1

    write_footer(sheet, r, params)
    return sheet


# ============================================================
# VERIFICATION
# ============================================================

def verify_sheet_names(wb, section_number):
    """Verify all 8 sheets exist."""
    expected = [
        f'{section_number} Procedures',
        f'{section_number}-1 Analytical',
        f'{section_number}-2 Occurence - Material',
        f'{section_number}-3 Occurence - Sensitive',
        f'{section_number}-4 Completeness',
        f'{section_number}-5 Cut off',
        f'{section_number}-6 Journals',
        f'{section_number}-7 Presentation',
    ]
    actual = [s.name for s in wb.sheets]
    errors = [name for name in expected if name not in actual]
    if errors:
        print('FAIL: Missing sheets:')
        for e in errors:
            print(f'  - {e}')
        return False
    print('PASS: All 8 sheets present')
    return True


def verify_skeleton(wb, section_number, section_name):
    """Verify rows 1-30 skeleton consistency."""
    errors = []
    for s in wb.sheets:
        if s.range('A2').value != 'Year End:':
            errors.append(f'{s.name}: A2 wrong')
        if s.range('A3').value != 'Section:':
            errors.append(f'{s.name}: A3 wrong')
        if str(s.range('B3').value or '') != section_name:
            errors.append(f'{s.name}: B3 wrong')
        if 'Performance materiality' not in str(s.range('A29').value or ''):
            errors.append(f'{s.name}: A29 wrong')
    if errors:
        print('FAIL: Skeleton errors:')
        for e in errors:
            print(f'  - {e}')
        return False
    print('PASS: Skeleton consistent')
    return True


def verify_footers(wb):
    """Verify footer (Notes, Legends, Conclusion) on every sheet."""
    errors = []
    for s in wb.sheets:
        found = {'notes': False, 'legends': False, 'conclusion': False}
        for row in range(50, 300):
            val = str(s.range(f'A{row}').value or '')
            if val.startswith('Notes:'):
                found['notes'] = True
            if val.startswith('Legends:'):
                found['legends'] = True
            if val.startswith('Conclusion:'):
                found['conclusion'] = True
        for key, label in [('notes', 'Notes:'), ('legends', 'Legends:'), ('conclusion', 'Conclusion:')]:
            if not found[key]:
                errors.append(f'{s.name}: Missing "{label}"')
    if errors:
        print('FAIL: Footer errors:')
        for e in errors:
            print(f'  - {e}')
        return False
    print('PASS: All footers present')
    return True


def run_all_verifications(wb, params):
    """Run all verification checks."""
    sn = params['section_number']
    sec = params['section_name']
    print('=' * 60)
    print('TEMPLATE VERIFICATION')
    print('=' * 60)
    v1 = verify_sheet_names(wb, sn)
    v2 = verify_skeleton(wb, sn, sec)
    v3 = verify_footers(wb)
    print('=' * 60)
    if all([v1, v2, v3]):
        print('ALL VERIFICATIONS PASSED')
    else:
        print('SOME VERIFICATIONS FAILED')
    print('=' * 60)
    return all([v1, v2, v3])


# ============================================================
# MAIN
# ============================================================

def main():
    # 1. Validate parameters
    errors = validate_parameters(PARAMS)
    if errors:
        print('PARAMETER ERRORS:')
        for e in errors:
            print(f'  - {e}')
        sys.exit(1)
    print('Parameters validated OK')

    # 2. Create workbook
    wb = xw.Book()
    default = wb.sheets[0]
    default.name = '__delete__'

    # 3. Build all 8 sheets
    print('Building Procedures...')
    build_procedures_sheet(wb, PARAMS)
    print('Building Analytical...')
    build_analytical_sheet(wb, PARAMS)
    print('Building Occurrence - Material...')
    build_occurrence_material_sheet(wb, PARAMS)
    print('Building Occurrence - Sensitive...')
    build_occurrence_sensitive_sheet(wb, PARAMS)
    print('Building Completeness...')
    build_completeness_sheet(wb, PARAMS)
    print('Building Cut-off...')
    build_cutoff_sheet(wb, PARAMS)
    print('Building Journals...')
    build_journals_sheet(wb, PARAMS)
    print('Building Presentation...')
    build_presentation_sheet(wb, PARAMS)

    # 4. Delete placeholder sheet
    wb.sheets['__delete__'].delete()

    # 5. Verify
    run_all_verifications(wb, PARAMS)

    # 6. Save
    sn = PARAMS['section_number']
    sec = PARAMS['section_name']
    client = PARAMS['client_name']
    filename = f'{sn} {sec} - {client} Template.xlsx'
    wb.save(filename)
    print(f'\nSaved: {filename}')


if __name__ == '__main__':
    main()
