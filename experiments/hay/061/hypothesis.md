# exp-061 — accept cheap draws only late in the reroll sequence

**Hypothesis.** 060's hybrid accept (memory-hit OR distance-1, checked
on *every* attempt) tied the pure-memory champion (057) instead of
beating it as modeled — likely because accepting a paid ~900-tick
distance-1 walk on an *early* attempt forfeits the chance that one or
two more free rerolls (400 each) would have found a real memory hit,
an opportunity cost the original model missed. Restricting the
cheap-accept condition to only the *last two* reroll attempts
(`rerolls >= REROLL_LIMIT - 2`) preserves the early free-hit chances
while still avoiding the single most expensive outcome — exhausting
the full budget and falling back to whatever (possibly distance-3)
walk is left — by accepting a cheap-enough (distance<=2, not just
distance==1, since being pickier only matters this late) alternative
along the way if one appears.

**Variable.** 060's every-attempt (memory-hit OR distance==1) →
late-only (memory-hit always OR (`rerolls>=REROLL_LIMIT-2` AND
distance<=2)), `REROLL_LIMIT=5` unchanged.

**Metric.** The completion modal's displayed time and global rank,
compared to 057's 02:42.421 / #111 (current champion) and 060's
02:42.439 (tie, not adopted).

**Baseline.** 057: 02:42.421 (memory-only). 060: 02:42.439 (hybrid,
every-attempt, tied 057).

**Procedure.**
1. `saves/hay/main.py`: late-only cheap-accept condition, otherwise
   identical to 060 (wrapped setup movement kept).
2. Smoke test at a small target first.
3. `tools/cycle.sh hay exp-hay-061-r1 --from <worktree>` — real, full
   target-gated run.
4. Compare to 057 and 060.

**Falsifier.** If this also ties or loses to 057, the reroll-then-walk
paradigm's floor really is close to what 057 already achieves, and
further refinement of *when* to accept a cheap walk isn't the
remaining lever — look elsewhere for the gap to the cluster.
