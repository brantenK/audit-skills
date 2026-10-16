"""Opt-in usage counts. Off by default.

Only the command or skill name, the tool version and the date are recorded. No file names,
client names, amounts or paths. Counts stay on the user's machine; nothing is uploaded in this
version. `audit-skills stats show` prints exactly what is stored.
"""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

from . import __version__, paths


def _settings() -> Path:
    return paths.home() / "settings.json"


def _log() -> Path:
    return paths.home() / "stats.jsonl"


def enabled() -> bool:
    f = _settings()
    return f.exists() and json.loads(f.read_text(encoding="utf-8")).get("stats", False)


def set_enabled(on: bool) -> None:
    f = _settings()
    data = json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}
    data["stats"] = on
    f.write_text(json.dumps(data, indent=2), encoding="utf-8")


def record(name: str) -> None:
    if not enabled():
        return
    entry = {"event": name, "version": __version__, "date": dt.date.today().isoformat()}
    with _log().open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry) + "\n")


def show() -> list[dict]:
    f = _log()
    if not f.exists():
        return []
    return [json.loads(line) for line in f.read_text(encoding="utf-8").splitlines() if line.strip()]


def clear() -> None:
    f = _log()
    if f.exists():
        f.unlink()
