"""Regression gates for public, proportionate audit workflow instructions."""
from pathlib import Path

import pytest

from audit_skills import install


ROOT = Path(__file__).resolve().parents[1]


def skill(name):
    return (ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8")


def test_client_request_separates_records_from_auditor_procedures():
    text = skill("client-request-workbook")
    assert "Document required | Details to include" in text
    assert "do not ask the client to trace" in text
    assert "invoice copies only" in text
    assert "evidence already held" in skill("event-dates-cutoff")
    assert "Hi [Name], hope you are well" in text


@pytest.mark.parametrize("name", ["audit-sampling", "audit-sampling-pack"])
def test_sampling_preserves_scope_count_and_history(name):
    text = skill(name).lower()
    assert "lead-sheet" in text
    assert "income in advance" in text
    assert "remaining count" in text or "retained count" in text
    assert "approval" in text and "replacements" in text
    assert "history" in text or "audit trail" in text
    assert "not a new systematic draw" in text or "not a newly validated systematic draw" in text


def test_minutes_and_testing_status_do_not_overstate_evidence():
    text = skill("audit-conventions")
    assert "Minutes: insights, not an automatic new audit exercise" in text
    assert "Selection totals are not amounts verified" in text
    assert "they do not establish a misstatement" in text
    assert "Do not automatically create six sheets" in skill("completeness-combined")
    assert "Leave documentary invoice fields and test results blank" in skill("working-paper-700-series")


def test_new_sampling_skills_are_installed_with_refinements(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    install.install_skills("opencode", project=True)
    for name in ("audit-sampling", "audit-sampling-pack"):
        target = tmp_path / ".opencode" / "skills" / name / "SKILL.md"
        assert target.is_file()
        assert "Read `audit-conventions` first." in target.read_text(encoding="utf-8")


def test_notes_are_findings_only_and_anchored():
    text = skill("audit-conventions")
    assert "Notes: findings only, always anchored" in text
    assert "unless the user asks for one" in text
    assert "Every note must be anchored" in text
    assert "dead text" in text
    assert "Never use notes for procedure descriptions" in text
    assert "sweep the whole workbook" in text


def test_evidence_search_includes_sent_items():
    text = skill("audit-conventions")
    assert "Search Sent Items as well as the Inbox" in text
    assert "scans with no text layer" in text
    assert "A document already held is not outstanding" in text


def test_rebuild_keeps_prior_year_border_convention():
    assert "does not license a new border style" in skill("audit-conventions")
    assert "does not license a new border style" in skill("wp-analytical-standard")
    assert "Never box every cell" in skill("audit-conventions")


def test_file_mode_save_flattens_rich_text():
    assert "flattens" in skill("audit-conventions")
    assert "verify per character" in skill("audit-conventions")


def test_client_request_page_layout_is_checked():
    text = skill("client-request-workbook")
    assert "A4 landscape" in text
    assert "manual page break" in text
    assert "openpyxl does not auto-fit" in text


def test_cash_count_guidance_covers_rate_and_date():
    text = skill("audit-working-paper")
    assert "Cash on hand and foreign currency" in text
    assert "rate implied by the foreign bank account" in text
    assert "An undated count sheet is a documentation weakness" in text


def test_bundle_index_lists_every_skill():
    index = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    for path in (ROOT / "skills").iterdir():
        if (path / "SKILL.md").is_file():
            assert f"skills/{path.name}/SKILL.md" in index
