---
name: age-analysis-transformation
description: Convert a transaction-heavy creditors or debtors age analysis report into a one-line-per-vendor audit summary sheet that reconciles to the source grand totals - use when a raw client age analysis needs restructuring into a working-paper summary.
---

# Age analysis transformation

Read `audit-conventions` first.

Live mode edits the open workbook and needs the user's `audit-skills approve` first. Show the
user what will be written and wait for approval; verify after writing; save only when the user
asks (`audit-conventions` §8).

## Objective

Convert a client-provided age analysis (many transaction lines per vendor) into a clean
one-line-per-vendor summary sheet that reconciles exactly to the source grand totals.

## Discovery - anchor detection

Never rely on fixed row numbers. Scan for anchor strings to find the data blocks:

| Anchor | Where | Meaning |
|---|---|---|
| `Vendor #:` | column A | start of a vendor block |
| `Total for [Code] :` | column B | vendor block total line |
| `Total For This Report :` | column B | report grand total |

## Column mapping

Scan roughly the first 50 rows to identify:

- **Name/code column** - usually column B.
- **Aging buckets** - Current, 30, 60, 90, 120, 120+ - located from the numeric values on the
  `Total for` lines.
- **Net balance column** - the amount-owing column; detect it per file, never assume a fixed
  column.

## Transformation rules

- Parse vendor labels `CODE (NAME)` into `CODE - NAME`.
- One summary row per vendor: aging bucket values as **static values**, so deleting or
  re-sorting source rows cannot break links.
- Grand total row: **SUM formulas** over the vendor rows, for internal mathematical accuracy.
- Ignore the transaction lines between the anchors.
- Formatting: Arial, black text; headers bold with grey shading D9D9D9; grand total bold with
  top and bottom borders; number format `_(* #,##0.00_);_(* (#,##0.00);_(* "-"??_);_(@_)`.

Parse with a short Python script (openpyxl or xlwings) using the anchors above, and keep the
script in the tool's temp folder, not in the workpaper folders. Back up the workbook before
writing.

## Verification (mandatory after writing)

Run one verification pass and report the results:

1. **Reconciliation:** summary grand total equals the source grand total (tolerance 0.01).
2. **Completeness:** vendor count in the summary equals the count of `Total for` lines in the
   source.
3. **Error scan:** no `#REF!`, `#VALUE!` or `#DIV/0!` in the new sheet.
4. **Formatting check:** number format and bold applied as specified.

Ask the user to confirm the result visually in Excel. Restore the backup if any check fails.

## Usage

"Apply the age analysis transformation to the approved workbook. Name the new sheet
`Age Analysis Summary` and verify the totals."
