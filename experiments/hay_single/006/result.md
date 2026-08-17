# exp-006 — clustered-v2-distance4 — result

**Outcome.** rejected (clustering, as a lever) — but two real findings came
out of it, one correcting 003.

**The collision fix worked.** `SELFGUARD 0` across all 90 cycles — distance
4 genuinely eliminates 005's bug, confirming the triangle-inequality
argument in 006's hypothesis.

**Finding 1 — 003 was wrong, or at least incomplete: wood is not
permanently zero.** `WOOD` ended at **573,952**, and Carrot starts showing
`AFFORD True` from cycle ~22 onward, with essentially every miss (any type)
satisfied from there on. The source: `Common.polyculture_mapped`-style logic
calls `harvest()` on a companion position before replanting it *whenever the
stocked type no longer matches the fresh request* — and by cycle ~20+, some
previously-planted Bush/Tree companions have had enough real time to mature.
Harvesting a **ripe** Bush/Tree for a type-mismatch replant yields real wood,
not nothing. 002's 60-cycle probe never ran long enough to see this — its
`WOOD` stayed 0 the whole time, and 003's arithmetic (correctly, for a
*fresh* farm with no standing mature companions) priced growing a *dedicated*
wood tile, not this incidental source. **Correction: given enough run
length, wood accumulates from ordinary companion churn and Carrot stops
being structurally dead** — 003's conclusion holds only for short runs / a
cold farm, not for the full ~1,221-harvest run this category actually needs.
This should be flagged wherever 003 is cited, not silently left standing.

**Finding 2 — the real cost of multi-tile is the commute, not the
companion-servicing math 004/005 focused on.** Despite most requests
(including Carrot, now) hitting the full 81,920 by the second half,
**average ticks/harvest is ≈2,286 — worse than 002's single-tile ≈1,469**,
and overall throughput is *lower* (196,201 hay/s vs 002's 238,428 hay/s)
despite collecting more total hay. Two tiles at wrapped distance 4 cost
~4 moves (~800 ticks) just to shuttle between them *every single cycle* —
a tax neither 001 nor 004's arithmetic priced in, because both treated
"movement" as only the companion-servicing trip, not the base cost of
tending more than one physically separate tile. This tax is paid on
*every* cycle, hit or miss, so it isn't something a better hit rate can buy
back.

**Numbers.** 90 cycles, 6,644,224 hay, 205,747 ticks, 33.87s. `HITS` 15/90
(16.7% raw — noisy, includes the warm-up window), `SAT` 66, `UNAFFORD` 9 (all
early), `SELFGUARD` 0, `CARROT_SEEN` 36 (40%, higher than the expected ~1/3 —
small-sample noise, not a mechanism change).

**Baseline.** 002 (~1,469 ticks/harvest, single tile).

**Noise floor.** Not established.

**Screenshots.** None — probe.

**Verdict.** Clustering is rejected for a third, cleaner reason now: even
free of 005's bug and with companion-servicing working as designed, the
**inter-tile commute cost exceeds anything clustering buys back.** Multi-tile
is closed for real this time — three independent reasons across
001/005/006 (no idle time to hide behind, self-collision risk at useful
overlap distances, and a flat commute tax at safe distances) all point the
same way. **007 should go back to 002's single-tile design and run it
longer** — long enough to see whether *it* also accumulates wood and starts
satisfying Carrot without ever paying a commute tax, since nothing in 002's
design precludes the same maturing-companion mechanism found here. That is
now the more promising open question than anything multi-tile.
