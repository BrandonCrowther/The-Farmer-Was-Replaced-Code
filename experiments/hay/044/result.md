# exp-044 — multi-tile-scheduled — result

**Outcome.** rejected — a clean, decisive negative result that closes
multi-tile-per-drone for Hay with a precise, quantified reason, rather
than leaving 041's promising idle-time finding as an open question.

**Numbers.** 80 cycles on tile A, 26 on tile B (`HARVESTS_B/HARVESTS_A =
0.325` — matches 041's measured ~32% hit rate almost exactly, confirming
the scheduling logic correctly triggers only on A's cheap cycles).
**Total: 106 harvests, 142,329 ticks → 1,342.73 ticks/harvest** — *worse*
than 039's real single-tile baseline (≈1,300).

**Why, precisely.** The idle window 041 measured (≈492 ticks average on
A's hit-cycles) is smaller than the **minimum possible cost of a B-visit**:
own-tile handling (harvest 200 + replant 200 = 400) plus the cheapest
possible commute at distance 1 (200 each way = 400) = **800 ticks, even in
the best case where B's own request is also a free hit**. `800 - 492 =
308` tick shortfall on every B-visit, before counting anything about B's
*own* servicing cost (which, drawn from the same distribution as A's, is
expensive ~68% of the time B is visited, making the real average shortfall
larger still). There is no scheduling refinement that fixes this — even
gating B's visit on B *also* being cheap only reduces how often the loss
is incurred, not whether each occurrence is a loss (800 > 492 regardless).

**Baseline.** 039: single-tile champion, main drone, real ≈1,300
ticks/harvest.

**Noise floor.** Not established (single 80-cycle probe), but the gap
(1,342.73 vs 1,300, ≈3.3%) is small and directionally consistent with the
308-tick-per-B-visit shortfall computed independently from first
principles — two ways of arriving at the same conclusion.

**Screenshots.** None — bounded probe, no scoring modal read.

**Verdict.** 041's idle-time finding was real and correctly measured, but
it isn't large enough to fund even the cheapest possible second tile.
**Multi-tile-per-drone is closed for Hay, with a sharper reason than
hay_single's**: hay_single had *no* idle time at all (001); Hay has real
idle time (041) but it's smaller than the unavoidable minimum overhead
(commute + own-handling) of servicing anything with it. This also means
039's ~441-tick, ~2.2-tiles-per-drone estimate for the leader is now in
real tension with the numbers measured tonight — if a second tile costs at
least 800 extra ticks to visit and Hay's own idle budget (492) can't cover
even that minimum, the leader's design is not "our champion plus a
second scheduled tile." Whatever they're doing is something else —
possibly related to 039's own caveat that the same-drone-count assumption
behind the 441 figure was never independently verified. That assumption,
not another companion-servicing or multi-tile variant, is the most
promising remaining thread.
