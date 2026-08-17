# exp-007 — 5-tile reroll pipeline (combined optimization)

**Hypothesis.** 006 confirmed reroll-before-walk cuts single-tile
handling from ≈2,422 to ≈1,571 ticks/visit, but a single tile stays
growth-bound (≈7,196 growth >> ≈1,571 handling) so the saving is
invisible there. Combining it with multi-tile pipelining should surface
it: with the cheaper handling, the idle-elimination crossing point moves
from N≈2.23 (004's model, 3 tiles already past it) to `N ≥ 7196/1,571 ≈
4.58` — **5 tiles**, spaced pairwise wrapped distance ≥4 (self-collision
safe, brute-force confirmed fittable on the 8x8 wrapped world:
`(0,0),(0,4),(2,2),(2,6),(4,0)`), should land near the handling floor,
projecting **≈1,571 ticks/harvest, ≈52.2 carrots/tick** — more than
double 004's adopted 3-tile champion (3,430.43 ticks/harvest, ≈23.88
carrots/tick).

**Variable.** 004/005's 3-tile walk-always design → 5-tile round-robin
with 006's reroll-before-walk (`REROLL_LIMIT=5`, memory dict, Grass-free
assumption gated on the memory dict per 006's bug fix) for each tile's
own companion resolution.

**Metric.** `TICKS_PER_HARVEST` over a bounded probe (75 cycles, 15 full
rounds across 5 tiles), compared to 004's real 3,430.43.

**Baseline.** 004: 3,430.43 ticks/harvest (3-tile, walk-always).
006: single-tile handling ≈1,571 (idle-subtracted).

**Procedure.**
1. `saves/carrots_single/main.py`: 5 tiles, round-robin, 006's reroll
   logic per tile (own memory dict shared across all 5, since it's one
   drone), instrumented the same way as 003/004/006.
2. `tools/cycle.sh carrots_single exp-carrots_single-007-r1 --from <worktree>`.
3. Read `OUTPUT=`; compute `TICKS_PER_HARVEST`, compare to 004 and to
   the ≈1,571 floor prediction.

**Falsifier.** If `TICKS_PER_HARVEST` doesn't clearly beat 004's
3,430.43, either the round-robin commute between the 5 farm tiles
(distinct from the ≤3-range companion walk) is eating the savings, or 5
tiles' extra companion traffic doesn't reduce revisit-interval idle as
cleanly as the single-tile model assumed (e.g. reroll attempts on one
tile competing for the same nearby positions memory across tiles isn't
modeled). Say what the model missed if it misses, don't just report the
miss.
