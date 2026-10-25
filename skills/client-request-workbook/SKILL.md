---
name: client-request-workbook
description: Build a simple one-sheet client request from approved audit selections, with transaction lists, a separate plain general-document list and a natural covering email. Use for client requests, send lists or requests for invoices and credit notes.
---

# Client request workbook

Read `audit-conventions` first. A working paper is internal; this workbook is the only thing that
leaves the office.

## What it is

A single-sheet workbook listing the approved transactions and essential supporting records the client must provide. The client sends the records; the auditor performs tracing, matching and reconciliation. Do not add new selections or procedures while preparing a request.

## File

- New workbook, saved in the section folder: `<Section> - Client Request FY<year>.xlsx`.
- Never a tab of the working paper and never saved inside it.

## Layout - one sheet only

1. Row 1: entity name (bold).
2. Row 2: `<Section> - client document request | Year end: <date>`.
3. Row 3: a short request appropriate to the listed documents, e.g. `Please provide copies of the invoices and credit notes listed below.`
4. Numbered, plain section headings: `1. Transactions`, `2. Selected invoices`.
5. Table columns, in the ledger's own order:

   `# | Account_Code | Account_Name | Date | Counterparty | Reference | Txn_Type | Narrative | Amount (R) | Document requested`

6. A bold total row per section.

### General documents: a separate simple list below the transactions

- Use `Document required | Details to include` for registers, ledgers and other general records. Do not repeat account, date, reference or amount columns that are irrelevant to these requests.
- Keep it on the same sheet. Preserve the transaction-table column widths above; two visual text blocks can span those existing columns without merged cells.
- Keep narrative paragraphs unmerged and unwrapped. Continue long text on the next line within its block; working-paper narratives use A through H then continue from A.
- One blank row before and after each heading, and between a note block and its table. Restart transaction numbering at 1 within each section after additions/removals.
- If an item appears in multiple approved groups, one set of supporting documents is sufficient. Do not silently combine groups or change the selection.

## Rules

- Dates `dd/mm/yyyy`; amounts `#,##0.00`, traceable to the relevant ledger lines. Define whether the row represents a selected GL line or the whole document; do not silently substitute an aggregated invoice amount for a selected line amount. Explain any intentional difference internally.
- `Document requested` is a short document name, e.g. **Tax invoice**, **Credit note** or **Signed journal voucher**, set from `Txn_Type`. Put any essential extra support in one short section note, not a repeated paragraph on every row.
- Membership/conference invoice requests default to invoice copies only. Do not append generic delivery notes, proof of service, purchase orders, attendance lists or payment evidence unless an agreed procedure specifically needs them.
- For credit notes, request the listed notes and any required related invoices/authorisation/cancellation support. Request the existing debtors/customer transaction report separately; do not ask the client to trace each item through the ledger or construct our allocation work.
- For a member database, start with names/codes and add category/status only where needed to identify fee-paying members. Request history or exit lists only where necessary for the agreed period. Do not automatically ask for contact details or every available database field.
- No materiality, no sample size, no interval, no "key item", no coverage, no testing rationale.
- No "Provided (Y/N)" or response column unless the user asks for one.
- No broad confirmations section. A specific unresolved invoice-number request may ask for a copy or confirmation the number was unused. Keep other explanations focused and agree them separately.
- Reuse reliable event-date evidence already held, including organiser website evidence. Do not request all event dates, planning packs or delegate lists again without a specific outstanding need and agreed scope.
- Keep selection groups as separate sections; do not merge them into one table.
- Do not apply Freeze Panes unless the user explicitly requests it for this workbook. New client request workbooks must be unfrozen; preserve existing pane settings when editing unless asked to change them.

## Covering email

- Short, no amounts, no "material", no "largest", no methodology.
- Match the user's normal relationship with the client: `Hi [Name], hope you are well. Could you please assist by providing the invoices and credit notes for the attached schedule? Could you also send us...`
- Mention essential general documents explicitly in the email (e.g. debtors report and member register) so the client does not overlook the bottom of the workbook. Avoid rigid headings or a formal template unless requested.
- Do not add evidence requests to the email that are not in the agreed schedule. Draft in the conversation when requested; drafting is not sending.

## Page layout

- A4 landscape, fit to one page wide, gridlines off, no freeze panes.
- Wrap the long `Details to include` column and set row heights explicitly from the text length.
  openpyxl does not auto-fit, and a default row height clips the wrapped text.
- Put a manual page break before a section heading rather than letting a heading fall at the foot of a
  page. Render to PDF and read every page before sending.
- Keep each section block whole: a table that starts on one page should not finish on the next.

## Check before sending

- Every line traces to the ledger extract (account + reference + amount).
- Every transaction matches an approved selection and its section scope. Check active tables, not excluded-item logs or historical support tabs. Do not run an old generator that would restore superseded samples.
- On an open workbook, verify the live state rather than relying on an older saved copy. Check section counts, sequential numbering and that every total covers the actual retained rows.
- Totals recalculate.
- Screenshot the sheet and fix clipped columns or headers.
- Scan the sheet for the words materiality, sample, interval, testing, coverage, selection - there should
  be none.
