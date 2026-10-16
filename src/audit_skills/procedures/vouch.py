"""Match ledger items to bank statement lines on amount and date."""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass

from ..ledger import GLLine, _date, _num

BANK_ALIASES = {
    "date": ["date", "transaction date", "value date"],
    "description": ["description", "details", "narrative", "payee", "reference"],
    "debit": ["debit", "dr", "payments", "withdrawal"],
    "credit": ["credit", "cr", "receipts", "deposit"],
    "amount": ["amount"],
    "source": ["source", "file", "statement"],
}


@dataclass
class BankLine:
    date: dt.date | None
    description: str
    amount: float  # payments negative, receipts positive
    source: str = ""


@dataclass
class Match:
    gl: GLLine
    status: str  # agreed | not_found | not_a_bank_item
    bank: BankLine | None = None
    note: str = ""


def read_bank(rows: list[list]) -> list[BankLine]:
    """Rows from a CSV or sheet with a header. Either 'amount' (signed) or debit and credit columns."""
    head = None
    cols: dict[str, int] = {}
    for i, row in enumerate(rows[:30]):
        cells = [str(c).strip().lower() if c is not None else "" for c in row]
        found = {}
        for key, names in BANK_ALIASES.items():
            for j, cell in enumerate(cells):
                if cell in names and key not in found:
                    found[key] = j
        if "date" in found and ("amount" in found or ("debit" in found and "credit" in found)):
            head, cols = i, found
            break
    if head is None:
        raise ValueError("Bank file needs a header with date and amount, or date, debit and credit")
    out = []
    for row in rows[head + 1:]:
        d = _date(row[cols["date"]])
        if d is None:
            continue
        if "amount" in cols:
            amt = _num(row[cols["amount"]])
        else:
            # statements often show debits as negative numbers already; take the magnitude
            amt = abs(_num(row[cols["credit"]])) - abs(_num(row[cols["debit"]]))
        desc = str(row[cols["description"]]) if "description" in cols and row[cols["description"]] else ""
        src = str(row[cols["source"]]) if "source" in cols and row[cols["source"]] else ""
        out.append(BankLine(d, desc, round(amt, 2), src))
    return out


NON_BANK_TYPES = ("invoice", "journal", "credit note")


def match(gl: list[GLLine], bank: list[BankLine], days: int = 3, payments: bool = True) -> list[Match]:
    """Match each ledger item to one unused bank line of the same amount within +/- days.

    payments=True: ledger debits (e.g. prepayments paid) are matched to bank outflows.
    Supplier invoices and journals are classified as not bank items.
    """
    used: set[int] = set()
    out: list[Match] = []
    for ln in gl:
        typ = (ln.txn_type or "").lower()
        if any(t in typ for t in NON_BANK_TYPES):
            out.append(Match(ln, "not_a_bank_item",
                             note="Invoice or journal: vouch to the document, not to bank"))
            continue
        target = -abs(ln.debit or ln.credit) if payments else abs(ln.credit or ln.debit)
        best = None
        for i, b in enumerate(bank):
            if i in used or round(b.amount, 2) != round(target, 2):
                continue
            if ln.date and b.date and abs((b.date - ln.date).days) > days:
                continue
            gap = abs((b.date - ln.date).days) if (ln.date and b.date) else 999
            if best is None or gap < best[0]:
                best = (gap, i)
        if best:
            used.add(best[1])
            out.append(Match(ln, "agreed", bank[best[1]]))
        else:
            out.append(Match(ln, "not_found",
                             note=f"No bank line of {abs(target):,.2f} within {days} days"))
    return out


def summary(matches: list[Match]) -> dict:
    s = {"agreed": 0, "not_found": 0, "not_a_bank_item": 0}
    for m in matches:
        s[m.status] += 1
    s["agreed_amount"] = round(sum(abs(m.gl.net) for m in matches if m.status == "agreed"), 2)
    return s
