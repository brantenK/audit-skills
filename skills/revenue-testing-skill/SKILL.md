---
name: revenue-testing-skill
description: Builds a complete 7-sheet revenue testing working paper template (Procedures, Analytical, Occurrence-AAC, Completeness, Cut-off, Journals, Presentation) in placeholder or CaseWare mode via the bundled scripts/build_template.py - use when the user asks for a new revenue section working paper from scratch.
---

# Revenue testing working paper template

Read `audit-conventions` first.

Builds a complete 7-sheet revenue testing working paper from scratch. The heavy lifting is done by the bundled script `scripts/build_template.py`. Prefer the prior-year template when one exists (`audit-conventions` section 2); build new only when the user asks for it.

## Sheets created

| # | Sheet name | Purpose |
|---|---|---|
| 1 | `{section_number} Procedures` | Revenue-specific audit procedures (ISA 240.26 fraud risk) |
| 2 | `{section_number}-1 Analytical` | CY vs PY analytical review |
| 3 | `{section_number}-2 Occurance,AAC` | Invoice testing + credit note testing (3-panel each) |
| 4 | `{section_number}-3 Completeness` | GL vs TB + sequence testing + PO tracing |
| 5 | `{section_number}-4 Cut Off` | Sales AND credit notes pre/post year-end |
| 6 | `{section_number}-5 Journals` | 3-panel journal testing (GL / Documents / Work done) |
| 7 | `{section_number}-6 Presentation` | IFRS for SMEs revenue disclosure checklist |

## Build steps

1. Collect the parameters below from the user. Take performance materiality and clearly trivial from the engagement config - never hard-code them (`audit-conventions` section 1).
2. Edit the `PARAMS` dict at the top of `scripts/build_template.py` with the collected values.
3. Run the script:

```bash
python scripts/build_template.py
```

The script validates the parameters, builds all 7 sheets with formatting, runs verification checks (sheet names, skeleton, footers) and saves the workbook.

Parameters to collect:

1. Section number (e.g. `700.40`)
2. Section name (e.g. `Revenue - Trading`)
3. Client name
4. Year end (`YYYY-MM-DD`)
5. Performance materiality (from engagement config)
6. Clearly trivial (from engagement config)
7. Mode: `caseware` or `placeholder`
8. Category type: `Category A` or `Category C`
9. Risk level: `Low`, `Medium` or `High`

## Revenue-specific features

- **ISA 240.26 fraud risk**: revenue has a presumed significant fraud risk. The Procedures sheet carries a dedicated fraud risk response section covering credit note cut-off testing, detailed cut-off testing, and testing of journals in revenue accounts.
- **Dual testing**: the Occurrence sheet has two separate sections - invoice testing (material + systematic selection) and credit note testing with its own sample selection block.
- **Sequence testing**: the Completeness sheet includes delivery note sequence testing, missing invoice testing, and purchase order to GL tracing.
- **4-part cut-off**: the Cut-off sheet has four sections - pre year-end sales, post year-end sales, pre year-end credit notes, post year-end credit notes (30 rows each).
- **3-panel journals**: the Journals sheet has three panels - per General Ledger, Supporting Documents, and Testing Performed (authorisation, VAT, period, criteria met).

## Dual mode

| Feature | `caseware` mode | `placeholder` mode |
|---|---|---|
| Client name (A1) | `=[1]!'CWEval\|active\|CLP2\|'` | Plain text (bold) |
| Year end (B2) | `=[1]!'CWEval\|active\|SDATE(CLP13)\|'` | Plain text |
| Sign-off fields | CaseWare user/date formulas | Empty (manual entry) |
| Materiality cells | Cross-sheet links to Procedures sheet | Direct values |
| All other content | Identical | Identical |

## Formatting

Per `audit-conventions` section 3: Arial 10pt, black text, grey shading only.

- D9D9D9 shading: section headers (Objective, Notes, Legends, Conclusion) and table column headers.
- F2F2F2 shading: sub-total and total rows.
- Tick marks: bold anchor letter, superscript source part (TB, PYTB, AFS), CaseWare reference number on the baseline (never superscripted) - all black text.
- Double bottom borders on subtotals; do NOT set `Weight` on a double border (COM crash prevention).
- Accounting number format on all amount cells.

## Excel mode

The script creates a new workbook. For any further live edits to a workbook open in Excel, follow `audit-conventions` section 8: the user must run `audit-skills approve <workbook>` first; show the user what will be written, wait for approval, then verify after writing.

## Guardrails

MUST NOT:

- Auto-populate test data
- Implement sample selection (use the `sample-and-coverage` skill)
- Create GL/data import sheets
- Hard-code account codes or client data
- Assume a December year-end
- Skip any of the 7 sheets

Scope: empty template structure only. GL data import, sample selection and actual testing are OUT OF SCOPE.
