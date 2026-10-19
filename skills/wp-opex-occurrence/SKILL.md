---
name: wp-opex-occurrence
description: Standard for the Accuracy and occurrence sheet of an operating-expenses testing workbook - use when building or rebuilding it. Covers category-block layout, live selection tables, the sampling chain, group-level materiality, prior-year sample-table grammar and workbook hygiene. Scoped to OPEX occurrence (completeness and cut-off out of scope).
---

# OPEX occurrence testing standard

Read `audit-conventions` first.

How the `Accuracy and occurrence` sheet of an operating-expenses testing paper must be built.
Bracketed values like `<PM>`, `<Category>`, `<GL file>` are per-engagement inputs.

Scope notes (load-bearing - do not drift):

- **Occurrence/accuracy/classification only.** Completeness and cut-off are `Low` with rationale (`No direct procedures in this section; addressed via trade payables subsequent-payments and accrual testing`) and have NO procedures, NO tables, NO legends referencing them.
- **Materiality at category (group) level.** Sub-PM accounts inside a material group are still tested - they ride with the group. Picks already requested from the client are never dropped to save work.
- Follow `audit-conventions` §8 Excel mode: work live in the open workbook via xlwings. Live mode needs the user's `audit-skills approve` first - show what will be written, wait for approval, verify after, keep a backup.

## 1. Sheet map (top to bottom)

1. Headers (client, year-end as text, `Operating expenses`, WP ref, preparer; strip all `=_xll` links).
2. Objective (OPEX occurrence/accuracy/classification, one line).
3. Procedures (a)-(i): castings, support docs, supplier/date/amount, maths accuracy, no capital items, OPEX classification (not COS/payroll/assets), VAT, EFT proof-of-payment, Journals-sheet cross-ref. No section-foreign machinery (delivery notes, GRN, rebates, leases).
4. Audit Risk (`Fraud, material misstatement`), Assertions (`Accuracy, occurrence, classification`), both plain.
5. Sheet-level selection box: population GL rows -> material-items count -> coverage sufficient -> methodology (material items + systematic, stratified) -> total picked -> test population -> selected value -> coverage formula -> sufficiency opinion.
6. One block per material category (the material categories per the engagement lead schedule). Each block, in order:
   a. `Item Tested: <Category>` - full-row grey title (A:U, D9D9D9).
   b. Objective one-liner (capitalized).
   c. Breathing space (one blank row).
   d. Selection table (§2).
   e. Breathing space.
   f. Sample table (§3).
   g. `Notes:` + one fieldwork placeholder row.
7. Keys block (6 ticks + plain descriptions) and `Conclusion:` label + OPEX conclusion sentence.

## 2. Selection table (per block, 11 columns A-K)

| Account | GL txns | Pool (N) | Test pop (R) | Material items (n) | Material value (R) | Remaining | Still material? | Method | Picked (n) | Coverage |

- One row per sampled account; unsampled block accounts get a single plain (ungridded, unmerged) note line: `<codes>: analytical only (below PM - no picks)`.
- `Remaining` is a live formula (`=Testpop-Keyvalue`); `Still material?` is a formula (`No (fully covered)` when zero, else Yes/No vs PM).
- Header D9D9D9 + bold + centered, full thin grid on header + data only.
- Plain words: `Material items`, never `Key Items`.
- Selection chain it must tell: material items (count + value, tested 100%) -> remaining -> systematic (`Every Nth`), `100% of pool`, or the engagement's judgmental rule (e.g. all debits above `<threshold>`). Tiny pools go 100% (N <= 15).

## 3. Sample table (prior-year grammar, exact)

- Group row: `Per supporting documents` merged H:N + `Work done` merged P:U, grey (D9D9D9) + bold + centered.
- Titles row: A-F GL-side (`Account`, `Date`, `Counterparty`, `Reference`, `Type`, `Net`), H-N supporting docs (`Date`, `Invoice number`, `Supplier`, `Description`, `Amount excl VAT`, `VAT`, `Amount incl VAT`), P-U work-done (`VAT treated correctly`, `Recalculate VAT`, `Invoice casts`, `Capital in nature`, `In name of company`, `Classification correct`) - grey + bold + centered.
- Spacer columns G and O stay unshaded - they are the visual dividers; shading them fuses the three tables into one.
- Data: GL values only (Account, date, counterparty, ref, type, net); H-U blank for fieldwork (`a`/`r`/`N1` codes). Dates as TEXT `DD/MM/YYYY` (pre-format `@` before writing - Excel flips to US dates otherwise). Amounts `#,##0.00`. Wrap + uniform 15pt rows.
- Material-item picks sort to the TOP of each block's sample table.
- No sample TOTAL row (coverage lives in the selection table).

## 4. Formatting and ticks

- Arial 10, black text; section labels grey (D9D9D9) + bold; detail rows plain; amounts right-aligned numbers.
- Tick standard (see `wp-analytical-standard` §4 - do not duplicate): bold anchor letter, superscript source part, reference number on the baseline, all text black. Applies to matrix-adjacent ticks (if any), keys and legends.
- Column widths follow the prior-year spec (A 11.66, B 13.78, C 27.33, D 16.89, E 16.44, F 16.89, G 11.55, H-N 17.11 except J 19.89 / K 28.44, O 11.55, P-U 17.11). Do not widen columns to fit text - shorten labels (codes) and wrap instead.

## 5. Workbook hygiene (mandatory)

- **No GL sheet inside testing workbooks.** The population lives in the external GL file, referenced by filename in the selection box.
- **No hidden sheets - delete them**, never hide. Verify nothing links to a sheet before deleting it.
- **No amount duplicated across sheets.** Category totals live on the Analytical sheet; occurrence sheets link or reference, never re-type.
- One blank row between every structural element (titles, tables, notes, keys, conclusion). Cramped stacking is a defect.

## 6. Live-edit pitfalls

- Map the existing structure row-by-row BEFORE writing; never assume row numbers from another sheet.
- Row inserts push old content down: insert MORE rows than calculated, write every pushed cell (values AND formats), delete leftovers, then verify nothing old survived (sweep values, fonts, fills, dates).
- Wording fixes first, deletions bottom-up last; renumber after.
- Bulk value-writes preserve existing formats (good) but also preserve stale ones (bad) - normalize formats explicitly on every touched range.
- Verify per-character for ticks (superscript + size), per-cell for fills, pattern-check every date. Then screenshot the sheet and look at it before reporting.

## 7. Done-check

- [ ] Every material category has a block, each complete per §1(6)
- [ ] Selection tables live (formulas calculate; counts tie the engagement GL and sampling file)
- [ ] Sample lines tie the sampling file (count and total); material picks lead
- [ ] No completeness/cut-off content anywhere; plain `material items` language
- [ ] Hygiene §5 holds (no hidden sheets, no GL sheet, no duplicated amounts)
- [ ] Format/date sweeps clean; screenshot self-reviewed; backup exists; user visually confirmed before save
