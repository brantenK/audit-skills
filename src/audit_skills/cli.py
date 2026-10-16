"""Command-line interface."""

from __future__ import annotations

import csv
import datetime as dt
import json
from pathlib import Path
from typing import List, Optional

import typer

from . import __version__, improve, install as install_mod, stats
from .config import Engagement, load_engagement, sample_requirement, save_engagement
from .excel import approvals, live
from .ledger import _rows, filter_accounts, read_balances, read_gl
from .procedures import cutoff as cutoff_mod
from .procedures import extract as extract_mod
from .procedures import sample as sample_mod
from .procedures import template as template_mod
from .procedures import tie as tie_mod
from .procedures import vouch as vouch_mod

app = typer.Typer(help="Audit working-paper skills and tools for AI coding agents.", no_args_is_help=True)
engagement_app = typer.Typer(help="Engagement settings (materiality, year end, client category).")
template_app = typer.Typer(help="Prior-year working papers.")
improve_app = typer.Typer(help="Lessons that refine the skills. You approve every change.")
stats_app = typer.Typer(help="Opt-in usage counts (off by default).")
app.add_typer(engagement_app, name="engagement")
app.add_typer(template_app, name="template")
app.add_typer(improve_app, name="improve")
app.add_typer(stats_app, name="stats")


def _out(obj) -> None:
    typer.echo(json.dumps(obj, indent=2, default=str))


def _accounts(values: List[str]) -> list[str]:
    out: list[str] = []
    for v in values:
        out += [a.strip() for a in v.split(",") if a.strip()]
    return out


@app.command()
def version() -> None:
    """Show the version."""
    typer.echo(__version__)


@app.command()
def install(agent: List[str] = typer.Option(["claude", "codex", "opencode"], "--agent", "-a",
                                            help="claude, codex, opencode (repeat for several)"),
            project: bool = typer.Option(False, help="Install into the current folder instead of your user folder"),
            mcp: bool = typer.Option(True, help="Also register the MCP server")) -> None:
    """Install the skills (and MCP server) into your agents."""
    for a in agent:
        if a not in install_mod.AGENTS:
            raise typer.BadParameter(f"Unknown agent {a}")
        done = install_mod.install_skills(a, project)
        typer.echo(f"{a}: {len(done)} skills installed")
        if mcp:
            typer.echo(f"{a}: MCP {install_mod.install_mcp(a)}")
    stats.record("install")


@app.command()
def approve(workbook: Path, hours: int = typer.Option(8, help="How long the approval lasts")) -> None:
    """Allow live editing of one workbook open in Excel. Must be run by you in a terminal."""
    typer.echo(f"Allow the agent to edit '{workbook.name}' directly in Excel for {hours} hours?")
    typer.echo("A backup copy is saved before every write.")
    if not typer.confirm("Approve"):
        raise typer.Exit(1)
    until = approvals.grant(workbook, hours)
    typer.echo(f"Approved until {until:%Y-%m-%d %H:%M}.")


@app.command()
def revoke(workbook: Path) -> None:
    """Withdraw live-mode approval for a workbook."""
    approvals.revoke(workbook)
    typer.echo("Approval removed.")


@app.command()
def live_status(workbook: Path) -> None:
    """Is the workbook open in Excel and approved for live mode?"""
    _out(live.status(workbook))


# ---------------- engagement ----------------
@engagement_app.command("init")
def engagement_init(client: str = typer.Option(..., prompt=True),
                    year_end: str = typer.Option(..., prompt="Year end (yyyy-mm-dd)"),
                    pm: float = typer.Option(..., prompt="Performance materiality"),
                    trivial: float = typer.Option(..., prompt="Clearly trivial"),
                    category: str = typer.Option("Category C", prompt=True),
                    overall: Optional[float] = typer.Option(None),
                    screenshots: bool = typer.Option(False, help="Live mode: screenshot each write"),
                    folder: Path = typer.Option(Path("."), help="Engagement folder")) -> None:
    """Create the engagement config in this folder (kept on your machine only)."""
    dt.date.fromisoformat(year_end)
    eng = Engagement(client=client, year_end=year_end, performance_materiality=pm, clearly_trivial=trivial,
                     category=category, overall_materiality=overall, screenshots=screenshots)
    path = save_engagement(folder, eng)
    typer.echo(f"Saved {path}")
    stats.record("engagement:init")


@engagement_app.command("show")
def engagement_show(folder: Path = typer.Option(Path("."))) -> None:
    """Show the engagement settings."""
    eng = load_engagement(folder)
    if not eng:
        typer.echo("No engagement config here. Run: audit-skills engagement init")
        raise typer.Exit(1)
    _out(eng.to_dict())


# ---------------- template ----------------
@template_app.command("inspect")
def template_inspect(path: Path) -> None:
    """Sheets, formulas and external links in a prior-year workbook."""
    _out(template_mod.inspect(path))
    stats.record("template:inspect")


@template_app.command("roll")
def template_roll(src: Path, dst: Path, sheet: str = typer.Option(...), year: str = typer.Option(...),
                  old: Optional[str] = typer.Option(None, help="Old year label if different from the sheet name"),
                  accept_link_loss: bool = typer.Option(False, help="Clear external-link cells in file mode")) -> None:
    """Copy a prior-year paper to a new file and shift the year labels (file mode)."""
    _out(template_mod.roll(src, dst, sheet, year, old, accept_link_loss))
    stats.record("template:roll")


# ---------------- procedures ----------------
@app.command("extract")
def extract(gl: Path = typer.Option(...), accounts: List[str] = typer.Option(..., "--accounts"),
            out: Path = typer.Option(...), entity: str = typer.Option(...), title: str = typer.Option(...),
            note: str = typer.Option("Source: general ledger detail.")) -> None:
    """Client-facing extract of ledger lines (ledger columns only)."""
    lines = filter_accounts(read_gl(gl), _accounts(accounts))
    _out(extract_mod.gl_extract(lines, out, entity, title, note))
    stats.record("extract")


@app.command("rollforward")
def rollforward(gl: Path = typer.Option(...), tb: Path = typer.Option(...),
                accounts: List[str] = typer.Option(..., "--accounts"),
                py_tb: Optional[Path] = typer.Option(None, help="Prior-year audited TB")) -> None:
    """Opening + movement = closing per account, agreed to the TB."""
    rows = tie_mod.rollforward(read_gl(gl), read_balances(tb), _accounts(accounts),
                               read_balances(py_tb) if py_tb else None)
    _out({"accounts": [r.to_dict() for r in rows], "bridge": tie_mod.bridge(rows)})
    stats.record("rollforward")


@app.command("sample")
def sample(balances: Path = typer.Option(..., help="CSV or Excel with account and balance"),
           risk: str = typer.Option(..., help="Low, Medium or High (your judgement)"),
           folder: Path = typer.Option(Path("."))) -> None:
    """Material accounts 100% and remainder sample to minimum coverage."""
    eng = load_engagement(folder)
    if not eng:
        raise typer.BadParameter("No engagement config. Run: audit-skills engagement init")
    p = sample_mod.plan(read_balances(balances), eng.performance_materiality, eng.individually_significant,
                        sample_requirement(eng.category, risk))
    _out(sample_mod.select_remainder(p).to_dict())
    stats.record("sample")


@app.command("vouch")
def vouch(gl: Path = typer.Option(...), accounts: List[str] = typer.Option(..., "--accounts"),
          bank: Path = typer.Option(..., help="Bank lines: CSV or Excel"), days: int = 3,
          receipts: bool = typer.Option(False, help="Match receipts instead of payments")) -> None:
    """Match ledger items to bank statement lines."""
    lines = filter_accounts(read_gl(gl), _accounts(accounts))
    matches = vouch_mod.match(lines, vouch_mod.read_bank(_rows(bank)), days, payments=not receipts)
    _out({"summary": vouch_mod.summary(matches),
          "items": [{"account": m.gl.account, "reference": m.gl.reference, "amount": abs(m.gl.net),
                     "status": m.status, "bank": (m.bank.description if m.bank else None), "note": m.note}
                    for m in matches]})
    stats.record("vouch")


@app.command("cutoff")
def cutoff(events: Path = typer.Option(..., help="CSV: account,name,start,end,source,confirmed"),
           year_end: str = typer.Option(...)) -> None:
    """Event dates against year end, with flags."""
    evs = []
    with events.open(newline="", encoding="utf-8-sig") as fh:
        for r in csv.DictReader(fh):
            evs.append(cutoff_mod.Event(
                r["account"], r["name"],
                dt.date.fromisoformat(r["start"]) if r.get("start") else None,
                dt.date.fromisoformat(r["end"]) if r.get("end") else None,
                r.get("source", ""), str(r.get("confirmed", "true")).lower() in ("true", "yes", "1")))
    _out(cutoff_mod.assess(evs, dt.date.fromisoformat(year_end)))
    stats.record("cutoff")


# ---------------- improve ----------------
@improve_app.command("propose")
def improve_propose(skill: str, lesson: str) -> None:
    """Write down a lesson for a skill. Client data is scrubbed; you review it before use."""
    eng = load_engagement()
    terms = ([eng.client] + eng.client_terms) if eng else []
    p = improve.propose(skill, lesson, terms)
    typer.echo(p.read_text(encoding="utf-8"))
    typer.echo(f"Saved as {p.name}. Approve with: audit-skills improve apply {p.name}")


@improve_app.command("list")
def improve_list() -> None:
    """List proposals and their status."""
    _out(improve.list_proposals())


@improve_app.command("apply")
def improve_apply(proposal: str) -> None:
    """Approve a proposal into your own layer, then re-install skills to use it."""
    notes = improve.apply(proposal)
    typer.echo(f"Added to {notes}. Run 'audit-skills install' to refresh your agents.")


@improve_app.command("submit")
def improve_submit(proposal: str, dry_run: bool = False) -> None:
    """Send a proposal to the public repo so it can improve the shared skills (optional)."""
    preview = improve.submit(proposal, dry_run=True)
    typer.echo(preview)
    if dry_run:
        return
    if not typer.confirm("Send this to the public repository?"):
        raise typer.Exit(1)
    typer.echo(improve.submit(proposal))


# ---------------- stats ----------------
@stats_app.command("on")
def stats_on() -> None:
    """Start recording anonymous usage counts on this machine."""
    stats.set_enabled(True)
    typer.echo("Usage counts on. Only command names, version and date are recorded.")


@stats_app.command("off")
def stats_off() -> None:
    stats.set_enabled(False)
    typer.echo("Usage counts off.")


@stats_app.command("show")
def stats_show() -> None:
    _out({"enabled": stats.enabled(), "entries": stats.show()})


@app.command("mcp")
def mcp() -> None:
    """Run the MCP server (stdio). Agents start this; you do not need to."""
    from .mcp_server import main
    main()
