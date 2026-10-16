"""Read general ledger lines and account balances from Excel or CSV exports.

Column names are matched case-insensitively against a list of common aliases, so most
accounting-package exports work without a mapping file.
"""

from __future__ import annotations

import csv
import datetime as dt
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import openpyxl

GL_COLUMNS = ["Account_Code", "Account_Name", "Date", "Counterparty", "Reference",
              "Txn_Type", "Narrative", "Debit", "Credit", "Net", "Month"]

ALIASES = {
    "account": ["account_code", "account", "account code", "acc", "gl account", "chart"],
    "account_name": ["account_name", "account name", "account description", "description of account"],
    "date": ["date", "account date", "transaction date", "posting date"],
    "counterparty": ["counterparty", "bank / customer / supplier", "customer / supplier", "supplier", "customer", "name"],
    "reference": ["reference", "ref", "document", "doc no"],
    "txn_type": ["txn_type", "transaction type", "type", "src"],
    "narrative": ["narrative", "description", "details", "memo"],
    "debit": ["debit", "dr"],
    "credit": ["credit", "cr"],
    "balance": ["balance", "closing balance", "amount", "account balance"],
}


@dataclass
class GLLine:
    account: str
    account_name: str | None
    date: dt.date | None
    counterparty: str | None
    reference: str | None
    txn_type: str | None
    narrative: str | None
    debit: float
    credit: float

    @property
    def net(self) -> float:
        """Debit less credit (credits negative)."""
        return round(self.debit - self.credit, 2)

    @property
    def month(self) -> str | None:
        return self.date.strftime("%b %Y") if self.date else None


def _rows(path: Path, sheet: str | None = None) -> list[list]:
    path = Path(path)
    if path.suffix.lower() in (".csv", ".txt"):
        with path.open(newline="", encoding="utf-8-sig") as fh:
            return [row for row in csv.reader(fh)]
    wb = openpyxl.load_workbook(path, data_only=True, read_only=True)
    ws = wb[sheet] if sheet else wb.worksheets[0]
    return [list(r) for r in ws.iter_rows(values_only=True)]


def _find_header(rows: list[list], required: Iterable[str]) -> tuple[int, dict[str, int]]:
    required = list(required)
    for i, row in enumerate(rows[:50]):
        cells = [str(c).strip().lower() if c is not None else "" for c in row]
        found: dict[str, int] = {}
        for key, names in ALIASES.items():
            for j, cell in enumerate(cells):
                if cell in names and key not in found:
                    found[key] = j
        if all(k in found for k in required):
            return i, found
    raise ValueError(f"Could not find a header row with columns {required}")


def _num(v) -> float:
    if v is None or v == "":
        return 0.0
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).replace(",", "").replace(" ", "").replace("R", "")
    neg = s.startswith("(") and s.endswith(")")
    s = s.strip("()")
    try:
        x = float(s)
    except ValueError:
        return 0.0
    return -x if neg else x


def _date(v) -> dt.date | None:
    if v is None or v == "":
        return None
    if isinstance(v, dt.datetime):
        return v.date()
    if isinstance(v, dt.date):
        return v
    s = str(v).strip()
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d", "%d-%m-%Y", "%Y%m%d", "%d %b %Y"):
        try:
            return dt.datetime.strptime(s[:10] if fmt != "%d %b %Y" else s, fmt).date()
        except ValueError:
            continue
    return None


def read_gl(path: Path, sheet: str | None = None) -> list[GLLine]:
    rows = _rows(path, sheet)
    h, col = _find_header(rows, ["account", "debit", "credit"])
    out: list[GLLine] = []

    def get(row, key):
        j = col.get(key)
        return row[j] if j is not None and j < len(row) else None

    for row in rows[h + 1:]:
        acc = get(row, "account")
        if acc is None or str(acc).strip() == "":
            continue
        out.append(GLLine(
            account=str(acc).strip(),
            account_name=get(row, "account_name"),
            date=_date(get(row, "date")),
            counterparty=get(row, "counterparty"),
            reference=get(row, "reference"),
            txn_type=get(row, "txn_type"),
            narrative=get(row, "narrative"),
            debit=_num(get(row, "debit")),
            credit=_num(get(row, "credit")),
        ))
    return out


def read_balances(path: Path, sheet: str | None = None) -> dict[str, float]:
    """Account balances, debit positive and credit negative.

    Accepts either a signed 'balance' column or separate debit and credit columns.
    """
    rows = _rows(path, sheet)
    try:
        h, col = _find_header(rows, ["account", "balance"])
        signed = True
    except ValueError:
        h, col = _find_header(rows, ["account", "debit", "credit"])
        signed = False
    out: dict[str, float] = {}
    for row in rows[h + 1:]:
        acc = row[col["account"]] if col["account"] < len(row) else None
        if acc is None or str(acc).strip() == "":
            continue
        acc = str(acc).split(" : ")[0].strip()
        if signed:
            val = _num(row[col["balance"]])
        else:
            val = _num(row[col["debit"]]) - _num(row[col["credit"]])
        out[acc] = round(out.get(acc, 0.0) + val, 2)
    return out


def filter_accounts(lines: list[GLLine], accounts: Iterable[str]) -> list[GLLine]:
    wanted = {a.strip() for a in accounts}
    return [ln for ln in lines if ln.account in wanted]
