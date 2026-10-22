---
name: new-section-paper
description: Build an audit working paper for a section that has no prior-year paper - six-sheet section structure, the standard header block (rows 1-44), GL sample tables with audit-trail references and mandatory supporting-documentation tables. Always asks which sheet to build before creating anything.
---

# New section paper (no prior-year reference)

Read `audit-conventions` first.

**If a prior-year paper exists for the section, use `update-from-prior-year` instead.** This skill is only
for sections with no reference paper.

## 1. Ask before you build

- **Never build all six sheets unasked.** Ask which sheet(s) the user wants, then build only those:
  `Procedures`, `Analytical`, `Completeness`, `Existence & Valuation`, `Journals`, `Presentation`.
- The rest are added later, on request. Building the full set "just in case" wastes the reviewer's time.

## 2. What each sheet is for

| Sheet | Purpose | Minimum content |
|---|---|---|
| Procedures | What we will do and why | Objective, ROMM, assertion codes, procedures with ISA references |
| Analytical | Movement and ratios | CY vs PY by account, variance %, explanation, days/ratios where relevant |
| Completeness | Understatement risk | Population, selection, coverage, conclusion |
| Existence & Valuation | Overstatement risk | Vouching to documents, confirmations, subsequent receipts, valuation |
| Journals | Large/unusual entries | Journal listing, purpose, support, cut-off |
| Presentation | Classification and disclosure | TB vs lead sheet vs AFS, current/non-current, disclosure checklist |

## 3. Standard header block - rows 1-44

Model: the `430.55` provision paper. Keep this order.

| Rows | Content |
|---|---|
| 1 | Sign-off header: entity · Prepared by · 1st Review · Performed by · Final Review · file name · document ref |
| 2 | Year End: date · preparer/reviewer names |
| 3 | Section: name |
| 4 | Title (full width) |
| 7 / 9 | "Objective:" and the one-sentence objective |
| 11 / 13 | "Audit risk:" and the Probe-approach sentence |
| 14-16 | Risk table: Inherent / Fraud / Control - assessment, score, scale, score |
| 17 | Risk of material misstatement (formula on the score) |
| 19 | "Based on the risk of material misstatement above…" statement |
| 21-25 | Sample size and selection: client category, level of risk, reason |
| 26-28 | Minimum sample size: number and coverage |
| 29-31 | Performance materiality, individually significant, clearly trivial |
| 33-36 | Procedures: heading, numbered procedure, lettered sub-items |
| 38-42 | Verification: CY/PY columns, account lines with BTB/BPYTB, total with BAFS/BPYAFS, `^` ticks |
| 44 | "Audit work performed:" - the testing section starts here |

Rules:
- Take PM, ISI and trivial from the engagement config. **Never hardcode a percentage** - prior papers
  have used 25% and 75% for ISI on different sections.
- Prior-year papers carry CaseWare `[1]!` formulas. Replace them with the cached values in file mode.
- Dates are real Excel dates (`dd/mm/yyyy`); when generating them by formula use `DATE(y,m,d)`.

## 4. GL sample table standard

- **One separate table per GL account. Never combine accounts.**
- Six columns, in this order: **Date · Entry Type · Reference · Description · Debit · Credit**.
- Account title row above each table: full GL code and description, Arial 10 bold, fill `#D9D9D9`,
  solid black perimeter.
- Header row: the six exact headers, Arial 10 bold, fill `#D9D9D9`, black borders.
- Body: Arial 10, source wording preserved, dotted grey internal borders `#A6A6A6`, solid black
  left/right perimeter. Do not populate unused rows; remove stale borders.
- **Audit-trail reference column** immediately right of the table, outside the border: Arial 10 bold,
  green `#008000`, borderless. Match each reference to the right transaction using date, amount, entry
  type and description - never amount alone.
- **Selected total** row: label "Selected total", Arial 10 bold, no fill, single top border and double
  bottom border, amount in the Debit or Credit column per the account's sign convention.
- **Nil accounts** keep their own six-column table, with "General" as the narrative and a zero/dash
  total (Debit column for expense/debit-sign accounts).
- Do not call a population 100% tested unless every transaction was genuinely selected and tested.

## 5. Supporting-documentation table - mandatory with every sample

- Build one **next to every GL sample table**, automatically - do not wait to be asked.
- Five columns: **Date · Reference · Description · Amount · Difference**.
- Heading above the five columns: **As per Supporting documentation**.
- Position it to the right of the audit-trail column, with a clean borderless spacer column.
- Align each row horizontally with its GL transaction row.
- Leave Date, Reference, Description and Amount blank until the evidence is received. Never invent
  supporting-document details.
- Difference formula on every row: `=SupportingAmount-GLDebit` for debit-sign samples,
  `=SupportingAmount-GLCredit` for credit-sign samples. When no amount is entered it shows the unmatched
  GL amount in brackets - never hardcode a zero.
- Number format `#,##0.00;[Red](#,##0.00);-`.
- Same header fills, black outer border, dotted grey internal borders, row heights and column widths as
  the GL table beside it.
- Include the same blank row before/after the body and the same total row (single top, double bottom).
- Nil accounts get a matching five-column supporting-documentation table too.

## 6. House formatting

| Element | Format |
|---|---|
| Table and section headers | Arial 10 bold, fill `#D9D9D9`, black borders |
| Account title rows | Arial 10 bold, fill `#D9D9D9`, black perimeter |
| Totals / subtotals / Selected total | Bold, no fill, single top border + double bottom (grand total) |
| Narrative rows | Merged across the table width, wrap text, no fill |
| Hyperlinks (source links) | Blue `#0000FF`, underlined, short label |
| Tick marks | Anchor & Float: green bold anchor, green superscript source, red non-superscript reference |
| Numbers | `#,##0.00` (financial: `#,##0.00;[Red](#,##0.00);-`) |
| Dates | `dd/mm/yyyy`, real dates |

Highlights - two colours only:

- **Light yellow `#FFFF99`** - exceptions, errors, and anything we are not yet sure of. This is the
  default signal that a line needs the reviewer's attention. Use it without being asked.
- **Light grey `#D9D9D9`** - everything else: table headers, column headers, account title rows,
  section dividers. Grey is the house fill.
- **Green `#00B050`** - only when the user asks for sampled rows to be marked in a GL extract. Not a
  default.
- **Material / key items** - no fill of their own. Highlight them only when the user asks, in the
  colour they name.
- No other fills. No stray colours, old borders, mixed date formats or half-formatted blocks.

## 7. Sampling

- Pull the sample from the GL and reconcile it to the audit trail before writing anything.
- Select using the applicable methodology, materiality, risk, unusual items, cut-off and coverage.
- Do not default to 100% simply because the population is available.
- Confirm sample count and value coverage against the testing objective.
- Recheck each selected item against both the GL and the audit trail before finalising.

## 8. Verify before hand-over

- Recalculate; zero formula errors; totals agree to the TB and lead sheet.
- Every GL account has its own table; totals sit in the right column; references align to the right rows;
  supporting-documentation rows align; Difference formulas point at the right cells.
- Screenshot the edited area and look at it: clipped headers, stray fills, merged cells in the wrong
  place.
- Tell the user what was checked and what was not.

## 9. Definition of done

Every relevant GL line item has its own correctly formatted table, sampled transactions agree to the GL
and audit trail, totals and coverage are correct, nil accounts retain their tables, and every sample
table has a matching five-column supporting-documentation table with aligned Difference formulas - with
no reminder needed.
