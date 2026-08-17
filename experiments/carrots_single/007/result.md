# exp-007 — 5-tile reroll pipeline — result

**Outcome.** adopted, after fixing a real bug that inverted the result.

**Numbers.**

| run | metric | note |
| --- | --- | --- |
| r1 (buggy) | `TICKS_PER_HARVEST` 6960.35, `HITS_GUARD` 0/75 | **worse** than 004's 3-tile champion |
| r2 (fixed) | `TICKS_PER_HARVEST` 2370.29, `HITS_GUARD` 0/75, `COMMUTE_AND_WAIT_TICKS` ≈1052 nearly every cycle | idle effectively eliminated |

**Bug found (r1 → fixed in r2).** r1 checked/rerolled the companion at
the *start* of the visit, after the crop had already been growing
untouched for a full round-robin lap (~7,000+ ticks). A reroll miss at
that point threw away all of that accumulated growth (harvest+replant
resets growth) instead of costing ~400 ticks — the opposite of 006's
timing, where the reroll happens *immediately* after planting, before
any growth accrues. Fixed by moving the reroll/walk resolution to
directly after `own_tile_ready()`, in the same visit, before moving to
the next tile — so growth only ever starts once the companion is
already settled, exactly mirroring 006's single-tile timing. r1's
number wasn't just noisy, it was structurally wrong: multi-tile
pipelining only pays off if the expensive part (growth) starts *after*
the cheap resolution step, not before it.

**Baseline.** 004: 3-tile walk-always, 3,430.43 ticks/harvest.
**Variant (r2).** 2,370.29 ticks/harvest. **Delta.** **−30.9%,
1.45x throughput over the current champion.** ≈42.2 carrots/tick.

Matches the model closely: predicted floor was in-place handling
(≈1,571, from 006) + mandatory round-robin commute at this 5-tile
spacing (≈800) ≈ 2,371 — measured 2,370.29, an almost exact match. The
5-tile spacing fully absorbs growth: `COMMUTE_AND_WAIT_TICKS` sits at a
near-constant ≈1052 across nearly every sampled cycle (commute + a
little water-application overhead), meaning real wait-for-ripe idle is
close to zero — the crossing point computed in 006 (`N ≥ 7196/1571 ≈
4.58` → 5 tiles) held.

**Caveat.** Cycles 0-4 (the first visit to each tile) came back
unmultiplied (512, not 81,920) — the initial per-tile setup loop plants
each tile directly without running the reroll/walk resolution, so the
very first companion draw per tile is never actually serviced. A
one-time warm-up cost (5 harvests out of ~1,221 in a full run,
negligible), but the real driver (008) should run the same resolution
logic during setup so it isn't wasted even once.

**Noise floor.** Not separately established — single 75-cycle sample
per variant.

**Screenshots.** None — probe.

**Verdict.** Adopting this design. 008 builds the real terminating
driver: 5-tile round-robin, reroll-before-walk resolved immediately at
plant time (including during initial setup, fixing the warm-up gap),
projecting `1,221 × 2,370.29 ≈ 2,894,244` ticks → **≈477s ≈ 7:57** for
the full target, down from 005's real 11:54.303.
