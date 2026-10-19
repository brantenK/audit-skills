---
name: sample-and-coverage
description: Split a balance into material accounts tested 100% and a remainder that is sampled, select the sample, compute coverage against the TB and write the sufficiency conclusion - use when planning, selecting or documenting a sample for an audit section.
---

# Sampling and coverage

Read `audit-conventions` first.

## Plan the split

1. Get PM, individually significant (default 75% of PM), client category and level of risk from the
   engagement config. If the level of risk is not set, ask the user: it is their judgement.
2. Run `audit-skills sample plan --balances <file> ` (or the `sample_plan` MCP tool). It returns:
   - **A. Material accounts**: at or above individually significant. Tested 100%.
   - **B. Remainder**: below individually significant. Whether the remainder in total is material
     (compared with PM).
   - Minimum number and coverage from the sample table for the category and risk.
3. Opening balances carried in a paper are not transactions. Test them by agreeing to the prior-year
   audited TB.

## Select the sample

**Simple systematic (the usual request).** When the user asks for a number of transactions without
mentioning materiality:

- Interval = population count ÷ sample size. 107 items ÷ 15 = every 7th; 200 ÷ 20 = every 10th.
- Sort by amount descending and select every Nth item.
- Do not ask for PM, risk levels or coverage percentages. The user's number governs.
- Tiny pools (N ≤ 15 items) are tested in full rather than sampled.

**Key Items plus systematic (only when the user mentions materiality or PM).**

- Key Items are single ledger lines above PM. Test them 100%. Zero Key Items is itself a finding:
  record the largest line and its multiple below PM.
- Cancelling pairs (an item and its exact reversal, net nil) are excluded from the pool and the
  pair is documented - never silently dropped.
- Select from the remainder until the minimum coverage is met. Prefer larger items and items near
  the year end.

**Defensible systematic (ISA 530, when the sample must survive review).**

- Keep the ledger's own posting order. Never re-sort by amount or date.
- k = FLOOR(N / n). Random start r via `secrets.randbelow(k) + 1`: one draw, no seed.
- Positions r, r+k, r+2k, ... (1-indexed in the ordered list). Require r + (n-1)k ≤ N.
- Record N, n, k, r, the generation method and the timestamp in the working paper, and show how
  each position maps back to a ledger row. Write the selection paragraph so a reviewer can replicate
  it: filter, order, number 1-N, apply the positions.

**Occurrence pools are invoices only.** Journals are Key Items if above PM, otherwise documented
separately - never inside an interval. Credit notes are excluded from occurrence picks. Other
transaction types are excluded and flagged for classification follow-up.

**Sub-selection.** To shrink an approved sample of n1 picks to n2, take the top n2 by value within
the parent picks only (earliest row breaks ties) and say so in the paper. Never re-select from the
full population once a parent sample exists.

## Coverage and conclusion

In the working paper show: sub-total A, sub-total B, items selected from B, total tested,
TB balance, overall coverage (formula), minimum coverage, and the sufficiency sentence:
"We tested X% of the balance (material accounts 100% and Y% of the remainder), which exceeds the
minimum coverage of Z%. We are therefore satisfied that the sample is sufficient."

Low coverage on bulk populations (1-4%) is expected. Assurance comes from spread plus analytical
proof-in-total, not from the percentage. Never present a judgmental pick as statistical sampling.

Mark selected rows with grey shading (D9D9D9); excluded cancelling pairs with F2F2F2 and a note.
No other colours (see `audit-conventions`).

## Notes

- The sample table lives in `methodology/conventions.yaml`. Values marked null are not set; ask the user.
- The sample list sent to the client is a plain ledger extract (skill `client-gl-extract`).
