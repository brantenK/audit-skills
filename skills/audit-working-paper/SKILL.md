---
name: audit-working-paper
description: Review, enhance or build an audit working paper in Excel to review standard - documentation rules (ISA 230), sheet structure and borders, tick marks, coverage boxes, client requests and troubleshooting. Use whenever a working paper must be created, reviewed or brought up to standard.
---

# Audit working paper

Read `audit-conventions` first.

> **If a prior-year paper exists for this section, stop and use `update-from-prior-year` instead of
> building a new layout.** Copy the prior-year workbook, keep its structure and update it. Only build
> from scratch when the user asks for it.
>
> **If there is no prior-year paper, use `new-section-paper`** - and ask which sheet(s) the user wants
> before creating anything. Never build the full six-sheet set unasked.

Excel edits follow `audit-conventions` §8: live mode edits an open workbook and needs the user's `audit-skills approve` first; show the user what will be written and wait for approval; verify after.

## 1. Documentation standards

ISA 230 (as adopted in South Africa / IRBA):

- **The experienced auditor test.** Documentation must let an experienced auditor with no previous connection to the audit understand the nature, timing and extent of the procedures, the results, and the significant matters and conclusions reached.
- **Identification.** Selected items must be specifically identified - "Invoice #1234 dated 12/03/2025", not "selected invoice".
- **Sign-offs.** Mandatory "Prepared by" (with date) and "Reviewed by" (with date) fields on every paper.

Companies Act 71 of 2008:

- **Section 24:** financial records and supporting documentation retained for 7 years.
- **Section 29:** working papers must support compliance with the reported framework (IFRS / IFRS for SMEs).

**Golden thread:** every number traceable - source (TB/GL) -> work performed -> evidence -> conclusion. No hardcoded numbers without a visible source.

**Evidence status:** selected, requested, received and vouched are different stages. A GL extraction or VAT calculation does not prove that the client invoice was inspected. Keep documentary results and pass/fail fields blank until supported; distinguish selected totals from verified totals. Never carry forward a clean conclusion while testing is outstanding.

**Minutes insights:** follow `audit-conventions` §6. Use minutes to inform existing sections, not automatically create a separate minutes paper or more testing. Quote the meeting/date, keep reported statements separate from verified findings, and do not infer a cancellation effective date, missing invoice or confirmed overstatement from discussion alone.

## 2. Formatting standards

Arial, black text, grey shading only: D9D9D9 headers, F2F2F2 sub-totals. No other colours.

| Element | Style |
|---------|-------|
| Section headers | Bold, 11pt+ |
| Account headers | Bold, grey shading D9D9D9 |
| Nature notes | Grey shading F2F2F2, italic |
| Table headers | Bold, grey shading D9D9D9, bottom border |
| Sub-totals | Bold, grey shading F2F2F2, top border |
| Totals | Bold, top border; double bottom border on grand totals |
| Key items | Bold with grey shading D9D9D9 |

Numbers `#,##0.00;(#,##0.00);"-"`. Dates `dd mmm yyyy` (per `audit-conventions` §3).

## 3. Sheet structure

Standard row map - adapt to the prior-year paper where one exists (`update-from-prior-year`):

| Rows | Content |
|------|---------|
| 1 | Title: client name, section, year (bold, merged across the sheet width) |
| 2 | Separator (height 6pt) |
| 3-7 | Sign-off grid: Prepared by / Reviewed by, name and date, bordered |
| 8 | Separator (6pt) |
| 9-14 | Assertion and risk table (relevant? risk Low / Medium / High as text) |
| 15 | Separator (6pt) |
| 16-31 | Objective and scope block |
| 32 | Separator (6pt) |
| 33-43 | Procedures performed |
| 44 | Separator (6pt) |
| 45 | Section header (e.g. "RECONCILIATION") |
| 47 | Column headers (grey D9D9D9) |
| 48-90 | Reconciliation / testing data with formulas |
| 91 | Separator (6pt) |
| 92 | Conclusion |
| 93-95 | Notes |
| 97-102 | Legend: tick mark definitions |

Standard columns: A descriptions/labels (width 45), B amounts (width 18, accounting format), C tick marks (width 12), D source references (width 25).

- Blank rows between sections: set height 6pt for consistent visual spacing.
- Narrative paragraphs: no merged cells or automatic wrapping. Write through column H, then continue on the next row from A. Keep one blank row before and after headings and between a note block and its table; retain approved template widths.
- Border every table and merged panel on all four edges, plus inside gridlines.
- Hide gridlines; landscape print layout, fit to one page wide, repeat row 1 as the print title.

## 4. Tick marks

Structure: `[Anchor][Superscript source][Reference number]`. Example `BTB 750` = bold anchor **B**, superscript `TB`, reference number `750` on the baseline. All text black, Arial.

| Part | Format |
|------|--------|
| Anchor (B, V) | Bold, 11pt, normal |
| Superscript part (TB, PYTB, GL, AFS, AMORT) | 10pt, superscript |
| Reference number (750, 550.70.1) | 10pt, normal - on the baseline, never superscript |

Vertical-align tick-mark cells to the bottom so superscripts are not clipped. Every tick mark used must appear in the legend.

```python
def apply_tick_mark_formatting(sheet, cell_range):
    """Format tick marks: bold anchor, superscript source, baseline reference. All black."""
    for cell in sheet.range(cell_range):
        value = str(cell.value) if cell.value else ''
        if len(value) < 2 or value[0] not in ('B', 'V'):
            continue
        letter_end, number_start = 0, -1
        for i, char in enumerate(value):
            if char.isdigit() or (char == ' ' and value[i + 1:i + 2].isdigit()):
                number_start = i
                break
            letter_end = i + 1
        try:
            c = cell.api
            c.Font.Bold = True
            c.VerticalAlignment = -4107            # xlBottom
            anchor = c.GetCharacters(Start=1, Length=1)
            anchor.Font.Size = 11
            anchor.Font.Superscript = False
            if letter_end > 1:
                sup = c.GetCharacters(Start=2, Length=letter_end - 1)
                sup.Font.Size = 10
                sup.Font.Superscript = True
            if number_start > 0:
                num = c.GetCharacters(Start=number_start + 1, Length=len(value) - number_start)
                num.Font.Size = 10
                num.Font.Superscript = False       # reference never superscripted
        except Exception:
            pass
```

## 5. Coverage box (mandatory)

Insert below every testing table to prove the extent of testing:

| Row | Content | Formula |
|-----|---------|---------|
| 1 | Total of account | `=ABS(closing_balance_cell)` |
| 2 | Amounts verified | `=SUM(items actually vouched)` or linked verified total, not the entire untested selection |
| 3 | Coverage % | `=verified/total`, formatted as % |

## 6. Auditable formulas

- Bad: a typed `15000`. Good: `=SUM(D10:D50)`, `=J12-K12` (movement).
- Rule: if a number changes in the GL, the working paper conclusion must update automatically.

## 7. Testing focus by section

| Section | Focus | Typical procedures |
|---------|-------|--------------------|
| Income 7XX | Occurrence, accuracy | Use the invoice plus the relevant membership/service/agreement records for the agreed procedure. Do not apply a generic delivery-note requirement to membership or conferences. Payment does not by itself prove the correct recognition period. Verify other income against its own section scope. |
| Expenses 6XX | Completeness, classification | Agree to supplier invoice, check the date (cut-off), verify VAT treatment |
| Assets 1XX-2XX | Existence, valuation | Receivables: confirmations, provision for bad debts. Inventory: count, lower of cost/NRV |
| Liabilities 3XX-4XX | Completeness (understatement risk) | Supplier statement reconciliations, search for unrecorded liabilities |

### Cash on hand and foreign currency

- Agree the count to the ledger currency by currency, then convert at the rate the client used. Compare
  that rate with the rate implied by the foreign bank account; a difference is a valuation point even
  when the amount is small.
- Record the date of the count. An undated count sheet is a documentation weakness - state the date on
  the paper or get the client to confirm it.
- Where a ledger balance was negative or unsupported and was written up to the count, treat the write-up
  as a correction. Identify the account it was posted to and whether it belongs in profit or loss.

## 8. Reconcile before you write

1. **Find the source data:** the prior-year recon (structure, tick marks, reconciling items), the analytical sheet, the GL extract, and any independent report the client produces (payroll report, provision schedule).
2. **Aggregate the GL by account**, total it, and compare with the TB.
3. **Present the full reconciliation to the user as a markdown table and get explicit approval of the numbers before writing anything to Excel.**

Reconciliation skeleton:

```
GL total (trial balance)                      <amount>
Less: items per the independent report       (<amount>)
Less: provision / other movements            (<amount>)
Less: GL items not in the independent report (<amount>)
                                              --------
Adjusted GL balance                           <amount>
Per the independent report                    <amount>
                                              --------
Variance                                      <amount>
```

Assess the variance against the engagement config: below clearly trivial - immaterial, no further work; between trivial and PM - investigate the nature; above PM - must be resolved.

## 9. Client requests

Use `client-request-workbook`: approved transaction lists plus a separate simple `Document required | Details to include` section for general records. Ask for records, not client performance of our tracing/allocation procedures. Reuse evidence held and request only what the agreed testing needs; no materiality, coverage, findings, conclusions or response boxes unless asked.

Question templates:

- **Cost recovery / intercompany:** provide the cost allocation schedule or calculation for this amount; what is the basis of allocation (headcount, revenue, time); provide the intercompany agreement covering this period; provide evidence of authorization/approval for this journal entry.
- **General expense:** provide the valid tax invoice; proof of delivery/service rendered; evidence of payment.

## 10. Hygiene and troubleshooting

- Fix `#REF!` / `#VALUE!` errors immediately - trace precedents.
- Unhide hidden rows/columns; if hiding is intentional, label it "Hidden for printing".
- Identify and break circular references.
- Define every tick mark in a legend.

COM pitfalls when driving Excel through xlwings:

| Issue | Cause | Fix |
|-------|-------|-----|
| `0x800ac472` error | Writing to a non-anchor cell of a merged range | Write to the anchor cell; retry with a delay |
| Text becomes a formula | Value starts with `=` | Prefix with a space |
| Borders disappear | COM race condition on large ranges | Brief sleep between border operations |
| Superscript invisible | Font too small (7pt) | 10pt minimum for superscript |
| Character formatting fails | Cell empty or merged | Check `cell.value` before formatting |
| Print setup fails | Sheet not active | Activate the sheet, brief pause, then set PageSetup |

Safe write helpers worth reusing:

```python
def safe_text(text):
    """Stop text that starts with '=' being read as a formula."""
    return ' ' + text if isinstance(text, str) and text.startswith('=') else text

def safe_write_value(sheet, cell_ref, value, retries=3):
    """Retry writes that hit merged-cell COM errors (0x800ac472)."""
    import time
    for attempt in range(retries):
        try:
            sheet.range(cell_ref).value = value
            return True
        except Exception as e:
            if '0x800ac472' not in str(e):
                raise
            if attempt == retries - 1:
                return False
            time.sleep(0.5)
    return False
```

## 11. Verify before hand-over

After writing, read back key cells against expected values (numbers to within 0.01, text exactly), scan the written range for error values, and confirm totals. Report what was checked and what was not, then ask the user for visual confirmation in Excel. On verification failure or user-reported issues, restore from the backup.

## Workflow

1. **Read** the current working paper and identify the section/account.
2. **Analyse** it against the standards above.
3. **Propose** a plan to the user (e.g. "this is section 730 Other Income; I will apply standard formatting, add a coverage box and draft a client request").
4. **Execute** with backup, preview and approval (`audit-conventions` §8).
5. **Verify** and report.
