---
name: client-request-workbook
description: Build the workbook that goes to the client listing the documents required for testing (invoices, signed journal vouchers) - use when the user says "client request", "send list", "request invoices" or asks what to send the client. Produces one client-facing sheet only.
---

# Client request workbook

Read `audit-conventions` first. A working paper is internal; this workbook is the only thing that
leaves the office.

## What it is

A single-sheet workbook listing the ledger lines for which the client must provide documents. The client
matches each line to their ledger and sends the document. Nothing else belongs in it.

## File

- New workbook, saved in the section folder: `<Section> - Client Request FY2026.xlsx`.
- Never a tab of the working paper and never saved inside it.

## Layout - one sheet only

1. Row 1: entity name (bold).
2. Row 2: `<Section> - client document request | Year end: <date>`.
3. Row 3: one line only - `Please provide invoices for the below transactions.`
4. Numbered, plain section headings: `1. Transactions`, `2. Selected invoices`.
5. Table columns, in the ledger's own order:

   `# | Account_Code | Account_Name | Date | Counterparty | Reference | Txn_Type | Narrative | Amount (R) | Document requested`

6. A bold total row per section.

## Rules

- Amounts and dates exactly as in the ledger (`dd/mm/yyyy`, `#,##0.00`).
- `Document requested` = **Tax invoice** or **Signed journal voucher**, set from `Txn_Type`, so the
  client knows what to send for each line.
- No materiality, no sample size, no interval, no "key item", no coverage, no testing rationale.
- No "Provided (Y/N)" or response column unless the user asks for one.
- No confirmations section - documents only. Confirmations (event dates, explanations) are asked
  separately, not in this workbook.
- Keep selection groups as separate sections; do not merge them into one table.

## Covering email

- Short, no amounts, no "material", no "largest", no methodology.
- "Please provide the invoices for the transactions in the attached list."

## Check before sending

- Every line traces to the ledger extract (account + reference + amount).
- Totals recalculate.
- Screenshot the sheet and fix clipped columns or headers.
- Scan the sheet for the words materiality, sample, interval, testing, coverage, selection - there should
  be none.
