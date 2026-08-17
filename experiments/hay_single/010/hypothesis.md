# exp-010 — finish-and-score-v2

**Hypothesis.** 009's reroll-before-walk logic, built into a real
terminating driver, scores near its ≈02:47 projection and becomes the new
champion, roughly halving the ~2.1x gap to the leader down to ~1.2x.

**Variable.** 008's champion (walk on every miss) → reroll up to 2 times
first, then walk (009's exact logic), with the real `Items.Hay >=
100,000,000` termination condition instead of a fixed cycle count.

**Metric.** The completion modal's verdict and displayed time, read with
vision — same as 008. `OUTPUT=`'s `DONE` line for the raw
tick/time/wood figures across the internal repeats.

**Baseline.** 008: real scored champion, 04:49.565, rank #302, ≈55.8
hay/tick. 009: probe projection, ≈98.75 hay/tick steady state, ≈02:47.

**Procedure.**
1. `saves/hay_single/main.py`: 009's reroll-then-walk logic wrapped in
   008's target-gated `while` loop.
2. `tools/cycle.sh hay_single exp-hay_single-010-r1 --from <worktree>` — run
   in the background, same as 008 (game repeats internally to 2 simulated
   hours before showing a result).
3. Read `SHOT=` with vision for the time, PB and rank; compare to 008's
   04:49.565 and 009's ≈02:47 projection.

**Falsifier.** If the modal shows "Run Failed" rather than scoring, the
reroll logic has a correctness bug 009's probe didn't surface (009 never
exercised the real target-gated exit path, same caveat as 008/007). If it
scores but lands far from ≈02:47 (say, worse than 008), the probe's 200-cycle
sample wasn't representative of the full ~1,221-harvest run and 011 should
say why before trying to tune further.
