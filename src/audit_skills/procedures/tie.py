"""Roll each account forward and agree it to the trial balance.

Sign convention: debit positive, credit negative, throughout.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass

from ..ledger import GLLine


@dataclass
class RollForward:
    account: str
    opening_per_ledger: float  # derived: closing per TB less the year's net movement
    debits: float
    credits: float
    closing_per_tb: float
    opening_per_py_audited: float | None = None

    @property
    def movement(self) -> float:
        return round(self.debits - self.credits, 2)

    @property
    def closing_per_ledger(self) -> float:
        return round(self.opening_per_ledger + self.movement, 2)

    @property
    def opening_difference(self) -> float | None:
        """Ledger opening less prior-year audited closing. Non-zero usually means an unposted
        prior-year auditor adjustment."""
        if self.opening_per_py_audited is None:
            return None
        return round(self.opening_per_ledger - self.opening_per_py_audited, 2)

    def to_dict(self) -> dict:
        d = asdict(self)
        d.update(movement=self.movement, closing_per_ledger=self.closing_per_ledger,
                 opening_difference=self.opening_difference)
        return d


def rollforward(lines: list[GLLine], closing_tb: dict[str, float], accounts: list[str],
                py_audited: dict[str, float] | None = None) -> list[RollForward]:
    out = []
    for acc in accounts:
        mine = [ln for ln in lines if ln.account == acc]
        debits = round(sum(ln.debit for ln in mine), 2)
        credits = round(sum(ln.credit for ln in mine), 2)
        closing = round(closing_tb.get(acc, 0.0), 2)
        opening = round(closing - (debits - credits), 2)
        out.append(RollForward(acc, opening, debits, credits, closing,
                               None if py_audited is None else round(py_audited.get(acc, 0.0), 2)))
    return out


def bridge(rf: list[RollForward]) -> dict:
    """Opening + movement = closing, in total. Explains why an extract of the year's lines does not
    equal the closing balance on its own."""
    opening = round(sum(r.opening_per_ledger for r in rf), 2)
    movement = round(sum(r.movement for r in rf), 2)
    closing = round(sum(r.closing_per_tb for r in rf), 2)
    return {"opening": opening, "movement": movement, "closing": closing,
            "agrees": round(opening + movement - closing, 2) == 0}
