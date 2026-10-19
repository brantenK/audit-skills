"""Content gates for the skills shipped in the repository.

The repository is public: it must contain methodology only - no client names,
engagement figures, client account codes or machine-specific paths. Skills also
follow house format: a SKILL.md per folder, frontmatter name matching the folder,
the read-conventions-first line, and the grey-only colour palette.
"""

from __future__ import annotations

import re
from pathlib import Path

SKILLS_DIR = Path(__file__).resolve().parents[1] / "skills"

# Client names and engagement-specific identifiers seen in source material.
# These must never appear in the public repository.
BANNED_TERMS = ["GKD", "SAIMM", "Isizwe", "AMS Haden", "Buismet", "583066", "30120"]

# Colour values outside the grey-only palette (allowed: D9D9D9, F2F2F2).
BANNED_COLOURS = [
    "00B0F0",  # blue key items
    "00B050",  # green systematic sample
    "FFFF00",  # yellow reversals
    "D9E1F2",  # light blue account headers
    "FFFFC8",  # light yellow nature notes
    "008000",  # dark green tick text
    "FF0000",  # red
    "0000FF",  # blue
]

COLOUR_PATTERNS = [
    re.compile(r"\.color\s*=\s*\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\)"),
    re.compile(r"Font\.Color"),
]


def all_skill_files():
    return sorted(p for p in SKILLS_DIR.rglob("*") if p.is_file())


def test_every_skill_folder_has_skill_md():
    for d in sorted(SKILLS_DIR.iterdir()):
        if d.is_dir():
            assert (d / "SKILL.md").is_file(), f"{d.name} has no SKILL.md"


def test_frontmatter_name_matches_folder():
    for d in sorted(SKILLS_DIR.iterdir()):
        f = d / "SKILL.md"
        if not f.is_file():
            continue
        text = f.read_text(encoding="utf-8")
        m = re.search(r"^name:\s*(\S+)", text, re.M)
        assert m, f"{d.name}: SKILL.md has no frontmatter name"
        assert m.group(1) == d.name, f"{d.name}: frontmatter name {m.group(1)} != folder name"


def test_skills_read_conventions_first():
    for d in sorted(SKILLS_DIR.iterdir()):
        if d.name == "audit-conventions":
            continue
        f = d / "SKILL.md"
        if not f.is_file():
            continue
        assert "Read `audit-conventions` first." in f.read_text(encoding="utf-8"), d.name


def test_no_client_data_in_skills():
    for p in all_skill_files():
        rel = p.relative_to(SKILLS_DIR)
        text = p.read_text(encoding="utf-8", errors="replace")
        for term in BANNED_TERMS:
            assert term not in text, f"{rel} contains banned term {term!r}"
        for colour in BANNED_COLOURS:
            assert colour not in text.upper(), f"{rel} contains non-grey colour {colour!r}"
        for pat in COLOUR_PATTERNS:
            assert not pat.search(text), f"{rel} sets a raw colour value"
