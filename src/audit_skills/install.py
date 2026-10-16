"""Install the skills and the MCP server into Claude Code, Codex CLI and OpenCode.

Skill folders (user level):
  claude   -> ~/.claude/skills/<skill>/SKILL.md
  codex    -> ~/.agents/skills/<skill>/SKILL.md
  opencode -> ~/.config/opencode/skills/<skill>/SKILL.md
With project=True the same folders are created under the current directory
(.claude/skills, .agents/skills, .opencode/skills).

MCP server:
  claude   -> `claude mcp add --scope user audit-skills -- audit-skills mcp` (printed if claude is not on PATH)
  codex    -> [mcp_servers.audit-skills] in ~/.codex/config.toml
  opencode -> "mcp": {"audit-skills": {...}} in ~/.config/opencode/opencode.json
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

from . import paths

AGENTS = ("claude", "codex", "opencode")
MARKER = "<!-- audit-skills: user additions -->"


def _skill_root(agent: str, project: bool) -> Path:
    base = Path.cwd() if project else Path.home()
    return {
        "claude": base / ".claude" / "skills",
        "codex": base / ".agents" / "skills",
        "opencode": (base / ".opencode" / "skills") if project else base / ".config" / "opencode" / "skills",
    }[agent]


def bundled_skills() -> list[Path]:
    return sorted(p for p in paths.skills_dir().iterdir() if (p / "SKILL.md").exists())


def render_skill(skill_dir: Path) -> str:
    """Base skill text plus the user's approved additions for that skill."""
    text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    notes = paths.overrides_dir() / skill_dir.name / "NOTES.md"
    if notes.exists() and notes.read_text(encoding="utf-8").strip():
        text = text.rstrip() + f"\n\n{MARKER}\n## Your additions (approved by you)\n" + notes.read_text(encoding="utf-8")
    return text


def install_skills(agent: str, project: bool = False) -> list[str]:
    root = _skill_root(agent, project)
    done = []
    for sd in bundled_skills():
        target = root / sd.name
        target.mkdir(parents=True, exist_ok=True)
        (target / "SKILL.md").write_text(render_skill(sd), encoding="utf-8")
        for extra in sd.iterdir():  # supporting files, if any
            if extra.name != "SKILL.md":
                dest = target / extra.name
                if extra.is_dir():
                    shutil.copytree(extra, dest, dirs_exist_ok=True)
                else:
                    shutil.copy2(extra, dest)
        done.append(str(target))
    return done


def _codex_mcp(command: list[str]) -> str:
    cfg = Path.home() / ".codex" / "config.toml"
    cfg.parent.mkdir(parents=True, exist_ok=True)
    text = cfg.read_text(encoding="utf-8") if cfg.exists() else ""
    if "[mcp_servers.audit-skills]" in text:
        return f"already configured in {cfg}"
    block = (f'\n[mcp_servers.audit-skills]\ncommand = "{command[0]}"\n'
             f"args = {json.dumps(command[1:])}\n")
    cfg.write_text(text.rstrip() + "\n" + block, encoding="utf-8")
    return f"added to {cfg}"


def _opencode_mcp(command: list[str]) -> str:
    cfg = Path.home() / ".config" / "opencode" / "opencode.json"
    cfg.parent.mkdir(parents=True, exist_ok=True)
    data = json.loads(cfg.read_text(encoding="utf-8")) if cfg.exists() and cfg.read_text(encoding="utf-8").strip() else {}
    data.setdefault("$schema", "https://opencode.ai/config.json")
    data.setdefault("mcp", {})["audit-skills"] = {"type": "local", "command": command, "enabled": True}
    cfg.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return f"added to {cfg}"


def _claude_mcp(command: list[str]) -> str:
    cmd = ["claude", "mcp", "add", "--scope", "user", "audit-skills", "--", *command]
    if not shutil.which("claude"):
        return "Claude Code not found on PATH. Run this yourself:\n  " + " ".join(cmd)
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0 and "already exists" not in (res.stderr + res.stdout):
        return "Could not add automatically. Run this yourself:\n  " + " ".join(cmd)
    return "added with claude mcp add"


def install_mcp(agent: str) -> str:
    command = ["audit-skills", "mcp"]
    return {"claude": _claude_mcp, "codex": _codex_mcp, "opencode": _opencode_mcp}[agent](command)
