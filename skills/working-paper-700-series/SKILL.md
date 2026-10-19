---
name: working-paper-700-series
description: Builds CaseWare-style 700-series occurrence working papers (700.55 pattern) with multi-stream selections - header, risk box, A-T vouching tables, VAT formulas, casts, coverage box, notes, legends and conclusion. Use for any client, any year.
---

# Working paper 700-series (occurrence)

Read `audit-conventions` first.

Replicates the prior-year 700.55 skeleton with current-year data, split into stream selections (one block per revenue stream in scope).

Follow `audit-conventions` §8 Excel mode for live edits: the user runs `audit-skills approve` on the workbook first; show what will be written, wait for approval, verify after, keep a backup.

## Skeleton (top to bottom - do not reorder)

1. **Header (rows 1-4):** entity, Year End, Section, Prepared/Reviewed/Performed/Final-review + dates, Item Tested, Doc ID. Plain values for portability; live CaseWare DDE links only on explicit request.
2. **Objective + risk:** objective sentence + Inherent / Fraud / Control + material (Yes/No) + RMM + `=SUM` of scores.
3. **Sample-size box:** Category A/C table (Low/Med/High -> n/coverage), entity category, risk level, reason (state the judgmental basis + no-projection explicitly), Number, Coverage pointer, **PM**, **ISI** (default 75% of PM, per the engagement config), Clearly Trivial - thresholds from the engagement config.
4. **Selection narrative:** one line per stream - population N, Key Items, interval k, random start r, TB tie for the stream.
5. **Procedures:** 9(a)-(h) + 14/17/19/23/24 (adapt N/A items, e.g. delivery notes, with reason).
6. **Work tables** (below) -> **combined coverage box** (verified / TB, `%` format) -> unusual accounts -> procedure notes -> N1-N4 -> legends (`^`, recalc, OCINV, `a`) -> conclusion + sign-off line.

## Work-table standard (columns A-U)

| Block | Cols | Content |
|---|---|---|
| Per GL | A-D | Invoice number, Date (`DD/MM/YYYY`), Debtors details, Amount Excl VAT |
| spacer | E | widened (>=6), no borders |
| Per invoice | F-I | Invoice number, Invoice date, Debtor name and code, Amount per invoice |
| spacer | J | widened (>=6) |
| Testing | K-T | Delivery note no/date (or N2), price list (N1), VAT recalc **`N =I*0.15` live formula**, VAT ok, period, debtors ledger, third-party taxes, recognition criteria |
| spacer | U | widened |

Per table: grey (D9D9D9) bold header row, note row if needed ("No items > PM - 100% systematic"), data rows, `=SUM` totals row (bold), `^` cast row. Each block (A-D, F-I, K-T) gets its **own full grid borders** so blocks read as separate tables. One blank row between sections.

## Styling defaults

- Dates: `DD/MM/YYYY` number format on all date cells (never raw datetimes showing time).
- Invoice-date column wide enough to avoid `####` (>=16).
- Category-table integers: `0` decimals.
- Amounts: `#,##0.00`, right-aligned; totals bold.
- Header fill D9D9D9; no merged cells (CaseWare-hostile); `fitToPage`.

## Rules

- F-I prefilled from GL as the starting point to be ticked; testing cols blank for fieldwork.
- VAT `N3` (foreign/no-VAT) applied during testing, not at build.
- Excluded items (cancelled pairs, journals in systematic) documented in the selection narrative - never silently dropped.
- Preparer/reviewer/dates left blank for the auditor to sign.
- After build: capture a screenshot of the header box and one full table (xlwings `to_png`), read it, fix clipping/dates/borders before reporting.
