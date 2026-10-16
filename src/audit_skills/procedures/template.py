"""Prior-year workbook inspection and roll-forward in file mode.

File mode uses openpyxl. It cannot keep cached values of external links (Caseware and other
workbook links); inspect() reports them so the user can choose live mode instead.
"""

from __future__ import annotations

import re
import shutil
import zipfile
from pathlib import Path

import openpyxl

LINK_PATTERN = re.compile(r"\[\d+\]")


def inspect(path: Path) -> dict:
    path = Path(path)
    with zipfile.ZipFile(path) as z:
        external = [n for n in z.namelist() if n.startswith("xl/externalLinks/") and n.endswith(".xml")]
    wb = openpyxl.load_workbook(path, keep_links=False)
    sheets = []
    link_cells = 0
    ref_errors = 0
    for ws in wb.worksheets:
        n_formulas = 0
        for row in ws.iter_rows():
            for c in row:
                if isinstance(c.value, str) and c.value.startswith("="):
                    n_formulas += 1
                    if LINK_PATTERN.search(c.value):
                        link_cells += 1
                    if "#REF!" in c.value:
                        ref_errors += 1
        sheets.append({"name": ws.title, "rows": ws.max_row, "cols": ws.max_column, "formulas": n_formulas})
    return {"path": str(path), "sheets": sheets, "external_link_parts": len(external),
            "cells_using_external_links": link_cells, "formulas_with_ref_errors": ref_errors,
            "advice": ("Workbook has external links. Use live mode (Excel) to keep them, or accept that "
                       "file mode will clear those cells.") if (external or link_cells) else "No external links."}


def roll(src: Path, dst: Path, sheet: str, new_label: str, old_label: str | None = None,
         accept_link_loss: bool = False) -> dict:
    """Copy the prior-year workbook, rename the paper sheet and shift year labels.

    Only the named sheet's header area (first 60 rows) has year labels replaced. Cells that use
    external links are cleared only when accept_link_loss is True; otherwise the function stops.
    """
    src, dst = Path(src), Path(dst)
    info = inspect(src)
    if info["cells_using_external_links"] and not accept_link_loss:
        raise RuntimeError("Prior-year workbook uses external links. Re-run with accept_link_loss=True "
                           "or use live mode to keep them.")
    if dst.exists():
        raise FileExistsError(f"{dst} already exists; choose another name")
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    wb = openpyxl.load_workbook(dst, keep_links=False)
    ws = wb[sheet]
    old = old_label or sheet
    ws.title = new_label
    cleared = 0
    replaced = 0
    for row in ws.iter_rows(min_row=1, max_row=min(ws.max_row, 60)):
        for c in row:
            v = c.value
            if isinstance(v, str) and v.startswith("=") and LINK_PATTERN.search(v):
                c.value = None
                cleared += 1
            elif isinstance(v, int) and str(v) == old:
                c.value = int(new_label) if new_label.isdigit() else new_label
                replaced += 1
            elif isinstance(v, str) and old in v and not v.startswith("="):
                c.value = v.replace(old, new_label)
                replaced += 1
    # clear remaining external-link formulas elsewhere in the sheet
    for row in ws.iter_rows(min_row=61):
        for c in row:
            if isinstance(c.value, str) and c.value.startswith("=") and LINK_PATTERN.search(c.value):
                c.value = None
                cleared += 1
    wb.save(dst)
    return {"path": str(dst), "sheet": new_label, "labels_replaced": replaced, "link_cells_cleared": cleared,
            "other_sheets": [s for s in wb.sheetnames if s != new_label],
            "next": "Clear risk ratings, prior-year notes and testing rows; update balances and materiality."}
