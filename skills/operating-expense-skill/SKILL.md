---
name: operating-expense-skill
description: Builds a complete 8-sheet expense testing working paper template (Procedures, Analytical, Occurrence-Material, Occurrence-Sensitive, Completeness, Cut-off, Journals, Presentation) in placeholder or CaseWare mode via the bundled scripts/build_template.py - use when the user asks for a new operating-expense section working paper from scratch.
---

# Expense testing working paper template

Read `audit-conventions` first.

Builds a complete 8-sheet expense testing working paper from scratch. The heavy lifting is done by the bundled script `scripts/build_template.py`. Prefer the prior-year template when one exists (`audit-conventions` section 2); build new only when the user asks for it.

## Sheets created

| # | Sheet name | Purpose |
|---|---|---|
| 1 | `{section_number} Procedures` | Standard audit procedures checklist |
| 2 | `{section_number}-1 Analytical` | CY vs PY analytical review |
| 3 | `{section_number}-2 Occurence - Material` | Material items testing (3-panel) |
| 4 | `{section_number}-3 Occurence - Sensitive` | Sensitive items testing (3-panel) |
| 5 | `{section_number}-4 Completeness` | GL vs TB completeness check |
| 6 | `{section_number}-5 Cut off` | Pre/post year-end cut-off testing |
| 7 | `{section_number}-6 Journals` | Journal entry testing |
| 8 | `{section_number}-7 Presentation` | IFRS for SMEs disclosure checklist |

## Build steps

1. Collect the parameters below from the user. Take performance materiality and clearly trivial from the engagement config - never hard-code them (`audit-conventions` section 1). The expense categories to test are the material categories per the engagement lead sheet - do not invent a category list.
2. Edit the `PARAMS` dict at the top of `scripts/build_template.py` with the collected values:

```python
PARAMS = {
    'section_number': '750.55',           # <-- change this
    'section_name': 'Other expenses',     # <-- change this
    'client_name': 'Test Client Ltd',     # <-- change this
    'year_end': '2025-12-31',             # <-- change this
    'performance_materiality': 1000000,   # <-- from engagement config
    'clearly_trivial': 50000,             # <-- from engagement config
    'mode': 'placeholder',                # <-- 'caseware' or 'placeholder'
    'category_type': 'Category A',       # <-- 'Category A' or 'Category C'
    'risk_level': 'Low',                 # <-- 'Low', 'Medium' or 'High'
}
```

3. Run the script:

```bash
python scripts/build_template.py
```

The script validates the parameters, creates a new workbook, builds all 8 sheets with formatting, runs verification checks and saves the file.

## Parameter validation rules

Before running, the script checks:

| Parameter | Rule |
|---|---|
| section_number | Must be digits.digits (e.g. `750.55`) |
| section_name | Must not be empty |
| client_name | Must not be empty |
| year_end | Must be valid YYYY-MM-DD date |
| performance_materiality | Must be > 0 |
| clearly_trivial | Must be > 0 and < performance_materiality |
| mode | Must be `caseware` or `placeholder` |
| category_type | Must be `Category A` or `Category C` |
| risk_level | Must be `Low`, `Medium`, or `High` |

If any check fails, the script prints errors and exits. Fix the PARAMS and re-run.

## Dual mode

| Feature | `caseware` mode | `placeholder` mode |
|---|---|---|
| Client name (A1) | `=[1]!'CWEval\|active\|CLP2\|'` | Plain text (bold) |
| Year end (B2) | `=[1]!'CWEval\|active\|SDATE(CLP13)\|'` | Plain text |
| Sign-off fields | CaseWare user/date formulas | Empty (manual entry) |
| Materiality (D29-D30) | Cross-sheet links to Procedures sheet | Direct values |
| All other content | Identical | Identical |

## What each sheet contains

### Sheet 1: Procedures
10 standard audit procedures with lettered sub-items. Columns: Procedure (A), Reference (L), Assertion (M). Covers risk assessment, analytical review, completeness, occurrence, cut-off, journals, presentation, extended testing, GL scrutiny, source document review.

### Sheet 2: Analytical
Work performed text (3 items); analytical review table CY vs PY; balance per trial balance, balance per below, difference; 15 empty detail rows with variance % formulas; subtotal row with SUM formulas.

### Sheet 3: Occurrence - Material
Three-panel testing table: "Per the GL" (A:G) | "Per the Supporting documents" (I:P) | "Work done" (R:X). 20 empty data rows with borders and difference formula (P = G - O). Subtotal row, methodology block (selection method, sample size, interval).

### Sheet 4: Occurrence - Sensitive
Same three-panel structure as Sheet 3, with "Sensitive Items Testing" header text.

### Sheet 5: Completeness
Work performed text (3 items); completeness check table: Balance per GL vs Balance per TB; difference formula.

### Sheet 6: Cut-off
Date windows calculated from the `year_end` parameter (never assumes December). Pre year-end testing section (15 empty rows) and post year-end testing section (15 empty rows). Uses `dateutil.relativedelta` for month calculations.

### Sheet 7: Journals
Work performed text (5 items); journal entry testing table with 20 empty rows. Columns: Journal #, Date, Description, Debit, Credit, Prepared by, Approved by, Supporting docs, Classification, Comments.

### Sheet 8: Presentation
Work performed text (7a-7f); IFRS for SMEs disclosure checklist with 6 items. Columns: Checklist Item, IFRS Ref, Compliant (Y/N), Comments.

## Formatting

Per `audit-conventions` section 3: Arial 10pt, black text, grey shading only.

- D9D9D9 shading: section headers (Objective, Audit work, Work performed, Notes, Legends, Conclusion) and table column headers.
- F2F2F2 shading: sub-total rows.
- Tick marks: bold anchor letter, superscript source part (TB, PYTB, AFS), CaseWare reference number on the baseline (never superscripted) - all black text.
- Thin borders on data rows, double borders on subtotals. Do NOT set `Weight` on a double border (COM crash prevention).
- Accounting number format on all amount cells; standard column widths (A through X).

## Excel mode

The script creates a new workbook. For any further live edits to a workbook open in Excel, follow `audit-conventions` section 8: the user must run `audit-skills approve <workbook>` first; show the user what will be written, wait for approval, then verify after writing.

## After generation

The template is empty - testing tables have structure but no data. The auditor (user) will:

1. Import GL data into the testing tables
2. Populate supporting document details
3. Fill in work done columns (Y/N)
4. Add tick marks
5. Write conclusions

Use the `sample-and-coverage` skill for sample selection.

## Guardrails

MUST NOT:

- Auto-populate test data
- Implement sample selection (use the `sample-and-coverage` skill)
- Create GL data sheets
- Hardcode account codes or client data
- Assume December year-end
- Skip any of the 8 sheets

Scope: this skill creates the empty template structure only. GL data import, sample selection, actual testing and evidence documentation are OUT OF SCOPE.
