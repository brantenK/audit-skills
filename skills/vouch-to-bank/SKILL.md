---
name: vouch-to-bank
description: Trace ledger payments or receipts to bank statements by amount, date and payee - use when the user asks to verify transactions against bank statements or check year-end bank balances against the TB.
---

# Vouch to bank statements

Read `audit-conventions` first.

## Steps

1. **Get the statements into a table.** Text PDFs: extract the lines. Scanned PDFs: render the pages and
   read them. Columns needed: date, description (with payee reference line), debit, credit, balance,
   source file and page.
   - Payee or reference often sits on the line below the amount line. Attach it to the right amount.
2. **Check continuity**: each statement's closing balance equals the next statement's opening balance.
3. **Year-end balance**: closing balance per statement equals the TB account.
4. **Match ledger items**:
   `audit-skills vouch bank --gl <gl-lines.xlsx> --bank <bank-lines.csv> --days 3`
   matches on amount and date within the window, then reports the payee for review.
5. **Classify each ledger item**:
   - Agreed to bank statement (amount, date and payee agree).
   - Not found on statements (searched the full period: say which statements were searched).
   - Not a bank item: supplier invoices and journals cannot be vouched to bank. Say so plainly; they
     need invoice or journal support instead.
6. **Report bank payments with no ledger match** that look related (same payee or venue). Record them as
   questions, not conclusions.

## Do not

- Do not count an invoice as "not found" without saying it is an invoice.
- Do not claim a statement was read if it was scanned and skipped.
