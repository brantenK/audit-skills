"""Where things live: bundled skills, the user's home folder for the tool, engagement config."""

from __future__ import annotations

import os
from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent


def data_dir() -> Path:
    """Bundled skills and methodology.

    Installed wheel: audit_skills/_data. Source checkout: the repo root.
    """
    bundled = PACKAGE_DIR / "_data"
    if bundled.exists():
        return bundled
    return PACKAGE_DIR.parent.parent


def skills_dir() -> Path:
    return data_dir() / "skills"


def methodology_file() -> Path:
    return data_dir() / "methodology" / "conventions.yaml"


def home(create: bool = True) -> Path:
    """The tool's own folder for the user: overrides, proposals, approvals, stats, temp files."""
    root = Path(os.environ.get("AUDIT_SKILLS_HOME", Path.home() / ".audit-skills"))
    if create:
        root.mkdir(parents=True, exist_ok=True)
    return root


def overrides_dir() -> Path:
    p = home() / "overrides"
    p.mkdir(parents=True, exist_ok=True)
    return p


def proposals_dir() -> Path:
    p = home() / "proposals"
    p.mkdir(parents=True, exist_ok=True)
    return p


def temp_dir() -> Path:
    p = home() / "tmp"
    p.mkdir(parents=True, exist_ok=True)
    return p


ENGAGEMENT_FILE = ".audit-skills/engagement.yaml"


def find_engagement(start: Path | None = None) -> Path | None:
    """Walk up from start looking for an engagement config."""
    cur = (start or Path.cwd()).resolve()
    for folder in [cur, *cur.parents]:
        candidate = folder / ENGAGEMENT_FILE
        if candidate.exists():
            return candidate
    return None
