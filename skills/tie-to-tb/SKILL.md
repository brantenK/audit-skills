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
   prior-year auditor adjustment (AJE or reclassification) that the client never posted. Record it as a
   finding and ask the client to post it. Do not assume the client reversed it.
6. **Explain the bridge** when asked whether an extract agrees: a list of the year's transactions
   agrees to the movement, not the closing balance. Opening + movement = closing.

## Output

A roll-forward table in the working paper with a difference column (formula) that must be nil, and a
note of any opening-balance differences.
