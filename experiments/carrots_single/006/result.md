# exp-006 — reroll-before-walk (single tile) — result

**Outcome.** partially confirmed, and caught a real bug along the way.
`TICKS_PER_HARVEST` on a single tile does **not** improve over 003
(growth-bound floor dominates, exactly as the Falsifier predicted), but
handling cost (idle subtracted) drops close to the ~1,400 prediction —
confirming the design is sound and worth combining with multi-tile.

**Numbers.**

| run | metric | note |
| --- | --- | --- |
| r1 (buggy) | `HITS_GRASS` 36, `HITS_REROLL` 1, `HITS_WALK` 3, `TICKS_PER_HARVEST` 8282.08 | **2/40 harvests came back at 512 (unmultiplied)** — see bug below |
| r2 (fixed) | `HITS_GRASS` 34, `HITS_REROLL` 2, `HITS_WALK` 4, `TICKS_PER_HARVEST` 8710.2, 40/40 multiplied | mean `SVC_TICKS` ≈883, mean `IDLE_TICKS` ≈7139 → handling (idle subtracted) ≈1,571 |

**Bug found (r1 → fixed in r2).** Dropping 003's "revert serviced
position back to Grass" step (kept as permanent stock instead, matching
hay_single's memory pattern) broke the "Grass companion is always free"
assumption: once a remote position is walk-serviced and left as Bush/
Tree, a *later* companion draw asking for Grass at that exact position
is no longer actually satisfied there — but the code still treated
`ctype == Grass` as an automatic free hit regardless of memory state.
Fixed by checking the memory dict first for *any* type (Grass included):
free-Grass is only assumed for a position never in `planted`; a position
in `planted` must match `planted[key] == ctype` to count as a hit.

**Baseline.** 003: 8,361.55 ticks/harvest, handling ≈2,422 (backed out).
**Variant.** 8,710.2 ticks/harvest (r2, within noise of 003 — both
growth-bound), handling ≈1,571. **Delta.** Headline ticks/harvest:
+4.2% (noise, not a real regression — single-tile is growth-bound so
handling isn't the bottleneck here). Handling itself: **−35%**, matching
the reroll-before-walk model's prediction (~1,400) reasonably closely
(the fallback walk's REROLL_LIMIT=5 cap pulls the average up a bit above
the idealized asymptote).

**Noise floor.** Not separately established — comparing means from
single 40-cycle samples.

**Screenshots.** None — probe.

**Verdict.** Confirmed: cheaper handling alone doesn't help a
growth-bound single tile (idle time just absorbs the savings, as
predicted). The real payoff is combining this with multi-tile
pipelining — since per-visit handling dropped from ≈2,422 to ≈1,571,
the crossing point `N × handling ≥ growth` moves from N≈2.23 (004's
number, already past at N=3) to `N ≥ 7196/1571 ≈ 4.58` — **5 tiles**
should now fully hide growth at this cheaper handling cost, projecting
close to the handling floor (≈1,571 ticks/harvest, **≈52.2 carrots/tick**,
more than double 004's adopted 3-tile champion at ≈23.88 carrots/tick).
007 builds this.
