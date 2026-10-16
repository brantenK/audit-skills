"""Improvement loop.

1. propose: the agent (or user) writes down a lesson for a skill. The text is scrubbed of client data.
2. apply:   the user approves it into their own layer. It is added to that skill when skills are installed.
3. submit:  optional. The user sends the scrubbed proposal to the public repo as an issue.
            The maintainer reviews it and, if accepted, changes the shared skill.
"""

from __future__ import annotations

import datetime as dt
import re
import shutil
import subprocess
from pathlib import Path

from . import paths

UPSTREAM = "brantenK/audit-skills"

_PATTERNS = [
    (re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+"), "[email]"),
    (re.compile(r"\+?\d[\d ()-]{8,}\d"), "[phone/number]"),
    (re.compile(r"\bR\s?\d[\d ,]*(\.\d{2})?\b"), "[amount]"),
    (re.compile(r"\b\d{1,3}(,\d{3})+(\.\d{2})?\b"), "[amount]"),
    (re.compile(r"\b\d+\.\d{2}\b"), "[amount]"),
    (re.compile(r"\b\d{6,}\b"), "[number]"),
    (re.compile(r"[A-Za-z]:\\[^\s\"']+"), "[path]"),
    (re.compile(r"(?<![\w.])/(?:home|Users|mnt|tmp)/[^\s\"']+"), "[path]"),
]


def scrub(text: str, extra_terms: list[str] | None = None) -> str:
    """Remove things that look like client data. A person still reviews the result."""
    out = text
    for term in sorted(extra_terms or [], key=len, reverse=True):
        if term.strip():
            out = re.sub(re.escape(term), "[client]", out, flags=re.IGNORECASE)
    for pat, repl in _PATTERNS:
        out = pat.sub(repl, out)
    return out


def propose(skill: str, lesson: str, extra_terms: list[str] | None = None) -> Path:
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    path = paths.proposals_dir() / f"{stamp}-{skill}.md"
    body = scrub(lesson, extra_terms)
    path.write_text(f"---\nskill: {skill}\ncreated: {stamp}\nstatus: proposed\n---\n\n{body.strip()}\n",
                    encoding="utf-8")
    return path


def list_proposals() -> list[dict]:
    out = []
    for p in sorted(paths.proposals_dir().glob("*.md")):
        head = p.read_text(encoding="utf-8").split("---")
        meta = dict(line.split(": ", 1) for line in head[1].strip().splitlines() if ": " in line) if len(head) > 2 else {}
        out.append({"file": p.name, **meta})
    return out


def _parse(path: Path) -> tuple[dict, str]:
    parts = path.read_text(encoding="utf-8").split("---", 2)
    meta = dict(line.split(": ", 1) for line in parts[1].strip().splitlines() if ": " in line)
    return meta, parts[2].strip()


def apply(proposal_file: str) -> Path:
    """Add an approved lesson to the user's layer for that skill."""
    p = paths.proposals_dir() / proposal_file
    meta, body = _parse(p)
    skill = meta["skill"]
    notes = paths.overrides_dir() / skill / "NOTES.md"
    notes.parent.mkdir(parents=True, exist_ok=True)
    with notes.open("a", encoding="utf-8") as fh:
        fh.write(f"\n- {body}\n")
    p.write_text(p.read_text(encoding="utf-8").replace("status: proposed", "status: applied"), encoding="utf-8")
    return notes


def submit(proposal_file: str, dry_run: bool = False) -> str:
    """Open an issue on the public repo with the scrubbed proposal (needs the GitHub CLI)."""
    p = paths.proposals_dir() / proposal_file
    meta, body = _parse(p)
    if dry_run:
        return f"Would submit to {UPSTREAM}:\n\nskill: {meta.get('skill')}\n\n{body}"
    if not shutil.which("gh"):
        raise RuntimeError("GitHub CLI (gh) not found. Install it, run 'gh auth login', then try again.")
    title = f"Skill improvement: {meta.get('skill')}"
    result = subprocess.run(
        ["gh", "issue", "create", "--repo", UPSTREAM, "--title", title, "--label", "skill-proposal",
         "--body", f"Skill: `{meta.get('skill')}`\n\n{body}\n\n_Submitted with audit-skills. Scrubbed of client data and reviewed by the submitter._"],
        capture_output=True, text=True)
    if result.returncode != 0:
        # label may not exist on the repo yet: retry without it
        result = subprocess.run(
            ["gh", "issue", "create", "--repo", UPSTREAM, "--title", title,
             "--body", f"Skill: `{meta.get('skill')}`\n\n{body}"],
            capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip())
    p.write_text(p.read_text(encoding="utf-8").replace("status: applied", "status: submitted")
                 .replace("status: proposed", "status: submitted"), encoding="utf-8")
    return result.stdout.strip()
