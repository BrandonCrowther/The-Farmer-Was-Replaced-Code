# exp-004 — overlap-arithmetic — result

**Outcome.** rejected as a route to *beating the leader*; adopted as a
genuine but bounded improvement over 002. No game cycle run — pure grid
geometry and probability, computed directly.

**Numbers.**

Ball overlap (radius-3, wrapped 8x8 grid, computed exactly):

| distance between tiles | overlap (of 24-cell ball) |
| --- | --- |
| 1 | 66.7% |
| 2 | 50.0% |
| 3 | 33.3% |
| 4 | 41.7% |
| 5 | 33.3% |
| 6 | 25.0% |
| 7-8 | 0% |

Close tiles share most of their companion zone — on this board, clustering
is cheap to arrange.

**The ceiling, derived not measured:** a fresh companion draw only matches
*already-stocked* ground truth if the type drawn equals the type standing
there. Carrot (1/3 of draws) never gets stocked at all (003) — permanent
miss. Of the remaining 2/3 (Bush/Tree), a position holds exactly one type at
a time, so a match needs the draw to agree with whichever of the two is
already there: **1/2**, regardless of how completely the position space is
covered. Overlap and clustering can only affect *how fast* coverage
approaches 100% (fewer distinct positions to learn, pooled across tiles) —
not the type-match ceiling itself.

- Best-case whole-run hit rate = `P(Bush/Tree) x P(covered=1) x P(type match) = (2/3) x 1 x (1/2) = 1/3` — a **hard ceiling of 33.3%**, essentially identical to 002's already-measured 27.6% second-half rate. There is very little headroom left to gain: 002 is already close to this ceiling without any clustering at all.
- At the ceiling: expected companion overhead per harvest ≈ `(1/3)(Carrot, ~0 extra) + (1/3)(Bush/Tree hit, ~0 extra) + (1/3)(Bush/Tree miss, ~1,200 real walk) ≈ 400` ticks. Own-tile floor ≈400. **Best-case total ≈800 ticks/harvest.**
- Budget from 001: **686 ticks/harvest.** Even the theoretical best case for this entire line of attack — perfect position memory, ideal clustering, zero extra overhead from tending multiple tiles — still lands **~17% over budget**, and that's before charging anything for the *extra* movement a real multi-tile layout would add between tiles (which 001 already flagged, and Hay's 027/029 measured as real and non-trivial in the same game).

**Baseline.** 002's measured design (~1,300 ticks/harvest, ~3x off pace).

**Noise floor.** N/A — arithmetic.

**Screenshots.** None — no game cycle run.

**Verdict.** Clustering is real and worth building — it could plausibly take
the measured ~1,300 ticks/harvest down toward the ~800-tick ceiling (roughly
a 35-40% speedup, cutting the gap from ~3x to perhaps ~1.6-1.7x) — but it
**cannot close the gap to the leader**, even under the most generous
assumptions, because the bottleneck was never position coverage, it's the
1-in-2 type-match probability at any position that's ever stocked at all,
and no amount of pre-planting changes that.

**This closes the fundamental-fork search.** Between 001 (schedulability),
002 (measured skip ceiling), 003 (Carrot/wood), and 004 (clustering
ceiling), every lever this category's mechanics expose has been priced or
measured, and all of them fall short of the leader's pace by a wide margin —
docs/LOOP.md's bar for stopping on an empty queue ("only stop when you have
genuinely run out of ideas, and then say what you tried and what you would
try next") is met. 005 should build the clustered design for real — it is
still the best achievable single-drone driver found so far, worth having as
a working, scored, terminating entry — but stop treating "beat 02:17.995" as
the target for this line of work. Report it as: best-effort design lands
around ~1.6-2x off the leader (versus ~3x for the naive single-tile version),
not a leaderboard win.
