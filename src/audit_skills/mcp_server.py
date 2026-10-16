"""MCP server exposing the mechanical procedures to any agent (stdio).

Live-mode Excel tools refuse to write unless the user has approved the workbook from a terminal.
"""

from __future__ import annotations

import datetime as dt
from pathlib import Path

from . import improve, stats
from .config import load_engagement, sample_requirement
from .excel import live
from .ledger import filter_accounts, read_balances, read_gl
from .procedures import cutoff as cutoff_mod
from .procedures import extract as extract_mod
from .procedures import sample as sample_mod
from .procedures import template as template_mod
from .procedures import tie as tie_mod
from .procedures import vouch as vouch_mod

try:  # mcp 2.x
    from mcp.server.mcpserver import MCPServer as _Server
except ImportError:  # mcp 1.x
    from mcp.server.fastmcp import FastMCP as _Server  # type: ignore

server = _Server("audit-skills")


def _eng(folder: str | None):
    eng = load_engagement(Path(folder) if folder else None)
    if eng is None:
        raise ValueError("No engagement config found. Ask the user to run 'audit-skills engagement init' "
                         "in the engagement folder.")
    return eng


@server.tool()
def engagement_info(folder: str | None = None) -> dict:
    """Materiality, year end, category and settings for the engagement containing `folder`."""
    stats.record("mcp:engagement_info")
    return _eng(folder).to_dict()


@server.tool()
def gl_extract(gl_path: str, accounts: list[str], out_path: str, entity: str, title: str,
               period_note: str = "Source: general ledger detail.") -> dict:
    """Write a client-facing extract of ledger lines for the given accounts (ledger columns only)."""
    stats.record("mcp:gl_extract")
    lines = filter_accounts(read_gl(Path(gl_path)), accounts)
    return extract_mod.gl_extract(lines, Path(out_path), entity, title, period_note)


@server.tool()
def rollforward(gl_path: str, tb_path: str, accounts: list[str], py_tb_path: str | None = None) -> dict:
    """Opening + movement = closing per account, agreed to the TB; flags opening differences to the
    prior-year audited TB (often an unposted auditor adjustment)."""
    stats.record("mcp:rollforward")
    lines = read_gl(Path(gl_path))
    tb = read_balances(Path(tb_path))
    py = read_balances(Path(py_tb_path)) if py_tb_path else None
    rows = tie_mod.rollforward(lines, tb, accounts, py)
    return {"accounts": [r.to_dict() for r in rows], "bridge": tie_mod.bridge(rows)}


@server.tool()
def sample_plan(balances: dict[str, float], level_of_risk: str, folder: str | None = None,
                select: bool = True) -> dict:
    """Material accounts (100%) and remainder sample to the minimum coverage, with the sufficiency sentence."""
    stats.record("mcp:sample_plan")
    eng = _eng(folder)
    req = sample_requirement(eng.category, level_of_risk)
    p = sample_mod.plan(balances, eng.performance_materiality, eng.individually_significant, req)
    if select:
        sample_mod.select_remainder(p)
    return p.to_dict()


@server.tool()
def vouch_bank(gl_path: str, accounts: list[str], bank_path: str, days: int = 3, payments: bool = True) -> dict:
    """Match ledger items to bank statement lines (CSV or Excel with date and amount, or debit/credit)."""
    stats.record("mcp:vouch_bank")
    from .ledger import _rows
    lines = filter_accounts(read_gl(Path(gl_path)), accounts)
    bank = vouch_mod.read_bank(_rows(Path(bank_path)))
    matches = vouch_mod.match(lines, bank, days, payments)
    return {"summary": vouch_mod.summary(matches), "items": [
        {"account": m.gl.account, "date": m.gl.date.isoformat() if m.gl.date else None,
         "reference": m.gl.reference, "amount": abs(m.gl.net), "status": m.status,
         "bank_date": m.bank.date.isoformat() if m.bank and m.bank.date else None,
         "bank_description": m.bank.description if m.bank else None,
         "bank_source": m.bank.source if m.bank else None, "note": m.note} for m in matches]}


@server.tool()
def cutoff_table(events: list[dict], year_end: str) -> list[dict]:
    """Assess event dates against year end. Each event: account, name, start (yyyy-mm-dd), end, source, confirmed."""
    stats.record("mcp:cutoff_table")
    evs = [cutoff_mod.Event(e["account"], e["name"],
                            dt.date.fromisoformat(e["start"]) if e.get("start") else None,
                            dt.date.fromisoformat(e["end"]) if e.get("end") else None,
                            e.get("source", ""), e.get("confirmed", True)) for e in events]
    return cutoff_mod.assess(evs, dt.date.fromisoformat(year_end))


@server.tool()
def template_inspect(path: str) -> dict:
    """Sheets, formula counts and external links (Caseware etc.) in a prior-year workbook."""
    stats.record("mcp:template_inspect")
    return template_mod.inspect(Path(path))


@server.tool()
def excel_live_status(workbook: str) -> dict:
    """Is the workbook open in Excel, and has the user approved live mode for it?"""
    return live.status(workbook)


@server.tool()
def excel_live_write(workbook: str, sheet: str, top_left: str, values: list[list],
                     folder: str | None = None) -> dict:
    """Write values into a workbook open in Excel. Needs the user's approval; backs up first;
    takes a screenshot when the engagement has screenshots switched on."""
    stats.record("mcp:excel_live_write")
    eng = load_engagement(Path(folder) if folder else Path(workbook).parent)
    shot = bool(eng and eng.screenshots)
    return live.write(workbook, sheet, top_left, values, screenshot=shot)


@server.tool()
def propose_improvement(skill: str, lesson: str, folder: str | None = None) -> dict:
    """Record a lesson for a skill (scrubbed of client data). The user approves it before it is used."""
    eng = load_engagement(Path(folder) if folder else None)
    terms = ([eng.client] + eng.client_terms) if eng else []
    p = improve.propose(skill, lesson, terms)
    return {"proposal": p.name, "text": p.read_text(encoding="utf-8"),
            "next": "Ask the user to review it and run: audit-skills improve apply " + p.name}


def main() -> None:
    server.run()
