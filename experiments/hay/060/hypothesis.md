# exp-060 — hybrid accept policy (memory-hit OR distance-1) + wrapped setup movement

**Hypothesis.** Clean tick-budget model: total ticks/harvest = 400
(own handling) + max(S, 415) where S is servicing cost. Solving the
reroll-only recurrence with steady-state per-draw hit probability
p≈1/3: `S = R(1-p)/p = 400×2 = 800` — *above* the 415 growth floor, so
growth is never actually the binding constraint for the pure-
memory-only reroll paradigm (057-059), no matter how the cap is
tuned. Raising the *effective* accept probability by also accepting
cheap real walks (distance-1, ≈900 ticks total but immediate,
guaranteed) instead of always rerolling should lower the asymptotic S.
Solving the same recurrence with the wider accept condition
(P(free)=1/3, P(cheap-paid)=1/9, P(reroll)=5/9) gives S≈737, a real
improvement over the pure-memory asymptote's ≈800-816.

Separately: `Common.move_to()` (unwrapped) is used for the initial
32-drone setup walk from the spawn point (0,0) to each drone's home.
Switching to `Common.move_to_wrapped()` cuts the worst-case single-
drone setup distance from 56 (unwrapped, corner (28,28)) to 28
(wrapped) — a real, essentially free micro-optimization, though setup
is a small fraction of the ~987,000-tick full run.

**Variable.** 057's memory-only accept condition → accept on
(memory-hit OR wrapped-distance==1), `REROLL_LIMIT=5` unchanged.
Setup movement: `Common.move_to` → `Common.move_to_wrapped`.

**Metric.** The completion modal's displayed time and global rank,
compared to 057's real 02:42.421 / #111 (current champion).

**Baseline.** 057: 02:42.421 (memory-only accept). 058/059: worse at
`REROLL_LIMIT` 10/3 (memory-only accept, confirms 5 is the right cap
*for that policy* — this experiment changes the *policy*, not just the
cap, so re-tests `REROLL_LIMIT=5` under the new accept rule).

**Procedure.**
1. `saves/hay/main.py`: accept condition widened to include
   wrapped-distance-1 draws (computed via `get_world_size()`, matching
   053/054's `wdist` helper); setup uses `move_to_wrapped`.
2. Smoke test at a small target first.
3. `tools/cycle.sh hay exp-hay-060-r1 --from <worktree>` — real, full
   target-gated run.
4. Compare to 057.

**Falsifier.** If this doesn't beat 057, either the real per-draw
distance-1 walk cost is higher than modeled (the ~900-tick estimate
may undersell till()/contention overhead), or the accept-probability
math is off somewhere — report the real number and reconsider the
model rather than re-tuning blindly.
