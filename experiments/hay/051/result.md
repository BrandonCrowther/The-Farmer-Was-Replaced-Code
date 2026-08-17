# exp-051 — tighter packing (spacing 4, not 5) — result

**Outcome.** rejected, and in the opposite direction from hoped.

**Numbers.**

| run | metric | note |
| --- | --- | --- |
| r1 | `HITS_SKIP` 48/150 (32%), `HITS_WALK` 102/150 (68%) | skip rate *fell* vs 047's spacing-5 baseline (36.7%) |
| r1 | `TICKS_PER_HARVEST` 2,347.27 | vs 047's 1,390 baseline — a large regression |

**Baseline.** 047: spacing 5, 1,390 ticks/harvest, 36.7% skip rate.

**Variant.** Spacing 4. **Delta.** +68.9% ticks/harvest, skip rate
down 4.7 points. Both metrics moved the wrong way.

**Noise floor.** Not established — single 150-cycle sample.

**Screenshots.** None — probe.

**Verdict.** Denser packing does raise the overlap between drones'
companion-request footprints, but the effect is dominated by
**thrashing**, not cooperation: neighboring drones' independently-
random companion needs conflict more often than they happen to align,
so a shared position gets overwritten with the "wrong" thing more
often than it's found "already right." The champion's spacing-5 choice
is close to (or past) the point where tighter packing helps — closes
the tighter-packing family with a real, opposite-direction result.
