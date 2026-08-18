# exp-085 — setup-phase tuple reuse for (px,py)

**Hypothesis.** Applying 084's exact lesson (a tuple rebuilt when an
identical one already exists) one loop up: the bush-wall setup builds
`(px, py)` as a fresh tuple literal for the `ALL_CROPS` membership
check, then builds it *again* for the `planted[(px, py)] = Entities.Bush`
write, for every position that survives the ALL_CROPS check and turns
out near. Build it once (`pos = (px, py)`) and reuse it for both.

**Variable.** Setup loop only: `pos = (px, py)` computed once, used for
both the `ALL_CROPS` check and the `planted` write (was two separate
tuple literals). No behavior change — `pos` is definitionally the same
value either way.

**Expectation going in.** Setup-phase only (paid once per drone, not
per-harvest) — 080's precedent (a much larger setup-phase change,
~27,000 ticks estimated) tied against the noise floor, so this smaller
one (~960 ticks estimated: 1 tick × ~30 positions × 32 drones) was
expected to likely be unmeasurable too. Tried anyway since it's free
and provably safe — the user's "micro optimizations still count as a
win" standing instruction.

**Correctness check.** Live validation (target = inventory + 200,000):
clean completion, no warnings, 3-line output. Same class of proof as
084 — no new game mechanic assumed, `pos` is provably the same value
the two separate tuple builds would have produced.

**Baseline.** 084 (`auto_experiment/hay/084`): 01:54.669, #53.
