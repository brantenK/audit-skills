"""
Revenue Testing Working Paper Template Builder
===============================================
Self-contained script. Fill in the PARAMS dict below and run: python build_template.py

Creates a 7-sheet revenue audit working paper template:
  1. Procedures (ISA 240.26 fraud risk)
  2. Analytical
  3. Occurance,AAC (Invoice + Credit note testing)
  4. Completeness (Sequence testing + PO tracing)
  5. Cut Off (Sales + Credit notes pre/post YE)
  6. Journals (3-panel)
  7. Presentation

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
    'section_number': '700.40',           # e.g., '700.40', '700.55'
    'section_name': 'Revenue - Trading',  # e.g., 'Revenue - Trading', 'Revenue - Services'
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
SUBTOTAL_FILL = 0xF2F2F2 # sub-total and total rows
NUM_FMT_ACCOUNTING = '_(* #,##0.00_);_(* (#,##0.00);_(* "-"??_);_(@_)'
NUM_FMT_PERCENT = '0.00%'
XLBOTTOM = -4107
XL_EDGE_TOP = 8
XL_EDGE_BOTTOM = 9
XL_CONTINUOUS = 1
XL_DOUBLE = -4119
XL_THIN = 2

COLUMN_WIDTHS = {
    'A': 25, 'B': 15, 'C': 15, 'D': 12, 'E': 15, 'F': 12,
    'G': 15, 'H': 12, 'I': 12, 'J': 12, 'K': 18, 'L': 18,
    'M': 15, 'N': 10, 'O': 15, 'P': 12,
    'R': 10, 'S': 10, 'T': 10, 'U': 10, 'V': 10, 'W': 10, 'X': 10,
}

# Revenue-specific audit procedures
PROCEDURES = [
    {
        'number': '1',
        'text': 'Significant risk responses (Fraud)',
        'sub_items': [
            ('', 'Risk: Fraud in revenue recognition — per ISA 240.26, the auditor shall presume there is a significant risk due to fraud in revenue recognition.'),
            ('', 'Response: In order to address the fraud risk, we will perform the following:'),
            ('', '  - Credit note cut-off testing'),
            ('', '  - Detailed cut-off testing'),
            ('', '  - Testing of any journals in the revenue accounts'),
        ],
        'ref': 'Fraud',
        'assertion': 'All assertions',
    },
    {
        'number': '2',
        'text': 'Agree amounts and disclosures in current period financial statements (ISA 330.20 and .30)',
        'sub_items': [
            ('(a)', 'Trial balance (ISA 330.20 and .30)'),
            ('(b)', 'General ledger and control accounts (ISA 330.20 and .30)'),
        ],
        'ref': 'Analytical',
        'assertion': 'Accuracy, Valuation',
    },
    {
        'number': '3',
        'text': 'Verify completeness and accuracy of the population from which items were selected (ISA 500.9)',
        'sub_items': [],
        'ref': 'Analytical',
        'assertion': 'Completeness',
    },
    {
        'number': '4',
        'text': 'Reconcile total revenue for the year with amounts declared in VAT returns (ISA 250.14)',
        'sub_items': [],
        'ref': '',
        'assertion': 'Accuracy, Valuation',
    },
    {
        'number': '5',
        'text': 'Select revenue transactions for all revenue categories, from quotations and follow through to:',
        'sub_items': [
            ('(a)', 'The accounting records and ensure that all sales are accounted for.'),
            ('(b)', "The debtors' account in the debtors ledger and ensure that it was allocated to the correct debtor."),
        ],
        'ref': 'Occurance,AAC',
        'assertion': 'Existence, Accuracy, Classification',
    },
    {
        'number': '6',
        'text': 'Select returns and adjustments from originating documentation and follow through to the accounting records',
        'sub_items': [
            ('', 'Ensure that returns and adjustments are accounted for.'),
        ],
        'ref': 'Occurance,AAC',
        'assertion': 'Completeness, Existence',
    },
    {
        'number': '7',
        'text': 'Select a sequence of delivery notes and ensure that all delivery notes were accounted for',
        'sub_items': [],
        'ref': 'Completeness',
        'assertion': 'Completeness, Existence',
    },
    {
        'number': '8',
        'text': 'Select invoices from the sales listing and account for missing invoices',
        'sub_items': [],
        'ref': 'Completeness',
        'assertion': 'Completeness, Valuation',
    },
    {
        'number': '9',
        'text': 'Review journal entries for revenue accounts',
        'sub_items': [],
        'ref': 'Journals',
        'assertion': 'Occurrence, Accuracy',
    },
    {
        'number': '10',
        'text': 'Presentation and disclosure review',
        'sub_items': [
            ('(a)', 'Review draft AFS for compliance with IFRS for SMEs'),
            ('(b)', 'Verify revenue classification and aggregation'),
            ('(c)', 'Check related party disclosures'),
        ],
        'ref': 'Presentation',
        'assertion': 'Presentation, Classification',
    },
    {
        'number': '11',
        'text': 'Extended tests of detail (if required)',
        'sub_items': [
            ('', 'Perform additional testing based on risk assessment results'),
        ],
        'ref': '',
        'assertion': 'As required',
    },
    {
        'number': '12',
        'text': 'Scrutinise the general ledger',
        'sub_items': [
            ('(a)', 'Review the GL for unusual entries, large balances, or abnormal patterns'),
            ('(b)', 'Investigate any unusual or unexpected items identified'),
        ],
        'ref': '',
        'assertion': 'All assertions',
    },
    {
        'number': '13',
        'text': 'Cut-off testing — select transactions before and after year-end',
        'sub_items': [
            ('(a)', 'Select sales invoices before and after year-end'),
            ('(b)', 'Select credit notes before and after year-end'),
            ('(c)', 'Agree to supporting documentation to ensure correct period'),
        ],
        'ref': 'Cut Off',
        'assertion': 'Cut-off',
    },
    {
        'number': '14',
        'text': 'Scrutinise source documents',
        'sub_items': [
            ('(a)', 'Review supporting documentation for reasonableness'),
            ('(b)', 'Verify authorization and approval'),
        ],
        'ref': '',
        'assertion': 'Occurrence, Accuracy',
    },
]


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def validate_parameters(params):
    errors = []
    if not re.match(r'^\d+\.\d+$', str(params.get('section_number', ''))):
        errors.append("section_number must match Digits.Digits (e.g., '700.40')")
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


def apply_header_fill(cell):
    """Grey D9D9D9 shading + bold, for section headers and table column headers."""
    cell.api.Interior.Color = HEADER_FILL
    cell.api.Font.Bold = True


def apply_subtotal_fill(cell):
    """Grey F2F2F2 shading + bold, for sub-total and total rows."""
    cell.api.Interior.Color = SUBTOTAL_FILL
    cell.api.Font.Bold = True


def set_double_bottom(cell_api):
    cell_api.Borders(XL_EDGE_BOTTOM).LineStyle = XL_DOUBLE


def set_all_borders(sheet, range_str):
    rng = sheet.range(range_str)
    for border_id in [7, 8, 9, 10]:
        rng.api.Borders(border_id).LineStyle = XL_CONTINUOUS
        rng.api.Borders(border_id).Weight = XL_THIN


def set_column_widths(sheet):
    for col, width in COLUMN_WIDTHS.items():
        sheet.range(f'{col}:{col}').column_width = width


def write_header_rows(sheet, params):
    mode = params['mode']
    sn = params['section_number']
    if mode == 'caseware':
        sheet.range('A1').formula = "=[1]!'CWEval|active|CLP2|'"
    else:
        sheet.range('A1').value = params['client_name']
        sheet.range('A1').api.Font.Bold = True
    sheet.range('E1').value = 'Prepared by'
    sheet.range('F1').value = 'First review'
    sheet.range('G1').value = 'Performed by'
    sheet.range('H1').value = 'Final Review'
    sheet.range('I1').value = f'{sn} Testing'
    sheet.range('M1').value = sn
    sheet.range('A2').value = 'Year End:'
    if mode == 'caseware':
        sheet.range('B2').formula = "=[1]!'CWEval|active|SDATE(CLP13)|'"
    else:
        sheet.range('B2').value = params['year_end']
    sheet.range('A3').value = 'Section:'
    sheet.range('B3').value = params['section_name']
    sheet.range('B3').api.Font.Bold = True


def write_title_block(sheet, title):
    sheet.range('A4').value = title
    sheet.range('A4').api.Font.Bold = True
    sheet.range('A4').api.Font.Size = 11


def write_objective_block(sheet, objective_text):
    apply_header_fill(sheet.range('A7'))
    sheet.range('A7').value = 'Objective:'
    sheet.range('A9').value = objective_text


def write_risk_assessment(sheet, params):
    risk = params['risk_level']
    sheet.range('A11').value = 'Audit risk:'
    sheet.range('A11').api.Font.Bold = True
    sheet.range('A13').value = (
        'The risk of material misstatement has been assessed using the Probe approach '
        'as below (refer to 700.10 and 11.60):'
    )
    labels = ['Inherent risk assessment', 'Fraud risk assessment', 'Control risk assessment']
    for row, label in zip([14, 15, 16], labels):
        sheet.range(f'B{row}').value = label
        sheet.range(f'B{row}').api.Font.Bold = True
        sheet.range(f'D{row}').value = risk
        sheet.range(f'E{row}').formula = f'=VLOOKUP(D{row},$F$14:$G$16,2,FALSE)'
    sheet.range('F14').value = 'Low'; sheet.range('G14').value = 1
    sheet.range('F15').value = 'Medium'; sheet.range('G15').value = 2
    sheet.range('F16').value = 'High'; sheet.range('G16').value = 3
    sheet.range('B17').value = 'Risk of material misstatement'
    sheet.range('B17').api.Font.Bold = True
    sheet.range('D17').formula = '=IF(E17<=3,"Low",IF(E17<=6,"Medium","High"))'
    sheet.range('E17').formula = '=SUM(E14:E16)'
    sheet.range('A18').value = (
        'Based on the risk of material misstatement above the required procedures, '
        'significant risk response and extended test of details will be sufficient to reduce '
        'the risk of material misstatement to the desired level of low.'
    )


def write_sample_matrix(sheet, params):
    cat = params['category_type']
    risk = params['risk_level']
    sheet.range('A20').value = 'Sample size and selection:'
    sheet.range('A20').api.Font.Bold = True
    sheet.range('A22').value = 'What type category client is the entity?'
    sheet.range('D22').value = cat
    sheet.range('A23').value = 'Level of risk?'
    sheet.range('D23').value = risk
    sheet.range('A24').value = 'Reason for risk level:'
    sheet.range('D24').value = 'See audit risk above. Should any significant matters be identified the risk will be appropriately reassessed.'
    sheet.range('G20').value = 'Category A'
    sheet.range('I20').value = 'Category C'
    matrix = {21: ('Low', 10, 0.4, 8, 0.4), 22: ('Medium', 20, 0.55, 15, 0.5), 23: ('High', 30, 0.7, 25, 0.6)}
    for row, (label, ca_s, ca_c, cc_s, cc_c) in matrix.items():
        sheet.range(f'F{row}').value = label
        sheet.range(f'G{row}').value = ca_s
        sheet.range(f'H{row}').value = ca_c
        sheet.range(f'H{row}').number_format = '0%'
        sheet.range(f'I{row}').value = cc_s
        sheet.range(f'J{row}').value = cc_c
        sheet.range(f'J{row}').number_format = '0%'
    sheet.range('A25').value = 'Minimum Sample Size:'
    sheet.range('A26').value = '  -  Number'
    sheet.range('A27').value = '  -  Coverage'
    if cat == 'Category A':
        sheet.range('D26').formula = f'=VLOOKUP("{risk}",F21:H23,2,FALSE)'
        sheet.range('D27').formula = f'=VLOOKUP("{risk}",F21:H23,3,FALSE)'
    else:
        sheet.range('D26').formula = f'=VLOOKUP("{risk}",F21:J23,4,FALSE)'
        sheet.range('D27').formula = f'=VLOOKUP("{risk}",F21:J23,5,FALSE)'
    sheet.range('D27').number_format = '0%'


def write_materiality(sheet, params, is_procedures_sheet=False):
    mode = params['mode']
    sn = params['section_number']
    sheet.range('A28').value = 'Performance materiality:'
    sheet.range('A29').value = 'Clearly trivial:'
    if mode == 'caseware' and not is_procedures_sheet:
        sheet.range('D28').formula = f"='{sn} Procedures'!D28"
        sheet.range('D29').formula = f"='{sn} Procedures'!D29"
    else:
        sheet.range('D28').value = params['performance_materiality']
        sheet.range('D29').value = params['clearly_trivial']
    sheet.range('D28').number_format = NUM_FMT_ACCOUNTING
    sheet.range('D29').number_format = NUM_FMT_ACCOUNTING


def write_universal_skeleton(sheet, params, title, objective, is_procedures_sheet=False):
    write_header_rows(sheet, params)
    write_title_block(sheet, title)
    write_objective_block(sheet, objective)
    write_risk_assessment(sheet, params)
    write_sample_matrix(sheet, params)
    write_materiality(sheet, params, is_procedures_sheet)
    set_column_widths(sheet)
    for row in range(1, 31):
        for col_letter in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']:
            cell = sheet.range(f'{col_letter}{row}')
            if cell.value is not None:
                cell.api.Font.Name = FONT_NAME
                cell.api.Font.Size = FONT_SIZE


def write_footer(sheet, start_row, params):
    r = start_row + 2
    sec = params['section_name']
    ye = params['year_end']
    apply_header_fill(sheet.range(f'A{r}'))
    sheet.range(f'A{r}').value = 'Notes:'
    r += 2
    apply_header_fill(sheet.range(f'A{r}'))
    sheet.range(f'A{r}').value = 'Legends:'
    r += 1
    # Tick marks: bold anchor, superscript source part, baseline reference number.
    # All text black — no colour values (repo convention).
    for tick, desc in [('BTB', 'Agreed to trial balance'), ('BAFS', 'Agreed to annual financial statements'),
                       ('BPYTB', 'Agreed to prior year trial balance'), ('BPYAFS', 'Agreed to prior year annual financial statements'),
                       ('\u2211', 'Recalculated'), ('^CC', 'Cross Casts'), ('^', 'Casts')]:
        cell = sheet.range(f'A{r}')
        cell.value = f'{tick} - {desc}'
        cell.api.Font.Bold = True
        r += 1
    r += 1
    apply_header_fill(sheet.range(f'A{r}'))
    sheet.range(f'A{r}').value = 'Conclusion:'
    r += 1
    sheet.range(f'A{r}').value = (
        f'Based on the procedures performed and results obtained, {sec} '
        f'are not materially misstated for the relevant assertions for the year ended {ye}. '
        f'No material misstatements were identified.'
    )
    r += 2
    sheet.range(f'A{r}').value = 'Results:'
    sheet.range(f'A{r}').api.Font.Bold = True
    r += 1
    for line in ['  Auditors journals raised: N/A', '  Management letter points: N/A',
                 '  Overs and unders journals raised: N/A', '  Other considerations: N/A']:
        sheet.range(f'A{r}').value = line
        r += 1
    return r


def calculate_cutoff_dates(year_end_str):
    ye = datetime.strptime(year_end_str, '%Y-%m-%d')
    pre_start = ye - relativedelta(months=1)
    post_end = ye + relativedelta(months=1)
    return {
        'pre_start': pre_start.strftime('%d %B %Y'),
        'pre_end': ye.strftime('%d %B %Y'),
        'post_start': ye.strftime('%d %B %Y'),
        'post_end': post_end.strftime('%d %B %Y'),
    }


# ============================================================
# SHEET BUILDERS
# ============================================================

def build_procedures_sheet(wb, params):
    sn = params['section_number']
    sec = params['section_name']
    sheet = wb.sheets.add(f'{sn} Procedures')
    write_universal_skeleton(sheet, params, f'{sec}: Procedures',
                             f'To ensure that revenue is complete, exists and accurate.', True)
    r = 31
    apply_header_fill(sheet.range(f'A{r}'))
    sheet.range(f'A{r}').value = 'Procedures:'
    sheet.range(f'L{r}').value = 'Reference to work performed'
    r += 2

    sheet.range(f'A{r}').value = 'Required procedures'
    sheet.range(f'A{r}').api.Font.Bold = True
    r += 1

    sheet.range(f'A{r}').value = 'Procedure'
    sheet.range(f'L{r}').value = 'Reference'
    sheet.range(f'M{r}').value = 'Assertion'
    for col in ['A', 'L', 'M']:
        apply_header_fill(sheet.range(f'{col}{r}'))
    r += 1

    for proc in PROCEDURES:
        text = proc['text'].replace('{section_name}', sec)
        sheet.range(f'A{r}').value = f"{proc['number']}. {text}"
        sheet.range(f'A{r}').api.Font.Bold = True
        sheet.range(f'L{r}').value = proc['ref']
        sheet.range(f'M{r}').value = proc['assertion']
        r += 1
        for letter, sub_text in proc['sub_items']:
            sub_text = sub_text.replace('{section_name}', sec)
            if letter:
                sheet.range(f'A{r}').value = f"  {letter} {sub_text}"
            else:
                sheet.range(f'A{r}').value = f"  {sub_text}"
            r += 1
        r += 1

    write_footer(sheet, r, params)
    return sheet


def build_analytical_sheet(wb, params):
    sn = params['section_number']
    sec = params['section_name']
    sheet = wb.sheets.add(f'{sn}-1 Analytical')
    write_universal_skeleton(sheet, params, f'{sec}: Analytical',
                             'To perform an analytical review to identify any unusual items for further investigation.')
    r = 31
    apply_header_fill(sheet.range(f'A{r}'))
    sheet.range(f'A{r}').value = 'Procedures:'
    r += 2
    sheet.range(f'A{r}').value = '2. Agree amounts and disclosures to trial balance and general ledger.'
    r += 1
    sheet.range(f'A{r}').value = '3. Verify completeness and accuracy of the population (ISA 500.9).'
    r += 2
    apply_header_fill(sheet.range(f'A{r}'))
    sheet.range(f'A{r}').value = 'Audit work performed:'
    r += 2
    sheet.range(f'A{r}').value = 'Procedure 2:'
    r += 1
    # CY/PY headers
    ye = datetime.strptime(params['year_end'], '%Y-%m-%d')
    cy = ye.year
    py = cy - 1
    sheet.range(f'D{r}').value = cy
    sheet.range(f'D{r}').api.Font.Bold = True
    sheet.range(f'G{r}').value = py
    sheet.range(f'G{r}').api.Font.Bold = True
    r += 2

    # Balance rows
    bal_row = r
    sheet.range(f'A{r}').value = 'Balance as per trial balance'
    sheet.range(f'F{r}').value = 'BPYTB'
    sheet.range(f'I{r}').formula = f'=IFERROR((D{r}-G{r})/ABS(G{r}),"")'
    sheet.range(f'I{r}').number_format = NUM_FMT_PERCENT
    r += 1
    first_detail = r + 5
    last_detail = first_detail + 19
    sheet.range(f'A{r}').value = 'Balance as per below'
    sheet.range(f'D{r}').formula = f'=SUM(D{first_detail}:D{last_detail})'
    sheet.range(f'G{r}').formula = f'=SUM(G{first_detail}:G{last_detail})'
    r += 1
    sheet.range(f'A{r}').value = 'Difference'
    sheet.range(f'D{r}').formula = f'=D{bal_row}-D{r-1}'
    sheet.range(f'G{r}').formula = f'=G{bal_row}-G{r-1}'
    r += 1
    sheet.range(f'I{r}').value = '^'
    sheet.range(f'I{r}').api.Font.Bold = True
    r += 2

    # Detail breakdown
    sheet.range(f'A{r}').value = 'Detail breakdown:'
    sheet.range(f'A{r}').api.Font.Bold = True
    r += 1
    for col, header in [('A', 'Account'), ('D', f'CY ({cy})'), ('G', f'PY ({py})'), ('I', 'Variance %')]:
        sheet.range(f'{col}{r}').value = header
        apply_header_fill(sheet.range(f'{col}{r}'))
    r += 1

    for i in range(20):
        sheet.range(f'I{r+i}').formula = f'=IFERROR((D{r+i}-G{r+i})/ABS(G{r+i}),"")'
        sheet.range(f'I{r+i}').number_format = NUM_FMT_PERCENT
        sheet.range(f'D{r+i}').number_format = NUM_FMT_ACCOUNTING
        sheet.range(f'G{r+i}').number_format = NUM_FMT_ACCOUNTING
    r += 20

    # Total
    first = r - 20
    last = r - 1
    sheet.range(f'A{r}').value = 'Total'
    sheet.range(f'A{r}').api.Font.Bold = True
    sheet.range(f'D{r}').formula = f'=SUM(D{first}:D{last})'
    sheet.range(f'G{r}').formula = f'=SUM(G{first}:G{last})'
    sheet.range(f'I{r}').formula = f'=IFERROR((D{r}-G{r})/ABS(G{r}),"")'
    for col in ['A', 'D', 'G', 'I']:
        apply_subtotal_fill(sheet.range(f'{col}{r}'))
        sheet.range(f'{col}{r}').number_format = NUM_FMT_ACCOUNTING if col in ['D', 'G'] else NUM_FMT_PERCENT
        set_double_bottom(sheet.range(f'{col}{r}').api)
    r += 1
    write_footer(sheet, r, params)
    return sheet


def _build_testing_section(sheet, r, section_title, item_type, num_rows=20):
    """Build a testing section with sample selection + 3-panel table."""
    apply_header_fill(sheet.range(f'A{r}'))
    sheet.range(f'A{r}').value = section_title
    r += 2

    # Sample selection methodology
    sheet.range(f'A{r}').value = 'Selection:'
    r += 1
    sheet.range(f'A{r}').value = f'Material sample selection:'
    r += 1
    sheet.range(f'C{r}').value = f'{item_type}'
    sheet.range(f'F{r}').value = ''  # total count - user fills
    r += 1
    sheet.range(f'B{r}').value = 'Minus:'
    sheet.range(f'C{r}').value = f'Material {item_type.lower()} selected'
    sheet.range(f'F{r}').value = ''  # user fills
    r += 1
    sheet.range(f'C{r}').value = f'Remaining {item_type.lower()}'
    minus_row = r - 1
    total_row = r - 2
    sheet.range(f'F{r}').formula = f'=F{total_row}-F{minus_row}'
    r += 1
    sheet.range(f'A{r}').value = 'Systematic sample selection'
    r += 1
    sheet.range(f'C{r}').value = f'Remaining {item_type.lower()}'
    remain_row = r - 2
    sheet.range(f'F{r}').value = ''  # same as remaining
    r += 1
    sheet.range(f'B{r}').value = 'Divided by:'
    sheet.range(f'C{r}').value = 'Increment used for testing'
    sheet.range(f'F{r}').value = ''  # sample size - user fills
    inc_row = r
    r += 1
    sheet.range(f'C{r}').value = f'Remaining {item_type.lower()}/Increment'
    remain_ref_row = r - 3
    sheet.range(f'F{r}').formula = f'=IF(F{inc_row}=0,"",F{remain_ref_row}/F{inc_row})'
    r += 1
    sheet.range(f'A{r}').value = f'Therefore every Nth {item_type.lower()} will be selected for verification'
    r += 2

    # Three-panel header
    sheet.range(f'A{r}').value = 'Per the GL'
    sheet.range(f'G{r}').value = 'Supporting Documents'
    sheet.range(f'L{r}').value = 'Testing performed'
    for col in ['A', 'G', 'L']:
        sheet.range(f'{col}{r}').api.Font.Bold = True
    r += 1

    # Column headers
    gl_headers = {'A': 'Reference\nnumber', 'B': 'Invoice number', 'C': 'Date', 'D': 'Description', 'E': 'Amount\nexcl VAT'}
    doc_headers = {'G': 'Invoice/batch\nnumber', 'H': 'Invoice/\nposting date', 'I': 'Description', 'J': 'Debtor\ncode', 'K': 'Amount per\ninvoice (excl VAT)'}
    work_headers = {'L': 'Authorised\nby', 'M': 'Signed\nby', 'N': 'Reason for\njournal', 'O': 'Valid\nreason', 'P': 'Standard price\nlist/Quote',
                    'Q': 'Delivery\nnote', 'R': 'Delivery\nnote date', 'S': 'VAT\nrecalculation', 'T': 'VAT treated\ncorrectly',
                    'U': 'Recorded\ncorrect period', 'V': 'Follow through\ndebtors ledger', 'W': 'Taxes collected\non behalf 3rd party', 'X': 'Recognised only\nwhen criteria met'}
    for headers in [gl_headers, doc_headers, work_headers]:
        for col, header in headers.items():
            sheet.range(f'{col}{r}').value = header
            apply_header_fill(sheet.range(f'{col}{r}'))
            sheet.range(f'{col}{r}').api.WrapText = True
    r += 1

    # Data rows
    data_start = r
    for i in range(num_rows):
        sheet.range(f'E{r+i}').number_format = NUM_FMT_ACCOUNTING
        sheet.range(f'K{r+i}').number_format = NUM_FMT_ACCOUNTING
    data_end = r + num_rows - 1
    set_all_borders(sheet, f'A{data_start}:X{data_end}')
    r = data_end + 1

    # Subtotal
    sheet.range(f'A{r}').value = 'Subtotal'
    sheet.range(f'A{r}').api.Font.Bold = True
    sheet.range(f'E{r}').formula = f'=SUM(E{data_start}:E{data_end})'
    sheet.range(f'K{r}').formula = f'=SUM(K{data_start}:K{data_end})'
    for col in ['A', 'E', 'K']:
        apply_subtotal_fill(sheet.range(f'{col}{r}'))
        sheet.range(f'{col}{r}').number_format = NUM_FMT_ACCOUNTING
        set_double_bottom(sheet.range(f'{col}{r}').api)
    r += 2
    return r


def build_occurrence_sheet(wb, params):
    sn = params['section_number']
    sec = params['section_name']
    sheet = wb.sheets.add(f'{sn}-2 Occurance,AAC')
    write_universal_skeleton(sheet, params, f'{sec}: Occurrence, Accuracy & Classification',
                             'To ensure revenue occurred, is accurate and classified correctly.')
    r = 31
    apply_header_fill(sheet.range(f'A{r}'))
    sheet.range(f'A{r}').value = 'Invoice testing:'
    r += 2
    sheet.range(f'A{r}').value = (
        f'We have obtained the entities invoice listing and will select all material invoices '
        f'and a systematically selection per firm policy.'
    )
    r += 2
    r = _build_testing_section(sheet, r, 'Invoice Testing:', 'Invoices', 20)
    r += 2

    # Credit note section
    apply_header_fill(sheet.range(f'A{r}'))
    sheet.range(f'A{r}').value = 'Credit note testing:'
    r += 2
    sheet.range(f'A{r}').value = (
        f'We have obtained the entities invoice listing and will select all material credit notes '
        f'and a systematically selection per firm policy.'
    )
    r += 2
    r = _build_testing_section(sheet, r, 'Credit Note Testing:', 'Credit notes', 20)

    write_footer(sheet, r, params)
    return sheet


def build_completeness_sheet(wb, params):
    sn = params['section_number']
    sec = params['section_name']
    sheet = wb.sheets.add(f'{sn}-3 Completeness')
    write_universal_skeleton(sheet, params, f'{sec}: Completeness',
                             'To ensure revenue occurred, is accurate and classified correctly.')
    r = 31
    apply_header_fill(sheet.range(f'A{r}'))
    sheet.range(f'A{r}').value = 'Procedures:'
    r += 2

    procs = [
        ('5', 'Select revenue transactions for all revenue categories, from quotations and follow through to:'),
        ('(a)', 'The accounting records and ensure that all sales are accounted for.'),
        ('(b)', "The debtors' account in the debtors ledger and ensure that it was allocated to the correct debtor."),
        ('6', 'Select returns and adjustments from originating documentation and follow through to accounting records.'),
        ('', ''),
        ('', 'Extended test of details'),
        ('7', 'Select a sequence of delivery notes and ensure that all delivery notes were accounted for.'),
        ('8', 'Select invoices from the sales listing and account for missing invoices.'),
    ]
    for num, text in procs:
        if not num and not text:
            r += 1
            continue
        if num and not num.startswith('('):
            sheet.range(f'A{r}').value = num
            sheet.range(f'A{r}').api.Font.Bold = True
            sheet.range(f'B{r}').value = text
            sheet.range(f'L{r}').value = 'Completeness'
        else:
            sheet.range(f'A{r}').value = num
            sheet.range(f'B{r}').value = text
        r += 1

    r += 1
    apply_header_fill(sheet.range(f'A{r}'))
    sheet.range(f'A{r}').value = 'Invoice testing:'
    r += 2
    sheet.range(f'A{r}').value = (
        'We have obtained the entities purchase order listing and have performed a haphazard selection '
        'and traced it back to the accounting records to verify that they have been recognised in the current year.'
    )
    r += 2

    # PO tracing table
    sheet.range(f'A{r}').value = 'As per purchase order listing'
    r += 1
    for col, header in [('A', 'Purchase order no.'), ('B', 'Customer'), ('C', 'Order date'), ('E', 'Amount')]:
        sheet.range(f'{col}{r}').value = header
        apply_header_fill(sheet.range(f'{col}{r}'))
    r += 1

    for i in range(30):
        sheet.range(f'E{r+i}').number_format = NUM_FMT_ACCOUNTING
    set_all_borders(sheet, f'A{r}:E{r+29}')
    r += 31

    sheet.range(f'A{r}').value = 'Result:'
    sheet.range(f'A{r}').api.Font.Bold = True
    r += 1
    sheet.range(f'A{r}').value = 'All purchase orders tested were traced to the accounting records / Exceptions noted above.'
    r += 1

    write_footer(sheet, r, params)
    return sheet


def build_cutoff_sheet(wb, params):
    sn = params['section_number']
    sec = params['section_name']
    sheet = wb.sheets.add(f'{sn}-4 Cut Off')
    write_universal_skeleton(sheet, params, f'{sec}: Cut Off',
                             'To ensure the cut-off of revenue is correct.')
    dates = calculate_cutoff_dates(params['year_end'])

    r = 31
    apply_header_fill(sheet.range(f'A{r}'))
    sheet.range(f'A{r}').value = 'Procedures:'
    r += 2

    # Fraud risk reference
    sheet.range(f'A{r}').value = '1'
    sheet.range(f'A{r}').api.Font.Bold = True
    sheet.range(f'B{r}').value = 'Risk:'
    r += 1
    sheet.range(f'B{r}').value = 'Fraud in revenue recognition: In terms of ISA 240.26, the auditor shall presume that there is a significant risk due to fraud in revenue recognition.'
    r += 1
    sheet.range(f'B{r}').value = 'Response: Credit note cut-off testing, detailed cut-off testing.'
    r += 2
    sheet.range(f'A{r}').value = '13'
    sheet.range(f'A{r}').api.Font.Bold = True
    sheet.range(f'B{r}').value = 'Select transactions before and after year-end and agree to supporting documentation.'
    r += 2

    sheet.range(f'A{r}').value = (
        f'Based on our firm methodology we have elected to make use of number of transactions by selecting '
        f'30 sales invoices before and after year end and 30 credit notes before and after year end.'
    )
    r += 2

    # Cutoff table headers
    cutoff_headers = {'A': 'Sequence\nnumber', 'B': 'Invoice\nnumber', 'C': 'Customer', 'D': 'Invoice\ndate',
                      'E': 'Amount\nexcl VAT', 'F': 'Correct period\n(Y/N)', 'G': 'Delivery note\ndate',
                      'H': 'Goods delivered\nbefore YE (Y/N)', 'I': 'Comments'}

    # Pre YE Sales
    apply_header_fill(sheet.range(f'A{r}'))
    sheet.range(f'A{r}').value = f'Sales before year-end ({dates["pre_start"]} to {dates["pre_end"]}):'
    r += 2
    for col, header in cutoff_headers.items():
        sheet.range(f'{col}{r}').value = header
        apply_header_fill(sheet.range(f'{col}{r}'))
        sheet.range(f'{col}{r}').api.WrapText = True
    r += 1
    for i in range(30):
        sheet.range(f'E{r+i}').number_format = NUM_FMT_ACCOUNTING
    set_all_borders(sheet, f'A{r}:I{r+29}')
    r += 31

    # Post YE Sales
    apply_header_fill(sheet.range(f'A{r}'))
    sheet.range(f'A{r}').value = f'Sales after year-end ({dates["post_start"]} to {dates["post_end"]}):'
    r += 2
    for col, header in cutoff_headers.items():
        sheet.range(f'{col}{r}').value = header
        apply_header_fill(sheet.range(f'{col}{r}'))
        sheet.range(f'{col}{r}').api.WrapText = True
    r += 1
    for i in range(30):
        sheet.range(f'E{r+i}').number_format = NUM_FMT_ACCOUNTING
    set_all_borders(sheet, f'A{r}:I{r+29}')
    r += 31

    # Pre YE Credit Notes
    apply_header_fill(sheet.range(f'A{r}'))
    sheet.range(f'A{r}').value = f'Credit notes before year-end ({dates["pre_start"]} to {dates["pre_end"]}):'
    r += 2
    for col, header in cutoff_headers.items():
        sheet.range(f'{col}{r}').value = header
        apply_header_fill(sheet.range(f'{col}{r}'))
        sheet.range(f'{col}{r}').api.WrapText = True
    r += 1
    for i in range(30):
        sheet.range(f'E{r+i}').number_format = NUM_FMT_ACCOUNTING
    set_all_borders(sheet, f'A{r}:I{r+29}')
    r += 31

    # Post YE Credit Notes
    apply_header_fill(sheet.range(f'A{r}'))
    sheet.range(f'A{r}').value = f'Credit notes after year-end ({dates["post_start"]} to {dates["post_end"]}):'
    r += 2
    for col, header in cutoff_headers.items():
        sheet.range(f'{col}{r}').value = header
        apply_header_fill(sheet.range(f'{col}{r}'))
        sheet.range(f'{col}{r}').api.WrapText = True
    r += 1
    for i in range(30):
        sheet.range(f'E{r+i}').number_format = NUM_FMT_ACCOUNTING
    set_all_borders(sheet, f'A{r}:I{r+29}')
    r += 31

    sheet.range(f'A{r}').value = 'Result:'
    sheet.range(f'A{r}').api.Font.Bold = True
    r += 1
    sheet.range(f'A{r}').value = 'All transactions tested were recorded in the correct financial period / Exceptions noted above.'
    r += 1

    write_footer(sheet, r, params)
    return sheet


def build_journals_sheet(wb, params):
    sn = params['section_number']
    sec = params['section_name']
    sheet = wb.sheets.add(f'{sn}-5 Journals')
    write_universal_skeleton(sheet, params, f'{sec}: Journals',
                             'To ensure that revenue is not materially misstated due to adjusting journals raised.')
    r = 31
    apply_header_fill(sheet.range(f'A{r}'))
    sheet.range(f'A{r}').value = 'Procedures:'
    r += 2
    sheet.range(f'A{r}').value = 'Journal entries and year-end adjustments'
    r += 1
    sheet.range(f'A{r}').value = '15'
    sheet.range(f'A{r}').api.Font.Bold = True
    sheet.range(f'B{r}').value = 'Identify material, significant and unusual year-end adjustments and other non-standard journal entries relating to revenue and:'
    r += 1
    for letter, text in [('(a)', 'Confirm the rationale for the journal entries.'),
                         ('(b)', 'Examine supporting evidence.'),
                         ('(c)', 'Review accounting entries to confirm recognition per IFRS for SMEs.')]:
        sheet.range(f'A{r}').value = letter
        sheet.range(f'B{r}').value = text
        r += 1
    r += 1

    apply_header_fill(sheet.range(f'A{r}'))
    sheet.range(f'A{r}').value = 'Audit work performed:'
    r += 2
    sheet.range(f'A{r}').value = 'Procedure 15:'
    r += 2
    sheet.range(f'A{r}').value = 'We have the general ledger and have identified material, significant or unusual journal entries processed.'
    r += 1
    sheet.range(f'A{r}').value = 'Selection 1: Material Journal sample selection'
    r += 2

    # 3-panel headers
    sheet.range(f'A{r}').value = 'Per General Ledger'
    sheet.range(f'G{r}').value = 'Supporting Documents'
    sheet.range(f'L{r}').value = 'Testing performed'
    for col in ['A', 'G', 'L']:
        sheet.range(f'{col}{r}').api.Font.Bold = True
    r += 1

    # Column headers
    gl_h = {'A': 'Reference\nnumber', 'B': 'Invoice\nnumber', 'C': 'Date', 'D': 'Description', 'E': 'Amount\nexcl VAT'}
    doc_h = {'G': 'Invoice/batch\nnumber', 'H': 'Invoice/\nposting date', 'I': 'Description', 'J': 'Debtor\ncode', 'K': 'Amount per\ninvoice (excl VAT)'}
    work_h = {'L': 'Authorised\nby', 'M': 'Signed\nby', 'N': 'Reason for\njournal', 'O': 'Valid\nreason',
              'P': 'Standard price\nlist/Quote', 'Q': 'Delivery\nnote', 'R': 'Delivery\nnote date',
              'S': 'VAT\nrecalculation', 'T': 'VAT treated\ncorrectly', 'U': 'Recorded\ncorrect period',
              'V': 'Follow through\ndebtors ledger', 'W': 'Taxes collected\non behalf 3rd party', 'X': 'Recognised only\nwhen criteria met'}
    for headers in [gl_h, doc_h, work_h]:
        for col, header in headers.items():
            sheet.range(f'{col}{r}').value = header
            apply_header_fill(sheet.range(f'{col}{r}'))
            sheet.range(f'{col}{r}').api.WrapText = True
    r += 1

    data_start = r
    for i in range(20):
        sheet.range(f'E{r+i}').number_format = NUM_FMT_ACCOUNTING
        sheet.range(f'K{r+i}').number_format = NUM_FMT_ACCOUNTING
    data_end = r + 19
    set_all_borders(sheet, f'A{data_start}:X{data_end}')
    r = data_end + 2

    sheet.range(f'A{r}').value = 'Result:'
    sheet.range(f'A{r}').api.Font.Bold = True
    r += 1
    sheet.range(f'A{r}').value = 'All journals tested were properly authorized and supported / Exceptions noted above.'
    r += 1

    write_footer(sheet, r, params)
    return sheet


def build_presentation_sheet(wb, params):
    sn = params['section_number']
    sec = params['section_name']
    sheet = wb.sheets.add(f'{sn}-6 Presentation')
    write_universal_skeleton(sheet, params, f'{sec}: Presentation and Disclosure',
                             'To ensure that revenue is presented and disclosed appropriately in the annual financial statements.')
    r = 31
    apply_header_fill(sheet.range(f'A{r}'))
    sheet.range(f'A{r}').value = 'Audit work:'
    r += 2

    sheet.range(f'A{r}').value = 'Procedure 10:'
    sheet.range(f'A{r}').api.Font.Bold = True
    r += 1
    sheet.range(f'A{r}').value = f'Review the draft annual financial statements for appropriate presentation and disclosure of {sec}.'
    r += 2

    apply_header_fill(sheet.range(f'A{r}'))
    sheet.range(f'A{r}').value = 'Work performed:'
    r += 1
    items = [
        f'10a. Verified that revenue is recognised when criteria per IFRS for SMEs Section 13 are met.',
        f'10b. Verified that sale of goods — risks and rewards transferred (Section 13.4).',
        f'10c. Verified that rendering of services — stage of completion measured reliably (Section 13.8).',
        f'10d. Verified that interest revenue recognised on effective interest basis (Section 13.14).',
        f'10e. Verified that dividend revenue recognised when right to receive established (Section 13.15).',
        f'10f. Verified that related party revenue is disclosed (Section 33).',
        f'10g. Verified that accounting policy for revenue is disclosed (Section 3).',
        f'10h. Verified that revenue is properly classified (operating vs non-operating) (Section 5).',
        f'10i. Verified that VAT and other taxes are properly excluded from revenue (Section 13.2).',
    ]
    for item in items:
        sheet.range(f'A{r}').value = item
        r += 1
    r += 2

    apply_header_fill(sheet.range(f'A{r}'))
    sheet.range(f'A{r}').value = 'Presentation and Disclosure Checklist:'
    r += 2

    for col, header in [('A', 'Checklist Item'), ('B', 'IFRS for SMEs Ref'), ('C', 'Compliant (Y/N)'), ('D', 'Comments')]:
        sheet.range(f'{col}{r}').value = header
        apply_header_fill(sheet.range(f'{col}{r}'))
    r += 1

    checklist = [
        ('Revenue recognised when criteria met', 'Section 13'),
        ('Sale of goods — risks and rewards transferred', 'Section 13.4'),
        ('Rendering of services — stage of completion', 'Section 13.8'),
        ('Interest revenue — effective interest basis', 'Section 13.14'),
        ('Dividend revenue — right to receive established', 'Section 13.15'),
        ('Related party revenue disclosed', 'Section 33'),
        ('Accounting policy for revenue disclosed', 'Section 3'),
        ('Revenue properly classified', 'Section 5'),
        ('VAT and taxes excluded from revenue', 'Section 13.2'),
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
    expected = [
        f'{section_number} Procedures',
        f'{section_number}-1 Analytical',
        f'{section_number}-2 Occurance,AAC',
        f'{section_number}-3 Completeness',
        f'{section_number}-4 Cut Off',
        f'{section_number}-5 Journals',
        f'{section_number}-6 Presentation',
    ]
    actual = [s.name for s in wb.sheets]
    errors = [name for name in expected if name not in actual]
    if errors:
        print('FAIL: Missing sheets:')
        for e in errors:
            print(f'  - {e}')
        return False
    print('PASS: All 7 sheets present')
    return True


def verify_skeleton(wb, section_number, section_name):
    errors = []
    for s in wb.sheets:
        if s.range('A2').value != 'Year End:':
            errors.append(f'{s.name}: A2 wrong')
        if s.range('A3').value != 'Section:':
            errors.append(f'{s.name}: A3 wrong')
        if str(s.range('B3').value or '') != section_name:
            errors.append(f'{s.name}: B3 wrong')
    if errors:
        print('FAIL: Skeleton errors')
        for e in errors:
            print(f'  - {e}')
        return False
    print('PASS: Skeleton consistent')
    return True


def verify_footers(wb):
    errors = []
    for s in wb.sheets:
        found = {'notes': False, 'legends': False, 'conclusion': False}
        for row in range(50, 500):
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
        print('FAIL: Footer errors')
        for e in errors:
            print(f'  - {e}')
        return False
    print('PASS: All footers present')
    return True


def run_all_verifications(wb, params):
    sn = params['section_number']
    sec = params['section_name']
    print('=' * 60)
    print('REVENUE TEMPLATE VERIFICATION')
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
    errors = validate_parameters(PARAMS)
    if errors:
        print('PARAMETER ERRORS:')
        for e in errors:
            print(f'  - {e}')
        sys.exit(1)
    print('Parameters validated OK')

    wb = xw.Book()
    default = wb.sheets[0]
    default.name = '__delete__'

    print('Building Procedures...')
    build_procedures_sheet(wb, PARAMS)
    print('Building Analytical...')
    build_analytical_sheet(wb, PARAMS)
    print('Building Occurrence, AAC...')
    build_occurrence_sheet(wb, PARAMS)
    print('Building Completeness...')
    build_completeness_sheet(wb, PARAMS)
    print('Building Cut Off...')
    build_cutoff_sheet(wb, PARAMS)
    print('Building Journals...')
    build_journals_sheet(wb, PARAMS)
    print('Building Presentation...')
    build_presentation_sheet(wb, PARAMS)

    wb.sheets['__delete__'].delete()

    run_all_verifications(wb, PARAMS)

    sn = PARAMS['section_number']
    sec = PARAMS['section_name']
    client = PARAMS['client_name']
    filename = f'{sn} {sec} - {client} Revenue Template.xlsx'
    wb.save(filename)
    print(f'\nSaved: {filename}')


if __name__ == '__main__':
    main()
