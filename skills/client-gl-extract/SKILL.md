---
name: client-gl-extract
description: Produce a plain extract of selected general ledger lines to send to the client so they know which items to support - use when the user wants to send a sample or list of transactions to the client.
---

# Client ledger extract

Read `audit-conventions` first.

## What the client gets

- The selected ledger lines, in the ledger's own columns (account, account name, date, counterparty,
  reference, transaction type, narrative, debit, credit, net, month), and a total.
- A three-line header: entity, what the list is, source and period.

## What the client does not get

- Materiality, coverage, risk, conclusions, findings.
- Bank statement references or "already agreed" notes.
- Response columns or boxes, unless the user asks for them.

## Steps

1. Confirm the scope: which accounts and which lines (all, material accounts only, or a sample).
   Accounts must be on the lead sheet for the section.
2. Run `audit-skills extract gl --gl <gl.xlsx> --accounts <list> --out <file.xlsx>`.
3. Check the line count and the total. If the user asks whether it agrees to the lead sheet, explain:
   the extract agrees to the year's movement; opening balance + movement = closing.
4. Save it with a client-facing name (for example `<Section> - GL extract FY<yyyy>.xlsx`).
   Do not leave internal drafts next to it with similar names.
