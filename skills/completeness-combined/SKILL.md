---
name: completeness-combined
description: Single-section revenue completeness testing - sequence-gap analysis (shared vs split numbering), master-to-billing, cut-off and reversal screen, and earned-vs-billed matching, each procedure with its reason - use when testing completeness of revenue for any client.
---

# Revenue completeness (combined)

Read `audit-conventions` first.

One section for total revenue. Direction is always **OUTSIDE -> INSIDE**: start from something real (a customer on the master file, an invoice number, cash, an event or a delivery) and prove it got recorded. Any failure = understated revenue.

## The four procedures (each ships with its reason)

| # | Procedure (what) | Reason (why it proves completeness) | Failure looks like |
|---|---|---|---|
| P1 | Master -> billing: every active customer on the master file at period start traced to an invoice; vouch catch-ups | The master file exists independently of the GL; a real customer with no invoice = missing revenue | Unbilled customers |
| P2 | Sequence continuity: every gap in the invoice run evidenced (void log, other-module invoice, next FY) | Numbers cannot be skipped silently; an unexplained gap may be an unrecorded sale | Unexplained gap |
| P3 | Cut-off + reversals: year-end invoices belong to the right period; every large credit matched to original + reason | Genuine sales pushed across year-end go missing from the year; unjustified reversals shrink revenue | Late sales; wipeouts |
| P4 | Earned-vs-billed + journals: events/deliveries matched to billings (deferral); each journal/intruder agreed to source | An event or delivery that happened must have matching revenue; sourceless journals hide missing or double-counted billings | Thin revenue vs activity |

Close with the chain sentence: *everyone billed + every number explained + right period with no unjustified wipeouts + everything recorded once = nothing real missing.*

## Sequence analysis protocol

1. Extract all invoice refs (all streams combined); parse numerics; report total lines, distinct count, span, % present.
2. Determine **shared vs split numbering**: sample consecutive numbers - if they mix accounts/streams, it is one shared run -> combined test is correct; if each stream has its own series -> stratify.
3. Bucket gaps: **HEAD** (below continuous run - prior FY/other ledgers), **TAIL** (above run - post-cutoff/other modules/manual numbers), **INTERNAL** (within run - must clear to register/void log).
4. Duplicates: same-ref multi-line splits (same counterparty+date) are normal - count documents on a distinct-number basis.
5. Non-standard refs (journals, SIV, payments) listed separately - never part of the sales sequence.
6. Honest caveat: internal gaps **cannot be cleared from the GL alone** - the full system invoice register + void/cancelled log is a mandatory client request. List gaps; do not pretend to clear them.

## Workbook layout (6 sheets)

Method (P1-P4 with reasons) | Sequence (gap table: series, from, to, size, bucket, "cleared to", init) | Master-Billing (GL side prefilled, client columns blank) | Cutoff-Reversals (year-end invoices + reversal pairs + clusters) | Deferred-Journals (event billings vs event dates + journal/intruder integrity) | Client Request (registers, master file, event dates, journal/reversal support).

Mark tested and gap rows with grey shading only (D9D9D9 headers, F2F2F2 highlight) - no other colours (`audit-conventions` section 3).

## Rules

- One assertion per conversation when presenting to the auditor; reasons in plain language before jargon.
- Credit-note runs get their own continuity test (usually tight - few gaps).
- Prior-period catch-ups found in-year (prior periods billed now) are P1 evidence of systematic late billing - expand master work, do not just accept.
