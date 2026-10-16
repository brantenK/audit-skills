"""Live mode: edit a workbook that is open in Excel, through xlwings.

Rules:
- Only after the user has approved that workbook (`audit-skills approve <workbook>`).
- A backup copy is saved before the first write in each call.
- Values are written in bulk ranges.
- When screenshots are on, the written range is saved as an image in the engagement's evidence folder.
"""

from __future__ import annotations

import datetime as dt
import shutil
from pathlib import Path

from .. import paths
from .approvals import is_approved


class LiveModeUnavailable(RuntimeError):
    pass


def _xw():
    try:
        import xlwings as xw  # type: ignore
    except ImportError as exc:  # pragma: no cover - depends on platform
        raise LiveModeUnavailable("xlwings is not installed. Install with: pip install 'audit-skills[live]'") from exc
    return xw


def open_book(workbook: Path | str):
    """Return the xlwings Book if the workbook is open in a running Excel, else None."""
    xw = _xw()
    target = str(Path(workbook).resolve()).lower()
    name = Path(workbook).name.lower()
    try:
        apps = list(xw.apps)
    except Exception:  # pragma: no cover
        return None
    for app in apps:
        for book in app.books:
            try:
                full = str(Path(book.fullname).resolve()).lower()
            except Exception:
                full = book.name.lower()
            if full == target or book.name.lower() == name:
                return book
    return None


def status(workbook: Path | str) -> dict:
    try:
        book = open_book(workbook)
        available = True
    except LiveModeUnavailable as exc:
        return {"live_available": False, "reason": str(exc), "approved": is_approved(workbook)}
    return {"live_available": available, "open_in_excel": book is not None, "approved": is_approved(workbook)}


def _backup(book, workbook: Path) -> Path:
    folder = paths.home() / "backups"
    folder.mkdir(parents=True, exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    target = folder / f"{workbook.stem}-{stamp}{workbook.suffix}"
    try:
        book.api.SaveCopyAs(str(target))  # Windows: includes unsaved changes, keeps the book's own path
    except Exception:
        if workbook.exists():
            shutil.copy2(workbook, target)  # fallback: last saved version on disk
    return target


def _screenshot(rng, evidence_dir: Path, label: str) -> Path | None:
    evidence_dir.mkdir(parents=True, exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    out = evidence_dir / f"{label}-{stamp}.png"
    try:
        rng.to_png(str(out))
        return out
    except Exception:
        try:
            from PIL import ImageGrab  # type: ignore
            ImageGrab.grab().save(out)
            return out
        except Exception:
            return None


def write(workbook: Path | str, sheet: str, top_left: str, values: list[list], screenshot: bool = False,
          evidence_dir: Path | None = None) -> dict:
    """Write a 2-D block of values (or formulas starting with '=') into the open workbook."""
    workbook = Path(workbook)
    if not is_approved(workbook):
        raise PermissionError(f"Live mode is not approved for {workbook.name}. "
                              f"Ask the user to run: audit-skills approve \"{workbook}\"")
    book = open_book(workbook)
    if book is None:
        raise LiveModeUnavailable(f"{workbook.name} is not open in Excel.")
    backup = _backup(book, workbook)
    ws = book.sheets[sheet]
    rng = ws.range(top_left).resize(len(values), max(len(r) for r in values))
    rng.value = values  # one bulk write
    shot = None
    if screenshot:
        shot = _screenshot(rng, evidence_dir or (workbook.parent / ".audit-skills" / "evidence"),
                           f"{workbook.stem}-{sheet}-{top_left}")
    return {"written": rng.address, "backup": str(backup), "screenshot": str(shot) if shot else None}


def read(workbook: Path | str, sheet: str, address: str) -> list:
    workbook = Path(workbook)
    if not is_approved(workbook):
        raise PermissionError(f"Live mode is not approved for {workbook.name}.")
    book = open_book(workbook)
    if book is None:
        raise LiveModeUnavailable(f"{workbook.name} is not open in Excel.")
    return book.sheets[sheet].range(address).value
