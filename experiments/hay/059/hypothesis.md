# exp-059 — REROLL_LIMIT=3 (between the champion's 2 and 057's 5)

**Hypothesis.** 058 showed `REROLL_LIMIT=10` is worse than 057's 5 —
the reroll-cost/hit-rate tradeoff peaks somewhere at or below 5, not
above it. Testing 3 (between the champion's original Carrot-only 2 and
057's full-reroll 5) narrows down whether 5 is itself already past the
peak, or the peak is close to 5 from below.

**Variable.** 057's `REROLL_LIMIT=5` → `REROLL_LIMIT=3`. Everything
else identical (full memory-matched reroll, water 0.999, spacing-5
layout).

**Metric.** The completion modal's displayed time and global rank,
compared to 057's 02:42.421 / #111 and 058's 02:55.859.

**Baseline.** 057: `REROLL_LIMIT=5`, 02:42.421 (current champion). 058:
`REROLL_LIMIT=10`, 02:55.859 (rejected, worse).

**Procedure.**
1. `saves/hay/main.py`: `REROLL_LIMIT=3`, otherwise identical to 057.
2. Smoke test at a small target first.
3. `tools/cycle.sh hay exp-hay-059-r1 --from <worktree>` — real, full
   target-gated run.
4. Compare to 057 and 058.

**Falsifier.** If 3 is also worse than 5, the peak is at (or very near)
5 specifically and this parameter is settled — stop tuning it further
and look elsewhere for the remaining gap to the cluster.
