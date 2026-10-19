---
name: wp-analytical-standard
description: House standard for the Analytical sheet of an audit working paper - use when building or rebuilding an Analytical sheet, applying tick marks, legends or superscript formatting.
---

# Working-paper Analytical and tick-mark standard

Read `audit-conventions` first.

How every working paper must look when it uses an Analytical sheet, legends or tick marks.
Client-agnostic: bracketed values like `<PM>`, `<Section>`, `<GL file>` are per-engagement inputs.

## 0. Preconditions

- Follow `audit-conventions` §8 Excel mode: work live in the open workbook via xlwings (rich-text tick formatting needs live Excel). Live mode needs the user's `audit-skills approve` first - show what will be written, wait for approval, verify after, and keep the backup / preview / verify discipline.

## 1. Analytical sheet layout (top to bottom)

1. **Headers** - client name, year-end, section name, WP ref (e.g. `750-1`), preparer initials (reviewer/date blank). No CaseWare links (`=_xll...`): strip them and hardcode text.
2. **Objective** - one line, section-specific (e.g. identify large or unusual movements vs prior period).
3. **ROMM block** - Completeness / Occurrence / Accuracy and allocation / Cut-off / Presentation. When a section is occurrence-only in scope: set Completeness and Cut-off to `Low` with rationale in the next column: `No direct procedures in this section; addressed via trade payables subsequent-payments and accrual testing`.
4. **Materiality** - PM and trivial threshold from the engagement config (never hard-coded).
5. **Procedures** - TB/GL agreement and IPE (ISA 330 / ISA 500.9) boilerplate only. No section-irrelevant steps (e.g. no gross-profit procedure on an OPEX sheet).
6. **Work-done TB table** - category blocks (§2). This is the body of the sheet.
7. **Legends** - tick key, styled per §4.
8. **Conclusion** - `Based on procedures performed and results obtained we have reasonable assurance that <section> are not materially misstated.`
9. **Never on an Analytical sheet:** monthly analysis, Notes/N1-N3 sections, gross-profit analysis (unless the section genuinely has COGS linkage).

## 2. Category-block table (the prior-year pattern)

Stack one block per lead-schedule category. Each block:

```
<code>  <account name>          <CY amount>   BTB <ref> | <PY amount>   BPYTB
...                                                             (one row per account)
Total <Category>                =SUM(...)     ^ BAFS  | =SUM(...)     ^ BPYAFS   (bold)
<blank spacer row>
```

- Columns: A code/label, B name, D CY, E CY tick, F PY, G PY tick. No %-change column.
- CY from GL recompute (debit - credit, exact cents); PY from the final prior-year TB. Nil-balance TB accounts with no GL rows are shown at `0.00`.
- Amounts formatted `#,##0.00`.
- Each subtotal is a live `=SUM` over its own block; the grand total sums the subtotal cells (`=D40+D46+...`), never a re-typed number.
- Grand total row: `Grand Total - <section>`, must tie to the TB to the cent (and the PY total to the PY TB). If a scoped-out group is included only for the tie-out, label it `Total <group> (see <other section>)`.
- GL-extract pseudo-rows (`None`, `TOTAL (...)`) are excluded from the table - flag them in the report.

## 3. Bold and borders

- **Detail rows:** not bold, no borders.
- **Subtotal rows:** bold, top border single-thin, bottom border double-thick.
- **Grand total:** bold, top double-thick, bottom double-thick.
- Excel shares edges between adjacent rows, so style top-down (subtotals before grand total) and verify edge-aware: a detail row above a subtotal legitimately shows the subtotal's top border on its bottom edge; a spacer below shows the double on its top edge.
- Verify by sweeping every table row: detail rows non-bold and borderless (apart from shared edges); total rows match the pattern exactly.

## 4. Tick-mark and legend standard (mandatory)

All text black, Arial. The structure is what matters:

| Element | Format | Size | Style |
|---|---|---|---|
| Anchor (first letter: `B`, `V`, `^`) | baseline, black | 10 | bold (whole tick cell bold) |
| Following letters (`TB`, `PYTB`, `AFS`, `GL`...) | **superscript**, black | 8 | bold |
| Reference number (`750`, `700`...) | baseline, black, **never superscript** | 10 | bold |

Rendered: `B`+raised-`TB`+`750`; `B`+raised-`PYTB`; `^ B`+raised-`AFS`; a lone `^` stays plain.

- **Legend cells** (column A of the Legends block): same treatment; description text plain.
- Table tick columns: CY tick (e.g. `BTB 750`) in E, PY tick (`BPYTB`) in G - every populated tick cell bold.
- Superscript must be applied per-character via live Excel (`GetCharacters(Start, Length)`); bulk value-writes do not carry it. Set size and superscript on the same character range in the same pass.

### xlwings recipe (live book only)

```python
PATTERNS = {'BTB 750': (2, 2), 'BPYTB': (2, 4), '^ BAFS': (4, 3),
            '^ BPYAFS': (4, 5), 'BTB': (2, 2), 'BAFS': (2, 3),
            'BPYAFS': (2, 4), 'OGL': (2, 2), 'VPYWP': (2, 4)}
for addr in tick_cells:  # E/G table ticks + legend column-A ticks
    c = ws.range(addr)
    v = c.value
    c.api.Font.Bold = True
    if (p := PATTERNS.get(v)):
        ch = c.api.GetCharacters(Start=p[0], Length=p[1]).Font
        ch.Superscript, ch.Size = True, 8
    if v == 'BTB 750':  # reference number stays on the baseline (adjust per ref)
        num = c.api.GetCharacters(Start=5, Length=3).Font
        num.Superscript, num.Size = False, 10
```

Verify per-character afterwards (superscript + size on samples); value-only sweeps miss superscript regressions.

## 5. Done-check for any Analytical rebuild

- [ ] Headers/objective/ROMM/materiality converted, CaseWare links gone
- [ ] Category blocks with live SUM subtotals; grand total ties the TB (CY and PY)
- [ ] No monthly block, no Notes, no irrelevant analysis
- [ ] Bold/border sweep clean (§3)
- [ ] Tick sweep: bold + superscript + baseline reference numbers, all text black (§4)
- [ ] No `#DIV/0!` / `#REF!`; other sheets untouched; backup exists; user visually confirmed before save
