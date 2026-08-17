# exp-008 — finish-and-score

**Hypothesis.** 007's single-tile design, given the real `Items.Hay >=
100,000,000` termination condition instead of a fixed cycle count, actually
terminates and scores — hay_single's first real leaderboard time — landing
somewhere near 007's ≈05:30 projection (the projection didn't account for
warm-up drag or a second sample, so treat it as an estimate, not a
prediction to hit exactly).

**Variable.** 007's probe (fixed 200 cycles, never reaches target) → a real
driver (loops on `num_items(Items.Hay) < TARGET`, terminates on hitting it).

**Metric.** The completion modal's verdict (`scored`, not `failed`) and its
displayed time, read with vision from the `SHOT=` screenshot — this is a
real run, not a probe, so (unlike 001-007) the modal's number is the thing
being measured.

**Baseline.** 007's projection: ≈330s (≈05:30) at ≈49.9 hay/tick steady
state. No prior score exists for this category to compare against — this
*is* the baseline, once it exists.

**Procedure.**
1. `saves/hay_single/main.py`: real driver, target-gated `while` loop, same
   servicing logic as 007.
2. `tools/cycle.sh hay_single exp-hay_single-008-r1 --from <worktree>` — run
   in the background; per Leaderboard.md a scored run repeats internally
   until 2 real hours of simulated time accumulate, so wall-clock duration
   for the modal to appear is unknown in advance and may be much longer than
   001-007's near-instant probes.
3. Read `SHOT=` with vision for the time, PB and rank. Read `OUTPUT=` for
   the `DONE` line's `TICK_FINAL`/`TIME_FINAL` (single-run figures, not the
   2-hour-averaged score).

**Falsifier.** If the run fails to terminate (times out, or the modal shows
"Run Failed") rather than scoring, the driver has a correctness bug that
007's fixed-cycle-count probe couldn't have surfaced (007 never ran the
target-gated exit path), and that bug — not pace — is what 009 has to fix
first.
