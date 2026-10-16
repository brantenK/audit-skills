"""Material accounts (100%) and remainder sampling, with coverage and the sufficiency sentence."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class SamplePlan:
    material: dict[str, float]
    remainder: dict[str, float]
    total: float
    pm: float
    individually_significant: float
    min_number: int | None
    min_coverage: float | None
    selected_remainder: dict[str, float] = field(default_factory=dict)

    @property
    def material_total(self) -> float:
        return round(sum(abs(v) for v in self.material.values()), 2)

    @property
    def remainder_total(self) -> float:
        return round(sum(abs(v) for v in self.remainder.values()), 2)

    @property
    def remainder_is_material(self) -> bool:
        return self.remainder_total >= self.pm

    @property
    def tested(self) -> float:
        return round(self.material_total + sum(abs(v) for v in self.selected_remainder.values()), 2)

    @property
    def coverage(self) -> float:
        return 0.0 if not self.total else round(self.tested / abs(self.total), 4)

    @property
    def remainder_coverage(self) -> float:
        if not self.remainder_total:
            return 1.0
        return round(sum(abs(v) for v in self.selected_remainder.values()) / self.remainder_total, 4)

    @property
    def sufficient(self) -> bool | None:
        if self.min_coverage is None:
            return None
        return self.coverage >= self.min_coverage

    def sentence(self) -> str:
        base = (f"We tested {self.coverage:.0%} of the balance (material accounts 100% and "
                f"{self.remainder_coverage:.0%} of the remainder)")
        if self.min_coverage is None:
            return base + ". Minimum coverage is not set: complete the level of risk."
        if self.sufficient:
            return (base + f", which exceeds the minimum coverage of {self.min_coverage:.0%}. "
                    "We are therefore satisfied that the sample is sufficient.")
        return (base + f", which is below the minimum coverage of {self.min_coverage:.0%}. "
                "Select further items from the remainder.")

    def to_dict(self) -> dict:
        return {
            "material": self.material, "remainder": self.remainder,
            "selected_remainder": self.selected_remainder,
            "material_total": self.material_total, "remainder_total": self.remainder_total,
            "remainder_is_material": self.remainder_is_material, "total": self.total,
            "tested": self.tested, "coverage": self.coverage,
            "min_number": self.min_number, "min_coverage": self.min_coverage,
            "sufficient": self.sufficient, "sentence": self.sentence(),
        }


def plan(balances: dict[str, float], pm: float, individually_significant: float,
         requirement: dict | None = None) -> SamplePlan:
    material = {a: v for a, v in balances.items() if abs(v) >= individually_significant}
    remainder = {a: v for a, v in balances.items() if a not in material and v}
    total = round(sum(abs(v) for v in balances.values()), 2)
    req = requirement or {}
    return SamplePlan(material, remainder, total, pm, individually_significant,
                      req.get("number"), req.get("coverage"))


def select_remainder(p: SamplePlan) -> SamplePlan:
    """Pick the largest remainder items until minimum coverage is reached (or all are taken)."""
    p.selected_remainder = {}
    for acc, val in sorted(p.remainder.items(), key=lambda kv: -abs(kv[1])):
        if p.min_coverage is not None and p.coverage >= p.min_coverage:
            break
        p.selected_remainder[acc] = val
    return p
