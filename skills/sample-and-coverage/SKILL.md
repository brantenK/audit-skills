---
name: sample-and-coverage
description: Split a balance into material accounts tested 100% and a remainder that is sampled, compute coverage against the TB and write the sufficiency conclusion - use when planning or documenting a sample for an audit section.
---

# Sampling and coverage

Read `audit-conventions` first.

## Steps

1. Get PM, individually significant (default 75% of PM), client category and level of risk from the
   engagement config. If the level of risk is not set, ask the user: it is their judgement.
2. Run `audit-skills sample plan --balances <file> ` (or the `sample_plan` MCP tool). It returns:
   - **A. Material accounts**: at or above individually significant. Tested 100%.
   - **B. Remainder**: below individually significant. Whether the remainder in total is material
     (compared with PM).
   - Minimum number and coverage from the sample table for the category and risk.
3. Select remainder items until the minimum coverage is met. Prefer larger items and items near the
   year end.
4. In the working paper show: sub-total A, sub-total B, items selected from B, total tested,
   TB balance, overall coverage (formula), minimum coverage, and the sufficiency sentence:
   "We tested X% of the balance (material accounts 100% and Y% of the remainder), which exceeds the
   minimum coverage of Z%. We are therefore satisfied that the sample is sufficient."
5. Opening balances carried in a paper are not transactions. Test them by agreeing to the prior-year
   audited TB.

## Notes

- The sample table lives in `methodology/conventions.yaml`. Values marked null are not set; ask the user.
- The sample list sent to the client is a plain ledger extract (skill `client-gl-extract`).
