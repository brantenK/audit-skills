"""Methodology (base + user/firm overrides) and engagement settings."""

from __future__ import annotations

import datetime as dt
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

import yaml

from . import paths


def _deep_merge(base: dict, extra: dict) -> dict:
    out = dict(base)
    for k, v in (extra or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def load_methodology() -> dict[str, Any]:
    """Base methodology merged with the user's or firm's overrides (overrides win)."""
    base = yaml.safe_load(paths.methodology_file().read_text(encoding="utf-8")) or {}
    override = paths.home(create=False) / "overrides" / "conventions.yaml"
    if override.exists():
        base = _deep_merge(base, yaml.safe_load(override.read_text(encoding="utf-8")) or {})
    return base


@dataclass
class Engagement:
    client: str
    year_end: str  # ISO date
    performance_materiality: float
    clearly_trivial: float
    category: str = "Category C"
    overall_materiality: float | None = None
    level_of_risk: str | None = None  # the auditor's judgement; left blank until set
    client_terms: list[str] = field(default_factory=list)  # extra words to scrub from proposals
    screenshots: bool = False  # live mode: capture the edited range after each write

    @property
    def individually_significant(self) -> float:
        pct = load_methodology().get("materiality", {}).get("individually_significant_pct_of_pm", 0.75)
        return round(self.performance_materiality * pct, 2)

    @property
    def year_end_date(self) -> dt.date:
        return dt.date.fromisoformat(self.year_end)

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["individually_significant"] = self.individually_significant
        return d


def save_engagement(folder: Path, eng: Engagement) -> Path:
    target = folder / paths.ENGAGEMENT_FILE
    target.parent.mkdir(parents=True, exist_ok=True)
    data = asdict(eng)
    target.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    return target


def load_engagement(start: Path | None = None) -> Engagement | None:
    found = paths.find_engagement(start)
    if not found:
        return None
    data = yaml.safe_load(found.read_text(encoding="utf-8")) or {}
    return Engagement(**data)


def sample_requirement(category: str, risk: str) -> dict[str, Any]:
    table = load_methodology().get("sample_table", {})
    row = table.get(category, {}).get(risk)
    if row is None:
        raise KeyError(f"No sample-table row for {category!r} / {risk!r}")
    return row
