---
name: wp-procedures-standard
description: House standard for the Procedures sheet of a testing working paper - use when building or rewriting it. Covers the header block, ROMM ratings, assertion codes, procedure numbering, ISA references, scope trimming and live-edit mechanics.
---

# Working-paper Procedures standard

Read `audit-conventions` first.

How the `Procedures` sheet of every testing working paper must be structured.
Bracketed values like `<PM>`, `<Section>` are per-engagement inputs.

## 0. Preconditions

- Follow `audit-conventions` §8 Excel mode: work live in the open workbook via xlwings. Live mode needs the user's `audit-skills approve` first - show what will be written, wait for approval, verify after, keep a backup.

## 1. Sheet skeleton (top to bottom)

| Block | Content |
|---|---|
| Headers (rows 1-4) | Client name, year-end, section name, sheet title `Procedures`, WP ref (e.g. `750-1`), preparer initials, reviewer blank. No CaseWare links (`=_xll...`): strip, hardcode. |
| Objective | One sentence: `To formulate substantive procedures to gain sufficient and appropriate audit evidence that <section> are not materially misstated`. |
| Risk and materiality | ROMM-at-assertion-level table: Completeness / Occurrence / Accuracy valuation and allocation / Cut-off / Presentation and disclosure, each `Medium` (or per §2), presentation `Low` with preparer rationale. Then `Performance materiality` and `Trivial threshold` from the engagement config. |
| Procedures table | The numbered list (§3). |
| (No conclusion block) | Procedures sheets state what *will be done*; conclusions live on the testing sheets. Lines like `We reviewed the general ledger and identified no unusual items` stay as fieldwork placeholders. |

## 2. ROMM and scope trimming

- Default rating is `Medium` unless evidence supports otherwise.
- **Occurrence-only sections:** set Completeness and Cut-off to `Low` with rationale in the next column: `No direct procedures in this section; addressed via trade payables subsequent-payments and accrual testing`. Never leave a `Medium` rating with zero matching procedures - reviewers flag it.
- Delete every procedure outside the agreed scope, not just its wording:
  - Completeness direction (document origin -> records, credit-note completeness) - delete.
  - Cut-off (± year-end selections, cut-off credit notes) - delete.
  - Purchases-specific machinery with no equivalent (returns/GRN flow, trade/settlement/volume rebates) - delete or condense to one line; never leave `purchases journal`, `GRN`, `delivery note`, `SME13` or `gross profit` references in a non-purchases paper.
- Merge duplicated vouching blocks: if invoice-agreement, castings, creditor-recon and EFT-proof steps repeat across two procedures, fold them into one procedure with lettered sub-steps `(a)-(l)` and delete the duplicates.
- Fold VAT checks into the main vouching procedure as final sub-steps (`ISA 250.14` calculation + accounting), not a standalone procedure.
- Keep the Journals procedure with its `(a)/(b)/(c)` spine: confirm rationale -> examine evidence -> IFRS for SMEs recognition/measurement. Retarget it to the section (e.g. `relating to operating expenses (incl. <known reversals/accruals>)`).

## 3. Procedures table mechanics

Four columns, every row:

- **A - assertion codes** (`EO`, `AVA`, `C`, `CO`, combos). Only codes in scope may appear: after trimming, an occurrence-only sheet carries `EO`/`AVA` only. Blank on reference/letter rows, matching the template pattern.
- **B - Reference**: the sheet where the procedure is performed (`Analytical`, `Accuracy and occurrence`, `Completeness and cut-off`, `Journals`). If a scope is dropped, its reference label must not appear anywhere in the table.
- **C - numbering**: integers `1..N` for main procedures, `(a)/(b)/...` for sub-steps, plus section labels (`Journal entries and year-end adjustments`). Numbering must be contiguous after any deletion.
- **D - procedure text** with ISA anchors: TB/GL agreement (`ISA 330.20/.30`), IPE and population completeness/accuracy (`ISA 500.9`), VAT (`ISA 250.14`).

Standard re-targeting mappings (adapt nouns per section):

| Template (cost-of-sales flavoured) | Becomes (OPEX flavoured) |
|---|---|
| `gross profit % per revenue category` | period/period movement per category + monthly trend |
| `conversion of inventory -> COS (SME..)` | correct classification (OPEX vs COS vs payroll vs assets) |
| `match invoice with order / price per order` | match to approved order, contract or SLA; rates to contract/tariff |
| `follow purchases through to creditors recon` | follow *expenses* through to creditors recon / payment advice |
| `cost of inventory (SME13.5/13.6)` | invoiced amount net of discounts; correct category/period |

## 4. Live-edit mechanics (xlwings)

- Back up first (timestamped `SaveCopyAs`, book stays unsaved).
- Wording fixes first (cell writes), **row deletions last, bottom block first** so row numbers stay valid.
- Renumber by scanning column C for integer values and reassigning `1..N` in row order (letters and labels untouched).
- Verify: numbering contiguous `1..N`; banned-string sweep for the old section's vocabulary (e.g. `cost of sales`, `_xll`, preparer names, stale section refs, stale materiality, `purchases journal`, `GRN`, `SME13`, `gross profit`, `rebate`); no out-of-scope assertion codes left over (`C`/`CO` on an occurrence-only sheet); `B` reference labels match surviving scopes; no `#` errors; other sheets untouched.

## 5. Done-check

- [ ] Headers/objective/ROMM/materiality converted, CaseWare links gone
- [ ] Scope-excluded procedures deleted (not reworded), duplicates merged
- [ ] Codes, references, numbering consistent and contiguous
- [ ] ISA anchors present; placeholders intact for fieldwork
- [ ] Sweep clean; backup exists; user visually confirmed before save
