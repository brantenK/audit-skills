---
name: tie-to-tb
description: Agree a section's balances to the trial balance and lead sheet, and roll each account forward from opening balance through the year's ledger movements to closing - use whenever a working paper or extract must reconcile to the TB or lead sheet.
---

# Agree to the TB and lead sheet

Read `audit-conventions` first.

## Steps

1. **Scope from the lead sheet.** List the accounts on the lead sheet for the section. Only those are in
   scope.
2. **Closing balances** per the current-year TB for each account.
3. **Opening balances** per the prior-year audited TB (comparative). Also derive the opening per the
   current-year ledger: closing less the year's net movement.
4. **Roll forward** each account:
   `audit-skills tie rollforward --gl <gl.xlsx> --tb <tb.xlsx> --accounts <list>`
   gives opening + credits - debits = closing per GL, compared with closing per TB.
5. **Compare** the ledger opening with the prior-year audited closing. A difference usually means a
   prior-year auditor adjustment that is in the audit file but not in the client's ledger.
   - Reclassifications (RCL) are usually presentation-only. The auditor raises them for the financial
     statements; the client does not post them, and they do not change the total. Explain the difference
     in a note in the working paper. Do not ask the client to post them and do not call it a finding.
   - Adjusting entries (AJE) that change amounts are different: ask the user whether the client was
     expected to post them.
   - Never assume the client reversed an adjustment.
6. **Explain the bridge** when asked whether an extract agrees: a list of the year's transactions
   agrees to the movement, not the closing balance. Opening + movement = closing.

## Reconciliation discipline

- **Simulate before you write.** Run the lookup on the data first (a scratch script or the tool's
  compare commands) and read the results before any formula goes into a working paper. A lookup
  that mostly misses means the keys do not match - fix the keys first, do not pepper the paper with
  `IFERROR(...,0)`.
- **Gap analysis before linking.** Compare the keys on both sides (for example account codes in the
  schedule against the TB) and list what is missing on each side. Resolve or explain every gap
  before you link.
- **Smart linking.** If a lookup against the client's list fails, try the auditor's own list or the
  lead sheet before concluding an item is missing.
- **Variance schedule.** When reconciling two sets of figures, produce a summary table whose
  variances sum to zero. If they do not, something is unexplained - find it before signing off.
- **Golden thread.** Every figure in a working paper links to a source. No hardcoded numbers.

## Output

A roll-forward table in the working paper with a difference column (formula) that must be nil, and a
note of any opening-balance differences.
