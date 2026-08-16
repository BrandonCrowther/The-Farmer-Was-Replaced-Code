# exp-002 — baseline

**Hypothesis.** The terminating seed's time is stable enough to serve as the
number every later Hay variant is compared against, and the Hay noise floor is
much smaller than `fastest_reset`'s ~10.7 minutes.

**Variable.** Nothing. Byte-identical code to `auto_experiment/hay/001`, run
three times. Only the leaderboard's own random seed differs.

**Metric.** Mean of the completion modal's time over 3 runs, plus the spread,
which is the floor any later claimed improvement has to clear.

**Baseline.** `auto_experiment/hay/001` at 83f9042 — a single run of 04:55.393.

**Procedure.** Per run: `tfwr.sh reload` (canonical window stacking), `run`,
`wait-result`, `capture`, archive `output.txt`, `dismiss`.
