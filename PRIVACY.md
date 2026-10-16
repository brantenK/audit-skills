# Privacy

## What stays on your machine

Everything about your clients:

- engagement settings (`.audit-skills/engagement.yaml` in the engagement folder),
- working papers, ledgers, trial balances, bank statements and extracts,
- screenshots taken in live mode (`.audit-skills/evidence/`),
- backups made before live-mode writes (`~/.audit-skills/backups/`),
- your approved lessons (`~/.audit-skills/overrides/`).

The tool has no server and makes no network calls of its own, except when **you** run
`audit-skills improve submit`.

## What can leave your machine, and only when you choose

`audit-skills improve submit <proposal>` creates an issue on the public repository with the text of one
lesson. Before it is sent:

1. the text has already been scrubbed: amounts, long numbers (account and ID numbers), emails, phone
   numbers, file paths, and the client name and any extra terms in the engagement config are replaced;
2. the full text is shown to you and you must confirm.

Scrubbing is a safety net, not a guarantee. Read the preview before you confirm.

## Usage counts (opt-in)

Off by default. `audit-skills stats on` records, on your machine only, the name of each command used, the
tool version and the date. Nothing else: no file names, client names, amounts or paths.
`audit-skills stats show` prints exactly what is stored. Version 0.1 does not upload these counts anywhere.

## Your agent

Your AI agent (Claude Code, Codex CLI, OpenCode) and its model provider process what you show it under
their own terms. This tool does not change that. Check your firm's policy before using an AI agent on
client data.
