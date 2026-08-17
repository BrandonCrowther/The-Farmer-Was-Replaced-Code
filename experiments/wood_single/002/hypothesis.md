# exp-002 — finish-and-score (single-tile reroll-before-walk)

**Hypothesis.** hay_single's exact champion paradigm (reroll-before-walk
companion service, `REROLL_LIMIT=5`, own-position memory) transfers
directly to wood_single: a Tree's companion is always Grass, Bush, or
Carrot (never Tree itself — Polyculture.md excludes the plant's own
species), so this single-tile design never plants a second Tree
anywhere, sidestepping 001's 2.44x neighbor-growth-penalty entirely.
`own_tile_ready()` must directly `plant(Entities.Tree)` rather than use
`Common.get_planting_instructions(Entities.Tree)` — that table entry
deliberately plants *Grass* instead (a wood-farming-pattern quirk noted
in Common.py's own comment, for a different multi-tile "farm" use case,
not for growing the plant itself).

**Variable.** hay_single's champion (Entities.Hay/Items.Hay) →
wood_single (Entities.Tree/Items.Wood), same `REROLL_LIMIT=5`.

**Metric.** The completion modal's verdict and displayed time —
wood_single's first-ever score.

**Baseline.** 001: base yield 2,560, full-multiplier yield 409,600
(160x), growth 34,718 ticks isolated. Projects `500,000,000/409,600 ≈
1,221` harvests if every one hits full multiplier (matches
carrots_single's harvest count almost exactly).

**Procedure.**
1. `saves/wood_single/main.py`: direct adaptation of hay_single's
   champion, target-gated on `Items.Wood`.
2. `tools/cycle.sh wood_single exp-wood_single-002-r1 --from <worktree>`.
3. Read `SHOT=` with vision for the time and rank; read `OUTPUT=` for
   the diagnostic line.

**Falsifier.** If the run fails to terminate, or the multiplier hit
rate is far below hay_single's own established rate at this
`REROLL_LIMIT`, check whether Tree's companion-satisfaction mechanics
genuinely mirror Hay's (free-Grass rate, reroll cost) rather than
assuming they must.
