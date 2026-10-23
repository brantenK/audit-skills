---
name: audit-sampling
description: Simple count-based audit sampling with approved sample size, lead-sheet scope checks, traceable selections and safe working-paper updates. Use when selecting a specified number of transactions or correcting an existing sample.
---

# Audit sampling

Read `audit-conventions` first.

## Scope and method before selection

1. Confirm the source entity, period, sheet, exact lead-sheet accounts and relevant posting side against the TB/GL. References alone do not establish scope.
2. Ask which method is needed: simple count-based systematic selection, or key items plus a remainder sample. For simple selection, ask only how many transactions; do not introduce PM, risk or coverage questions unless relevant to the request.
3. Preserve an existing approved method, order and start. If the firm has a methodology document, use it; do not invent or change methodology while updating a request.
4. Define whether the unit is a GL line or a whole invoice. Retain source-row/account/reference identity and avoid combining unrelated accounts or periods that reuse a reference.

## Simple count-based systematic selection

- Let N be the filtered population count and n the approved number to select. The interval is count-based, not a monetary cumulative interval.
- For the simple amount-ordered approach, sort descending by the relevant amount with source row as the tie-break, unless another order is already agreed.
- Use the agreed interval rounding and starting position. Verify that exactly n distinct positions exist within N. If the agreed rule would produce too many, too few, or out-of-range picks, resolve that before writing; do not silently change n or cycle through the population.
- For a documented equal-step implementation, k = floor(N/n), with a recorded start r and positions r + i*k for i = 0 through n-1. Check k >= 1 and the last position <= N. Do not describe a non-random start as random.
- Preview the full selected references, dates, accounts, amounts, source rows, count and total; obtain approval before changing the working paper.

## Key items and reversals

- Use engagement thresholds and the approved approach only when key-item testing is requested. Identify all qualifying items on the correct posting side, then define the remainder pool separately.
- Keep journal key items separate from an invoice-only systematic pool. A journal releasing deferred income can legitimately credit recognised revenue; an invoice posted only to income in advance is not a revenue occurrence item.
- Equal/opposite amounts identify reversal candidates, not confirmed pairs. Check references, customer, dates, account and allocation/support before exclusion. A cancellation may itself be relevant to cut-off.
- A nil closing balance is not an automatic reason to remove an account's movements from testing.

## Correcting an approved sample

- Show the keep/remove list and remaining count before editing. If exclusions leave an agreed ten-item table short, it is incomplete, not a finished sample.
- Obtain approval for replacements or a changed count. For first/last-ten selections, use the correct population, agreed date ordering and explicit same-day tie-break; verify exactly ten eligible documents.
- Preserve original selection history. A filtered subset is not a newly validated systematic draw; reassess sufficiency if the population changes.
- Update the working paper and client request consistently, including totals and narrative counts. Do not redraw unaffected selections or expand testing automatically.

## Write and verify

- Live Excel writes require workbook approval and a backup; preview first, read back afterwards, check references/counts/formulas and ask for visual confirmation.
- Leave live workbooks unsaved unless the user asks to save. Do not apply Freeze Panes unless requested. Follow the shared formatting conventions instead of embedding a colour scheme in selection code.
- Selected is not vouched: leave test results pending until supporting evidence is inspected.
- Client output follows `client-request-workbook`: approved transactions only, no sampling mathematics or methodology. The client supplies records; the auditor performs tracing.
