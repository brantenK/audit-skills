---
name: audit-sampling-pack
description: Reviewer-defensible GL sampling packs with lead-sheet scope, key-item and invoice-pool separation, systematic provenance, agreed sample counts and honest coverage. Use when documenting multi-stream samples or reviewing existing selections.
---

# Audit sampling pack

Read `audit-conventions` first.

## 1. Scope gate before selection

- Confirm the entity and period inside the source, not just its filename. Agree exact lead-sheet accounts to the TB/GL and use the relevant debit/credit side.
- Define file, sheet, source-row range, account filter, transaction-type filter, selection unit and ordering. Exclude blank/total rows.
- An invoice prefix or broad income-account prefix is not proof of revenue scope. Income in advance and other income outside the lead are not occurrence picks. Release journals may be in scope on their recognised-revenue credit.
- Keep the approved method and order. For a new posting-order systematic pack, retain source order; do not impose that on an approved amount-ordered method.
- For document-level amounts, aggregate only relevant lines in the correct period; exclude debtor controls, VAT and forex revaluations. Explain differences between selected GL-line values and whole-document values internally.

## 2. Separate pools

- Scan key items against the approved engagement threshold and relevant side. Report source rows, references, accounts, dates, amounts and total. No key items is a population characteristic, not automatically a control finding.
- Revenue systematic occurrence pools contain tax invoices only. Journal key items are separate; do not include journals inside an invoice interval.
- Credit notes are a separate population. Equal/opposite amounts identify candidate reversals only; confirm the relationship and agree exclusions. Do not discard cancellations automatically from cut-off testing.
- Flag supplier invoices, payments and other intruders for classification review rather than treating them as sales.

## 3. Systematic provenance

For an agreed random-start, equal-step count selection:

```text
k = floor(N / n)
r = secrets.randbelow(k) + 1
positions = r + i*k, for i = 0 through n-1
require k >= 1 and r + (n-1)*k <= N
```

- Record N, n, k, r, ordering, generation method, timestamp and the mapping from positions to source rows. Record the actual start; do not claim randomness if none was used.
- If n exceeds N or a position is invalid, stop and agree the treatment; do not silently reduce n or redraw an approved sample.
- Include a concise methodology paragraph and replication steps in the internal paper, not the client schedule.

## 4. Correcting scope or reducing a sample

- First show exclusions and the retained count. Obtain approval before reducing the agreed sample or choosing replacements. Do not leave a last-ten/first-ten table short and describe it as complete.
- Refill first/last selections from the correct population only after approval, using the agreed date ordering and a documented same-day tie-break. Verify the exact count and eligible references.
- If a top-by-value sub-selection within an approved parent draw is agreed, preserve parent provenance and state its judgmental nature. Do not relabel it as statistical or claim unperformed remainder assurance.
- A scope-cleaned subset is not a new systematic draw. Preserve the original selection audit trail and reassess sample sufficiency when the frame changes.
- Do not redraw unaffected samples or automatically expand testing. Update the working paper and client request together.

## 5. Coverage and completion

- Distinguish selected, requested, received and vouched amounts. Use actual verified amounts for verified coverage, with the correct reconciled denominator.
- Low selection coverage does not itself prove insufficiency or justify a larger sample. Assess it against the agreed methodology and procedures actually performed.
- Verify active selections, not excluded-item logs or historical support tabs: exact lead accounts, posting sides, counts, uniqueness, references and totals.
- Before live writes: preview, approval, backup. Afterwards: read-back, error scan, formula/total check and visual confirmation. Leave unsaved unless asked to save; no Freeze Panes unless requested.
- Use `client-request-workbook` for the client list. Preparing that list does not authorise another selection, additional evidence requests or a claim that testing passed.
