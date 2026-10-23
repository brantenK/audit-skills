---
name: completeness-combined
description: Single-section revenue completeness testing - sequence-gap analysis (shared vs split numbering), master-to-billing, cut-off and reversal screen, and earned-vs-billed matching, each procedure with its reason - use when testing completeness of revenue for any client.
---

# Revenue completeness (combined)

Read `audit-conventions` first.

One section for total revenue. Completeness direction is **OUTSIDE -> INSIDE**: start from an independent source and trace the transactions that should have been recognised into the accounting records. An unmatched source item is an exception to investigate, not automatically an understatement: exemption, timing, cancellation or duplicate records may explain it.

## The four procedures (each ships with its reason)

| # | Procedure (what) | Reason (why it proves completeness) | Failure looks like |
|---|---|---|---|
| P1 | Master -> billing: eligible fee-paying members/customers during the agreed period traced to billings; investigate omissions and valid exemptions | The master exists independently of invoices and can reveal omitted billings | Eligible but unbilled members/customers |
| P2 | Sequence continuity: every gap in the invoice run evidenced (void log, other-module invoice, next FY) | Numbers cannot be skipped silently; an unexplained gap may be an unrecorded sale | Unexplained gap |
| P3 | Cut-off + reversals: year-end invoices belong to the right period; every large credit matched to original + reason | Genuine sales pushed across year-end go missing from the year; unjustified reversals shrink revenue | Late sales; wipeouts |
| P4 | Earned-vs-billed + journals: events/deliveries matched to billings (deferral); each journal/intruder agreed to source | An event or delivery that happened must have matching revenue; sourceless journals hide missing or double-counted billings | Thin revenue vs activity |

Conclude only on procedures actually performed and exceptions resolved. A sequence check alone does not establish that every eligible member or delegate was billed. Do not claim completeness before the independent-source work needed for the agreed approach is complete.

## Membership: keep the procedure and request proportionate

- Invoice -> member database checks the validity of recorded charges. Member database -> billing checks completeness; paid members must not be omitted from the source population.
- Identify fee-paying eligibility from the approved fee/category/status rules, including exemptions or company-paid arrangements. Add join/exit history only where needed for the agreed period; avoid requesting all database fields by default.
- Invoice delivery failures are not necessarily missing accounting entries. Unallocated receipts are not proof that a member has not paid.
- Payment supports occurrence/collection but does not establish the membership or service period for recognition.
- The client supplies the existing register and transaction report; the auditor does the tracing and reconciliation.
- For conferences, reuse event dates already evidenced. Request registration/attendance populations only when a delegate-to-billing procedure is agreed; website event dates alone do not prove all delegates were billed.

## Sequence analysis protocol

1. Extract all invoice refs (all streams combined); parse numerics; report total lines, distinct count, span, % present.
2. Determine **shared vs split numbering**: sample consecutive numbers - if they mix accounts/streams, it is one shared run -> combined test is correct; if each stream has its own series -> stratify.
3. Bucket gaps: **HEAD** (below continuous run - prior FY/other ledgers), **TAIL** (above run - post-cutoff/other modules/manual numbers), **INTERNAL** (within run - must clear to register/void log).
4. Duplicates: same-ref multi-line splits (same counterparty+date) are normal - count documents on a distinct-number basis.
5. Non-standard refs (journals, SIV, payments) listed separately - never part of the sales sequence.
6. Honest caveat: a gap unresolved after checking the available ledgers requires evidence of its disposition. First use records already held; ask for the specific invoice or confirmation it was unused, and request a wider register/void log only if needed. Do not label unresolved gaps "skipped" or "never issued" without evidence.

## Workbook layout: agreed scope first

Use the existing prior-year/approved paper. Do not automatically create six sheets or implement every procedure above. Add Master-Billing, Cutoff-Reversals or Deferred-Journals schedules only when the corresponding work is agreed. A client request is a separate client-facing workbook using `client-request-workbook`, not an internal testing tab sent to the client.

Mark tested and gap rows with grey shading only (D9D9D9 headers, F2F2F2 highlight) - no other colours (`audit-conventions` section 3).

## Rules

- One assertion per conversation when presenting to the auditor; reasons in plain language before jargon.
- Credit-note runs get their own continuity test (usually tight - few gaps).
- Prior-period catch-ups flag possible late billing or recognition issues. Establish the service period and discuss any needed expansion; do not expand master work automatically.
