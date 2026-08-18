# exp-083 — water threshold retune, and a closing scour pass — result

**Outcome.** **Closed, no code change.** One live measurement (the
water-threshold probe) and three analytical checks, all against the
current (082) champion; none found anything safe and worth a real run.

**1. Water threshold — measured, not adopted.** See `hypothesis.md`.
`WATER_CALLS 16/900`, `WAIT_TICKS 0` (growth still fully hidden), but
`MIN_WATER 0` — the tile's own water already touches its floor at the
current threshold. No slack to lower `WATER_THRESHOLD` further without
risking a real regression (turning 0 wait ticks into nonzero).

**2. Three-or-more tiles per drone — re-derived, still closed.** 070's
"one sibling's service time already exceeds growth floor, so 3+ tiles
give no gain" reasoning re-checked against current numbers: with 2
tiles, growth (415 ticks) is hidden behind a sibling visit (~850-900
ticks of real reroll+harvest+move work) with ~470-485 ticks of margin
already unused. The bottleneck is *servicing* cost per visit
(reroll+harvest+move), not growth-wait — a bottleneck a 3rd tile
doesn't touch, it only gives growth even more already-unused slack.
079/081/082's per-visit speedups don't change this shape, since they
reduce the *servicing* cost too, preserving the same margin structure.

**3. Beating the 1/3 reroll floor by mixing pre-seeded types — ruled
out algebraically.** Current design pre-seeds every reachable position
as Bush, so a reroll "hits" iff the drawn companion *type* is Bush
(1/3, since type is IID-uniform over Bush/Tree/Carrot — 040). Mixing
some positions to Tree or Carrot instead was worth checking: could it
raise the hit rate above 1/3? No — since position and type are drawn
independently and the pre-seed assignment is fixed *before* any draw,
`P(drawn type == that position's preset)` is exactly `1/3` for *any*
fixed assignment of one type per position, by the same logic that makes
a biased-in-advance guess no better than 1/3 against a fair 3-way IID
draw. All-Bush is already optimal among single-type-per-position
strategies, and no strategy of this shape can beat 1/3 — the floor
established in 069 is a real mathematical minimum, not an artifact of
which type was chosen.

**4. Dropping the `key in planted` check since NEAR_OFFSETS now covers
every reachable position — checked, unsafe.** Tempting since 080's
`NEAR_OFFSETS` is exactly the full companion-draw window, but the
bush-wall setup loop explicitly skips any position that's in
`ALL_CROPS` (a neighbor's or this drone's own crop tile) — so coverage
is `NEAR_OFFSETS` *minus* a handful of excluded positions, not total.
A companion draw can genuinely land on one of those excluded positions
(geometrically possible at 5-spacing with ±3/±4 windows), and treating
that as an automatic hit (skipping the `key in planted` check) would
silently claim the polyculture multiplier without it actually being
there — the exact shape of bug `docs/LOOP.md` already warns about.
Left unchanged.

**Verdict.** No further safe, code-provable, or cheaply-measured lever
found in this pass. Combined with 079/081/082's shrinking win sizes
(-0.798s, -0.313s, -0.189s) and this pass's four dead ends, the
stray-tick-scour line for the current two-tile-interleaving design
looks genuinely close to exhausted for tonight. Recorded in
`queue.md`/`record.json` as the closing note for this arc — see there
for the honest state-of-play summary and what a real next step would
require (a different macro-design, not another parameter inside this
one).
