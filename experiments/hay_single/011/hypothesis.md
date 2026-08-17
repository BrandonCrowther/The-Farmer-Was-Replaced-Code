# exp-011 — champion-tick-profile

**Hypothesis.** The champion's real steady-state ticks/harvest (from a full
~1,221-harvest run, not a 200-cycle probe) is meaningfully higher than
009's 200-cycle tail estimate (≈829.5 ticks/harvest, ≈98.75 hay/tick) and
closer to what 010's real score implies (≈64.7 hay/tick average, ≈1,267
ticks/harvest) — because a full run visits many more distinct companion
positions than 200 cycles can establish, and each first-ever visit still
costs a full walk regardless of `REROLL_LIMIT`.

**Variable.** None — 010's exact champion logic, unchanged, with a
`quick_print` every 50 harvests (free, 0 ticks per Timing.md) added.

**Metric.** `PROFILE` lines' tick deltas between successive 50-harvest
checkpoints, across the run — gives a real per-harvest-batch rate at every
stage, not just a single tail-window estimate.

**Baseline.** 009: 200-cycle probe, ≈829.5 ticks/harvest tail estimate.
010: real score, ≈1,267 ticks/harvest average (81,920/64.7).

**Procedure.**
1. `saves/hay_single/main.py`: 010's logic plus the profile print.
2. `tools/cycle.sh hay_single exp-hay_single-011-r1 --from <worktree>` —
   background, real scored run (same as 008/010).
3. Read `OUTPUT=`; compute ticks/harvest between consecutive `PROFILE`
   checkpoints across the run, and see whether it keeps falling (still
   warming up even past 200 harvests) or plateaus.

**Falsifier.** If the profile plateaus near 009's 829.5 figure well before
harvest 1,221, the gap between 009's projection and 010's real score has a
different explanation (e.g. real op costs differ slightly from the assumed
1,600-tick walk, or the internal-repeat averaging in 010's score includes
some slower-than-typical repeats) and 012 should look there instead of at
"probe window too short."
