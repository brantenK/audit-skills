# audit-skills

Audit working-paper skills and tools for AI coding agents: **Claude Code**, **Codex CLI** and **OpenCode**.

It teaches your agent how an auditor prepares working papers: update last year's paper instead of
rebuilding it, agree everything to the TB and lead sheet, sample material accounts 100% and the remainder
to minimum coverage, vouch to bank, send the client a plain ledger extract, and confirm event dates for
cut-off. The skills get better as you use them, and only with your approval.

**No client data ever leaves your machine.** The repository holds methodology only. See [PRIVACY.md](PRIVACY.md).

## What you get

| Skill | Use it to |
|---|---|
| `audit-conventions` | Ground rules every other skill follows (read first) |
| `update-from-prior-year` | Roll last year's working paper forward by editing it, not rebuilding it |
| `tie-to-tb` | Agree balances to the TB and lead sheet; roll accounts forward; spot unposted prior-year adjustments |
| `sample-and-coverage` | Material accounts 100%, remainder sampled, coverage and the sufficiency sentence |
| `vouch-to-bank` | Trace ledger items to bank statements by amount, date and payee |
| `client-gl-extract` | A plain extract of ledger lines to send to the client |
| `event-dates-cutoff` | Event and conference dates for prepaid and income-received-in-advance cut-off |

Plus an MCP server so the agent can run the mechanical steps (extracts, roll-forwards, sampling, bank
matching, cut-off tables, Excel live editing) instead of improvising them.

## Install (Windows, macOS or Linux)

Needs Python 3.10 or later.

```bash
pipx install "git+https://github.com/brantenK/audit-skills"          # file mode
pipx install "audit-skills[live] @ git+https://github.com/brantenK/audit-skills"   # + live Excel (Windows/macOS with Excel)
audit-skills install            # installs into Claude Code, Codex CLI and OpenCode
audit-skills install -a claude  # or just one agent
```

Where the skills go:

| Agent | Skills | MCP server |
|---|---|---|
| Claude Code | `~/.claude/skills/` | `claude mcp add --scope user audit-skills -- audit-skills mcp` |
| Codex CLI | `~/.agents/skills/` | `[mcp_servers.audit-skills]` in `~/.codex/config.toml` |
| OpenCode | `~/.config/opencode/skills/` | `mcp.audit-skills` in `~/.config/opencode/opencode.json` |

Use `--project` to install into the current folder instead.

## Start an engagement

In the engagement folder:

```bash
audit-skills engagement init
```

It asks for client, year end, performance materiality, clearly trivial and client category, and saves them
in `.audit-skills/engagement.yaml` in that folder only. Every skill reads materiality from here, so it is
never hard-coded in a paper.

## Excel: file mode and live mode

- **File mode** (default): edits the `.xlsx` file on disk. Works everywhere. Cannot keep cached values of
  external links such as Caseware links; the tool warns you first.
- **Live mode** (xlwings): edits a workbook that is open in Excel, keeps Caseware links, and Excel does the
  recalculation. It only works after **you** approve that workbook:

  ```bash
  audit-skills approve "C:\path\to\paper.xlsx"     # asks you to confirm; lasts 8 hours
  audit-skills revoke  "C:\path\to\paper.xlsx"
  ```

  The approval must be typed in a terminal, so an agent cannot approve itself. A backup copy is saved
  before every write. Switch on screenshots for an engagement (`--screenshots` at `engagement init`) to
  save an image of each edited range in `.audit-skills/evidence/` as proof of the change.

## How the skills improve

1. When you correct your agent, it records the lesson: `propose_improvement` (MCP) or
   `audit-skills improve propose <skill> "<lesson>"`. Amounts, account numbers, emails, paths and the
   client's name are scrubbed.
2. You review it and approve it into **your own layer**: `audit-skills improve apply <proposal>`, then
   `audit-skills install` to refresh your agents. The shared skills are not touched.
3. If you want others to benefit, send it to this repository: `audit-skills improve submit <proposal>`.
   It shows you exactly what will be sent and asks before sending. The maintainer reviews it before it
   changes the shared skills.

Firm-wide changes (sample table, legends, formatting) go in `~/.audit-skills/overrides/conventions.yaml`
and override the base methodology.

## Commands

```text
audit-skills install / approve / revoke / live-status
audit-skills engagement init | show
audit-skills template inspect <file> | roll <src> <dst> --sheet 2025 --year 2026
audit-skills extract --gl <file> --accounts 8730/101,8730/102 --out <file> --entity "..." --title "..."
audit-skills rollforward --gl <file> --tb <file> --accounts ... [--py-tb <file>]
audit-skills sample --balances <file> --risk Medium
audit-skills vouch --gl <file> --accounts ... --bank <bank-lines.csv>
audit-skills cutoff --events <events.csv> --year-end 2026-06-30
audit-skills improve propose | list | apply | submit
audit-skills stats on | off | show
```

## Methodology

The base methodology is in [`methodology/conventions.yaml`](methodology/conventions.yaml): individually
significant at 75% of performance materiality, the sample-size table by client category and risk, legends
and formatting (Arial, black text, grey shading only). Sample-table rows marked `null` are not set yet:
fill them in for your firm before relying on them.

This is a tool to support a qualified auditor's work. It does not replace professional judgement, the
firm's methodology or the auditing standards. You remain responsible for the audit.

## Status

Version 0.1. Tested on synthetic data. Live mode needs Windows or macOS with Excel and has not yet been
through wide use; report problems as issues.

## Licence

[AGPL-3.0](LICENSE). If you change this tool and let others use it over a network, you must share your
changes under the same licence.
