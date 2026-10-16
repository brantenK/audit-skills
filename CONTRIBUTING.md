# Contributing

## Improving a skill

The easiest way: use the tool. `audit-skills improve submit <proposal>` opens an issue with a scrubbed
lesson. Good lessons are:

- **specific**: what the agent did wrong and what it should do instead,
- **general**: true for other engagements, not just one client,
- **free of client data**: no names, amounts, account numbers or file paths.

The maintainer turns accepted lessons into changes to `skills/` or `methodology/`.

## Code changes

```bash
git clone https://github.com/brantenK/audit-skills
cd audit-skills
python -m venv .venv && . .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pytest
```

Rules:

- Tests use synthetic data only. Never commit real ledgers, trial balances, statements or client names.
- Keep the skills short and procedural. One skill per procedure.
- Anything that writes to a user's workbook must respect live-mode approval and back up first.
- New behaviour needs a test.

## Licence

By contributing you agree that your contribution is licensed under AGPL-3.0.
