# exp-058 — higher REROLL_LIMIT (10, not 5)

**Hypothesis.** 057 confirmed memory-matched reroll-before-walk is a
real, positive win over the full run (`REROLL_LIMIT=5`: 02:47.682 →
02:42.421). The mature per-draw hit rate (~1/3, matching the physical
skip-rate baseline) compounds favorably with more attempts —
`1-(2/3)^(k+1)` — and each attempt is cheap (400 ticks, no growth
penalty since it happens immediately at plant time) relative to a real
walk (~1,300+ ticks). Raising `REROLL_LIMIT` to 10 should capture more
of that compounding without materially changing the worst-case cost
(the fallback walk still happens exactly once per cycle, just after
more attempts).

**Variable.** 057's `REROLL_LIMIT=5` → `REROLL_LIMIT=10`. Everything
else (water 0.999, full memory-matched reroll, spacing-5 layout)
unchanged.

**Metric.** The completion modal's displayed time and global rank,
compared to 057's real 02:42.421 / #111.

**Baseline.** 057: 02:42.421, #111 (real full run, adopted champion).

**Procedure.**
1. `saves/hay/main.py`: `REROLL_LIMIT=10`, otherwise identical to 057.
2. Smoke test at a small target first (bounded, catch bugs cheaply).
3. `tools/cycle.sh hay exp-hay-058-r1 --from <worktree>` — real, full
   target-gated run (a bounded probe would be misleading per 049 vs
   057's lesson).
4. Read `SHOT=` with vision for time/rank; compare to 057.

**Falsifier.** If this is worse than 057, the reroll-cost/hit-rate
tradeoff has already crossed its optimum somewhere between 5 and 10 —
report the real number and don't keep raising the limit blindly.
