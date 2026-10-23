---
name: audit-skills
description: Audit working-paper skills for AI agents - teaches an agent how an auditor prepares and reviews Excel working papers (roll forward last year's paper, agree to the TB and lead sheet, sample and coverage, vouch to bank, cut-off, revenue, OPEX, PPE, leases and more). Use for any external audit working-paper task; start with audit-conventions, then open the matching sub-skill.
---

# Audit skills

A bundle of audit working-paper skills. Each sub-skill lives in `skills/<name>/SKILL.md`.

## How to use

1. Always read `skills/audit-conventions/SKILL.md` first. Every other skill depends on its ground rules.
2. Pick the sub-skill whose description matches the task below and follow its `SKILL.md`.
3. Shared house conventions are in `methodology/conventions.yaml`.
4. Two skills bundle a Python template builder (`scripts/build_template.py`) that needs Python 3.10+ and openpyxl.

No client data is included; this bundle is methodology only (see `PRIVACY.md`).

## Sub-skills

- `audit-conventions` (`skills/audit-conventions/SKILL.md`): Ground rules for any audit working-paper task - read before creating, editing or sending any working paper, extract or schedule for an audit engagement.
- `age-analysis-transformation` (`skills/age-analysis-transformation/SKILL.md`): Convert a transaction-heavy creditors or debtors age analysis report into a one-line-per-vendor audit summary sheet that reconciles to the source grand totals - use when a raw client age analysis needs restructuring into a working-paper summary.
- `audit-manager` (`skills/audit-manager/SKILL.md`): Senior-auditor review mode for Excel audit working papers - hygiene, formula and presentation review, sample selection guidance and monthly summaries, with mandatory preview, approval, verification and rollback. Use when asked to review, check or manage working papers.
- `audit-monthly-summary` (`skills/audit-monthly-summary/SKILL.md`): Build a GL monthly summary by adding Net Balance and Month helper columns to a transaction detail sheet and a two-column SUMIF-driven Monthly Analysis sheet reconciled to the trial balance - use when the user asks for a monthly analysis or monthly summary of a general ledger account.
- `audit-planning-questionnaire` (`skills/audit-planning-questionnaire/SKILL.md`): Restructure a verbose audit planning questionnaire (IT environment / gathering information) from an expanded multi-row layout into a compact, bordered three-panel table in working-paper format. Use when a sheet holds raw questionnaire text spread over many rows and must become an auditable planning document.
- `audit-working-paper` (`skills/audit-working-paper/SKILL.md`): Review, enhance or build an audit working paper in Excel to review standard - documentation rules (ISA 230), sheet structure and borders, tick marks, coverage boxes, client requests and troubleshooting. Use whenever a working paper must be created, reviewed or brought up to standard.
- `new-section-paper` (`skills/new-section-paper/SKILL.md`): Build only the requested sheets when no prior-year paper exists, with GL and supporting-documentation tables and a traceable audit trail.
- `client-gl-extract` (`skills/client-gl-extract/SKILL.md`): Produce a plain extract of selected general ledger lines to send to the client so they know which items to support - use when the user wants to send a sample or list of transactions to the client.
- `client-request-workbook` (`skills/client-request-workbook/SKILL.md`): One-sheet client requests from approved transactions, plus a simple general-document list and natural covering email.
- `audit-sampling` (`skills/audit-sampling/SKILL.md`): Simple count-based selection with exact lead-sheet scope, agreed counts and safe corrections.
- `audit-sampling-pack` (`skills/audit-sampling-pack/SKILL.md`): Reviewer-defensible sampling packs with separate pools, systematic provenance and honest coverage.
- `completeness-combined` (`skills/completeness-combined/SKILL.md`): Single-section revenue completeness testing - sequence-gap analysis (shared vs split numbering), master-to-billing, cut-off and reversal screen, and earned-vs-billed matching, each procedure with its reason - use when testing completeness of revenue for any client.
- `employee-costs-update` (`skills/employee-costs-update/SKILL.md`): Roll an employee costs working paper (e.g. a monthly insurance premium account) forward by locating the account in the client GL, extracting its 12 monthly transactions, and updating the ledger and WP sheets with formula-based totals. Use when an employee-cost paper must be updated from the prior year to the current year.
- `event-dates-cutoff` (`skills/event-dates-cutoff/SKILL.md`): Confirm event or conference dates against organiser sources to test cut-off of prepaid expenses and income received in advance - use when balances relate to future events and the user needs evidence of when they take place.
- `financial-liabilities` (`skills/financial-liabilities/SKILL.md`): Reconcile other financial liabilities (instalment sale agreements) between the Existence and Valuation working paper and the Analytical working paper - flexible column mapping, gap analysis, current/non-current split and tick marks. Use when an analytical schedule must be updated from an existence and valuation source.
- `lease-liabilities-working-paper` (`skills/lease-liabilities-working-paper/SKILL.md`): Build and review instalment agreement / lease liability working papers - classify short term vs long term capital per IFRS for SMEs, extract movements from amortization schedules and reconcile to the trial balance. Use for any lease or instalment sale liability section.
- `operating-expense-skill` (`skills/operating-expense-skill/SKILL.md`): Builds a complete 8-sheet expense testing working paper template (Procedures, Analytical, Occurrence-Material, Occurrence-Sensitive, Completeness, Cut-off, Journals, Presentation) in placeholder or CaseWare mode via the bundled scripts/build_template.py - use when the user asks for a new operating-expense section working paper from scratch.
- `ppe-analytical-sheet` (`skills/ppe-analytical-sheet/SKILL.md`): Rebuilds the Analytical (movement analysis) sheet of a PPE audit working paper - exact row and column layout, border rules, tick-mark structure, group sub-totals and totals reconciliation to the trial balance - use when creating or updating the Analytical tab of any PPE working paper.
- `revenue-testing-skill` (`skills/revenue-testing-skill/SKILL.md`): Builds a complete 7-sheet revenue testing working paper template (Procedures, Analytical, Occurrence-AAC, Completeness, Cut-off, Journals, Presentation) in placeholder or CaseWare mode via the bundled scripts/build_template.py - use when the user asks for a new revenue section working paper from scratch.
- `sample-and-coverage` (`skills/sample-and-coverage/SKILL.md`): Split a balance into material accounts tested 100% and a remainder that is sampled, select the sample, compute coverage against the TB and write the sufficiency conclusion - use when planning, selecting or documenting a sample for an audit section.
- `tie-to-tb` (`skills/tie-to-tb/SKILL.md`): Agree a section's balances to the trial balance and lead sheet, and roll each account forward from opening balance through the year's ledger movements to closing - use whenever a working paper or extract must reconcile to the TB or lead sheet.
- `trial-balance-analytical` (`skills/trial-balance-analytical/SKILL.md`): Restructure an analytical schedule whose subtotals sit above their detail lines - moves subtotals below the details, replaces typed subtotals with SUM formulas, strips account codes, and adds variance and materiality columns - use whenever a trial-balance analytical schedule needs rebuilding into proper working-paper form.
- `update-from-prior-year` (`skills/update-from-prior-year/SKILL.md`): Roll a prior-year audit working paper forward to the current year by editing the prior-year workbook in place - use when the user asks to prepare a current-year paper and a prior-year paper exists. Not for building a new paper from scratch.
- `vouch-to-bank` (`skills/vouch-to-bank/SKILL.md`): Trace ledger payments or receipts to bank statements by amount, date and payee - use when the user asks to verify transactions against bank statements or check year-end bank balances against the TB.
- `working-paper-700-series` (`skills/working-paper-700-series/SKILL.md`): Builds CaseWare-style 700-series occurrence working papers (700.55 pattern) with multi-stream selections - header, risk box, A-T vouching tables, VAT formulas, casts, coverage box, notes, legends and conclusion. Use for any client, any year.
- `wp-analytical-standard` (`skills/wp-analytical-standard/SKILL.md`): House standard for the Analytical sheet of an audit working paper - use when building or rebuilding an Analytical sheet, applying tick marks, legends or superscript formatting.
- `wp-opex-occurrence` (`skills/wp-opex-occurrence/SKILL.md`): Standard for the Accuracy and occurrence sheet of an operating-expenses testing workbook - use when building or rebuilding it. Covers category-block layout, live selection tables, the sampling chain, group-level materiality, prior-year sample-table grammar and workbook hygiene. Scoped to OPEX occurrence (completeness and cut-off out of scope).
- `wp-procedures-standard` (`skills/wp-procedures-standard/SKILL.md`): House standard for the Procedures sheet of a testing working paper - use when building or rewriting it. Covers the header block, ROMM ratings, assertion codes, procedure numbering, ISA references, scope trimming and live-edit mechanics.

## Licence

AGPL-3.0, see `LICENSE`. Source: https://github.com/brantenK/audit-skills
