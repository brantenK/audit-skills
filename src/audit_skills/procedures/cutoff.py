"""Event-date table for cut-off of prepaid expenses and income received in advance."""

from __future__ import annotations

import datetime as dt
import re
from dataclasses import dataclass


@dataclass
class Event:
    account: str
    name: str
    start: dt.date | None
    end: dt.date | None = None
    source: str = ""
    confirmed: bool = True


def financial_year(d: dt.date, year_end_month: int, year_end_day: int) -> int:
    """Financial year label = calendar year in which that financial year ends."""
    ye_this = dt.date(d.year, year_end_month, year_end_day)
    return d.year if d <= ye_this else d.year + 1


def assess(events: list[Event], year_end: dt.date) -> list[dict]:
    rows = []
    for e in events:
        start = e.start
        flags = []
        if start is None:
            after = None
            fy = None
            flags.append("date not found")
        else:
            after = start > year_end
            fy = financial_year(start, year_end.month, year_end.day)
            if not after:
                flags.append("event on or before year end: balance should have been released")
            if (start - year_end).days > 365:
                flags.append("more than 12 months after year end: non-current")
            label_fy = [int(y) for y in re.findall(r"FY\s?(\d{4})", e.name, flags=re.IGNORECASE)]
            if label_fy and fy not in label_fy:
                flags.append(f"account label says FY{label_fy[-1]} but event falls in FY{fy}")
        if not e.confirmed:
            flags.append("not confirmed by organiser source")
        rows.append({"account": e.account, "event": e.name,
                     "start": start.isoformat() if start else None,
                     "end": e.end.isoformat() if e.end else None,
                     "after_year_end": after, "financial_year": fy,
                     "source": e.source, "flags": flags})
    return rows
