# exp-083 — water threshold retune (probe-only, no code change)

**Hypothesis.** `WATER_THRESHOLD=0.75` was tuned in 072, before 079,
081, 082 collectively reduced the hot loop's per-iteration overhead —
maybe the growth-timing margin that made 0.75 safe has room to lower
further now, cutting the number of `use_item()` calls (200 ticks each)
below the ~16/871 072 measured.

**Measurement first** (071/072's own methodology — instrument before
guessing): single-drone probe, 900 cycles, current champion code
unmodified, measuring `WATER_CALLS` (actual `use_item()` count),
`WAIT_TICKS` (real idle time spent polling `can_harvest()` while unripe
— should be ~0 if growth is still fully hidden), and the tile's own
water level (`get_water()`) at the start of every cycle, min and
average.

**Result.** `WATER_CALLS 16 of 900` (matches 072's figure almost
exactly). `WAIT_TICKS 0 avg 0` (growth still fully hidden, confirms no
regression from 079/081/082's speedups). **`MIN_WATER 0`** — the tile's
own water level hits exactly 0 at least once in this 900-cycle sample,
`AVG_WATER 0.88`.

**Verdict: closed, no code change, no real run.** The premise was
wrong. 072's "headroom" was about *growth-completion timing* relative
to the away-window (~518 ticks needed inside a ~900-tick window), not
about unused water-conservation slack — and this probe shows the
*water* side is already touching its own floor (0) at the current
threshold, even though that hasn't yet caused real idle wait. Lowering
`WATER_THRESHOLD` further would make hitting 0 more frequent, eating
into a margin that's already gone on the water axis specifically —
real risk of turning `WAIT_TICKS` from 0 into something nonzero (an
actual regression, not just a missed optimization) for an unclear and
likely small payoff (some fraction of 16 calls × 200 ticks ≈ 3200
ticks/drone at best, already a small target). Not worth a real 2B-hay
scored run to find out — the probe answered the question directly, at
zero cost, per `docs/LOOP.md`'s own repeated lesson (`quick_print`/
`get_tick_count()` cost 0 ticks, a probe that doesn't score is still a
good cycle).
