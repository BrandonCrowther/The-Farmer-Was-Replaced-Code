# exp-001 — mechanics-probe — result

**Outcome.** measurement, and a major discovery — see 002 for direct
confirmation.

**Numbers.**

| quantity | value |
| --- | --- |
| world / max_drones | 8 / 1 (matches hay_single) |
| starting stockpile | **1,000,000,000 Hay, 1,000,000,000 Wood** — no bootstrapping problem, ever; ~625k total needed for ~1,221 Carrot plantings is negligible against this |
| `COST_CARROT` | `{Hay:512, Wood:512}` — matches Hay's figure exactly |
| Bush/Tree/Grass cost | free — matches |
| move/till/plant | 200/201/202 (small print-overhead, same pattern as hay_single 001) |
| `GROUND_AFTER_TILL` | `Grounds.Soil` — confirmed |
| growth ticks (5 samples) | 7,680 / 5,718 / 6,290 / 8,296 / 7,995 — mean **≈7,196**, matching Plant-growth.md's Carrot range (4.8-7.2s at water 0, scaled 5x at water~1 → 0.96-1.44s → 5,827-8,741 ticks at the measured ~6,070 ticks/s rate) almost exactly |
| companion distances (wrapped) | 2, 3, 3, 3, 2 — all ≤3, confirms the same range rule |
| companion types seen | Bush, Grass, Tree, Grass, Grass — **never Carrot** (confirms "never itself") |
| **yield: Grass-companion cycles** | **81,920 — multiplied, 3/3 times, despite never planting anything there** |
| yield: Bush/Tree-companion cycles | 512 — bare, 2/2 times, as expected (never serviced) |

**Baseline.** hay_single 001 (404-tick growth, same tick rate, same
companion range).

**Noise floor.** Not established (n=5), but the 3/3-vs-0/2 split on
Grass-vs-other companion satisfaction is too clean to be coincidence — see
002 for direct confirmation, not just this inference.

**Screenshots.** None — probe.

**Verdict.** Growth is ~17.8x slower than Grass's (7,196 vs 404 ticks) —
this category is very plausibly growth-bound, not servicing-bound, the
opposite of hay_single. The starting stockpile removes any economic
bootstrapping concern entirely — Carrot can be planted (and re-planted, for
rerolling) as freely as Grass was in hay_single, resource-wise. And every
Grass-type companion request was satisfied without any action — see 002
for the direct check.
