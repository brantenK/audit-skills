"""Live-mode approvals. Only a person at a terminal can grant one; agents cannot approve themselves."""

from __future__ import annotations

import datetime as dt
import json
import sys
from pathlib import Path

from .. import paths

DEFAULT_HOURS = 8


def _file() -> Path:
    return paths.home() / "approvals.json"


def _key(workbook: Path | str) -> str:
    return str(Path(workbook).resolve()).lower()


def _load() -> dict:
    f = _file()
    return json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}


def grant(workbook: Path | str, hours: int = DEFAULT_HOURS, interactive_check: bool = True) -> dt.datetime:
    """Grant live-mode access to one workbook for a number of hours.

    Refuses when stdin is not an interactive terminal, so an agent running shell commands cannot
    grant itself access.
    """
    if interactive_check and not sys.stdin.isatty():
        raise PermissionError("Approval must be given by a person in an interactive terminal.")
    data = _load()
    until = dt.datetime.now() + dt.timedelta(hours=hours)
    data[_key(workbook)] = until.isoformat(timespec="seconds")
    _file().write_text(json.dumps(data, indent=2), encoding="utf-8")
    return until


def revoke(workbook: Path | str) -> None:
    data = _load()
    data.pop(_key(workbook), None)
    _file().write_text(json.dumps(data, indent=2), encoding="utf-8")


def is_approved(workbook: Path | str) -> bool:
    until = _load().get(_key(workbook))
    return bool(until) and dt.datetime.fromisoformat(until) > dt.datetime.now()
