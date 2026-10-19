---
name: lease-liabilities-working-paper
description: Build and review instalment agreement / lease liability working papers - classify short term vs long term capital per IFRS for SMEs, extract movements from amortization schedules and reconcile to the trial balance. Use for any lease or instalment sale liability section.
---

# Lease liabilities working paper

Read `audit-conventions` first.

Excel edits follow `audit-conventions` §8: live mode edits an open workbook and needs the user's `audit-skills approve` first; show the user what will be written and wait for approval; verify after.

## When to use

- Creating new instalment agreement working papers
- Reviewing client-prepared lease liability schedules
- Reconciling amortization schedules to the Trial Balance
- Classifying short term vs long term portions

## IFRS for SMEs classification rules

| Classification | Definition | Source |
|----------------|------------|--------|
| Current liability (`<short-term account>`) | Capital payments due within 12 months from the reporting date | Sum of amortization capital column for Jan-Dec of the following year |
| Non-current liability (`<long-term account>`) | Capital payments due after 12 months | Sum of amortization capital column for months 13+ |
| Accrued interest | Disclosed separately (not part of the ST/LT split) | Total outstanding - capital balance |

**Key principle: Short Term + Long Term = Capital Balance, NOT Total Outstanding.** Accrued interest is disclosed separately in trade/other payables.

## Amortization schedule columns

| Col | Header | Contains |
|-----|--------|----------|
| A | Period | Payment period number |
| B | Date | Payment date |
| C | O/B | Opening balance (total outstanding = capital + interest) |
| D | Capital | Capital balance at that date |
| E | Interest | Interest accrual |
| F | Instalment | Instalment amount |
| G | Charges | Additional charges |
| H | Paid | Total paid (instalment + charges) |
| I | Rate | Interest rate |
| J | Interest | Interest portion of the payment |
| K | Capital | Capital portion of the payment |
| L | C/B | Closing balance |

## Working paper columns

| Col | Header | Source | Formula / value |
|-----|--------|--------|-----------------|
| A | Details | - | Asset name |
| B | Agreement number | - | Lender agreement number |
| C | Opening capital | Prior year TB | ST + LT from the audited TB |
| D | New agreements | Amortization | Capital at first payment date |
| E | Total capital outstanding | Calculated | `=C+D` |
| G | Capital paid | Amortization | Sum of monthly capital payments |
| I | Interest paid | Amortization | Sum of monthly interest payments |
| K | Instalment paid | Calculated | `=G+I` |
| M | Capital outstanding EOY | Amortization | Capital column at Jan of next year |
| O | Short term portion | Amortization | Sum of capital payments for the next 12 months |
| Q | Long term portion | Amortization | Sum of capital payments for months 13+ |

## Steps

### 1. Gather source documents

Prior-year audited TB, current-year TB, client amortization schedules for all agreements, the list of new agreements in the year, and the list of sold/paid-off agreements.

### 2. Extract opening capital from the prior TB

For each asset: Opening Capital = Short Term + Long Term from the prior audited TB. This must equal the capital balance (amortization column D) at January of the current year. **Do not use total outstanding (column C) - it includes interest.**

### 3. Process new agreements

For assets not in the prior TB: find the first payment date in the amortization schedule, take the capital balance at that date, and enter it in the "New agreements" column.

### 4. Calculate capital paid

Sum the monthly capital payments (amortization column K) for the current year. Show the working as an explicit addition of the twelve monthly amounts so the breakdown is visible in the cell:

```
=1200.00+1210.00+1220.50+1231.00+1242.25+...   (synthetic illustration)
```

### 5. Calculate interest paid

Same approach on the interest column (J): an explicit addition of the twelve monthly amounts.

### 6. Calculate instalment paid

Formula: `=Capital paid + Interest paid`.

### 7. Capital outstanding EOY

Take the capital balance (column D) at January of next year. This must reconcile to the TB total (ST + LT).

### 8. Short term portion

Sum capital payments (column K) for Jan-Dec of the next year - the 12 months from year end.

### 9. Long term portion

Sum capital payments (column K) for months 13+ (the year after next onwards).

### 10. Reconcile to the TB

| Account | Trial balance | Working paper |
|---------|---------------|---------------|
| Short term (`<short-term account>`) | `<amount>` | `<amount>` |
| Long term (`<long-term account>`) | `<amount>` | `<amount>` |
| **Total capital** | `<amount>` | `<amount>` |

## Common issues and solutions

- **ST + LT does not equal capital EOY.** Caused by amortization rounding (daily interest). Use the capital balance as the authoritative figure and document the difference in the notes.
- **Prior TB differs from the amortization opening.** Amortization column C includes accrued interest. Use the prior audited TB for opening capital; column D should match it; the C vs D difference is accrued interest.
- **Asset in the amortization but opening = 0.** Agreement started during the year: set opening capital 0, new agreements = capital at first payment date, document as "NEW".
- **Capital EOY = 0 but opening had value.** Sold or paid off during the year: capital paid should equal opening capital, capital EOY = 0, document as "SOLD" or "PAID OFF".

## Python reference

```python
import xlwings as xw

CURRENT_YEAR = <yyyy>     # year under audit
NEXT_YEAR = CURRENT_YEAR + 1

wb = xw.Book('<Client> instalment agreements.xlsx')
ws = wb.sheets['<asset name>']

# Capital balance (column D) at January of next year
data = ws.range('B1:D100').value
for row in data:
    date, capital = row[0], row[2]
    if date and hasattr(date, 'year') and date.year == NEXT_YEAR and date.month == 1:
        jan_capital = capital
        break

# Read the schedule once for the payment sums
data = ws.range('B1:K100').value
capital_paid = sum(r[9] for r in data
                   if r[0] and hasattr(r[0], 'year') and r[0].year == CURRENT_YEAR and r[9])
interest_paid = sum(r[8] for r in data
                    if r[0] and hasattr(r[0], 'year') and r[0].year == CURRENT_YEAR and r[8])
st_capital = sum(r[9] for r in data
                 if r[0] and hasattr(r[0], 'year') and r[0].year == NEXT_YEAR and r[9])
lt_capital = sum(r[9] for r in data
                 if r[0] and hasattr(r[0], 'year') and r[0].year > NEXT_YEAR and r[9])

# Build the explicit monthly addition formula (audit trail)
monthly = [r[8] for r in data
           if r[0] and hasattr(r[0], 'year') and r[0].year == CURRENT_YEAR and r[8]]
formula = '=' + '+'.join(f'{v:.2f}' for v in monthly)
ws.range('<target cell>').formula = formula
```

## Tick marks

| Tick mark | Meaning |
|-----------|---------|
| VAMORT | Vouched to amortization schedule |
| BTB | Agreed to Trial Balance |
| BPYTB | Agreed to Prior Year Trial Balance |
| VGL | Verified to General Ledger |
| CC | Cross-cast (agreed to another working paper) |

Apply the standard tick-mark structure: bold anchor, superscript source part, reference number on the baseline - all black (see `audit-working-paper`).

## Verification checklist

- [ ] Opening capital agrees to the prior-year TB (ST + LT)
- [ ] New agreements column populated for assets not in the prior TB
- [ ] Capital paid formula shows the monthly breakdown
- [ ] Interest paid formula shows the monthly breakdown
- [ ] Instalment paid = capital paid + interest paid
- [ ] Capital EOY matches the TB total (within rounding)
- [ ] ST + LT approximately equals capital EOY
- [ ] All tick marks in place
- [ ] Totals row uses SUM formulas
- [ ] Reconciliation section shows the TB comparison

## Notes

1. Always classify on the **capital balance** (column D), never total outstanding (column C).
2. The prior-year audited TB is authoritative for opening balances.
3. Small rounding differences are acceptable - amortization schedules use daily interest. Document them.
4. New agreements show capital at inception, not total outstanding.
5. Interest and capital formulas display the monthly breakdown for the audit trail.

Files (per engagement, confirm with the user): working paper `<Client> lease liabilities.xlsx`; amortization schedules `<Client> instalment agreements <year>.xlsx`; current-year TB per the engagement file; prior-year TB from the audited financial statements.
