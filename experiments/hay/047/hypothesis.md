# exp-047 — pinpoint the walk-servicing tick blowup

**Hypothesis.** 046 found "walk" servicing costs wildly inflated —
many samples in the 12,000-26,000 tick range, 10-15x the ~800-2,000
expected for a distance-≤3 round trip (till+harvest+plant+move). 046
also found the champion's own long-standing "water is 10x short"
comment is wrong: real water sits at 0.8-1.0 throughout, not
near-zero. Splitting the walk into move-out / service / move-back
should reveal whether the blowup is movement (repeated failed `move()`
calls, 1 tick each, likely from cross-drone contention on a shared
32x32 world with 32 concurrently-moving drones) or something in the
till/harvest/plant sequence itself.

**Variable.** None — a finer-grained measurement pass on the same
champion logic.

**Metric.** Per walk cycle: `MOVE_OUT_TICKS`, `SVC_ACTION_TICKS`,
`MOVE_BACK_TICKS`, plus companion distance (wrapped Manhattan) for
context.

**Baseline.** 046: `SVC_TICKS` for "walk" outcomes ranged 876-26,252,
highly bimodal-looking (some ~800-1,700, many ~12,000-26,000).

**Procedure.**
1. `saves/hay/main.py`: same 32-drone real-contention setup, main
   drone instrumented to split `move_to(px,py)`, the
   till/harvest/plant service, and `move_to(ax,ay)` into separate
   timed segments.
2. `tools/cycle.sh hay exp-hay-047-r1 --from <worktree>`.
3. Read `OUTPUT=`; identify which segment(s) account for the blowup.

**Falsifier.** If no segment shows an outsized cost, the blowup may be
noise from real-time drone scheduling/contention rather than a fixed
per-call cost — say so and reconsider before assuming a fix exists.
