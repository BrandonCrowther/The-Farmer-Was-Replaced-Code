# exp-081 — drop the move()-guarding redundant target check

**Hypothesis.** `driver()`'s hot loop checks `num_items(Items.Hay) >=
TARGET` three separate times per iteration: the outer `while`'s own
condition, once before `harvest()`/the reroll chase, and once more
before the final `move()`. Each `if...break` costs ~3 ticks (if-entry +
getter + compare) and runs unconditionally every iteration regardless
of how far from TARGET the run actually is — ~2600 ticks/drone
recurring over ~871 harvests, real cost across the whole run, unlike
076/077/080's one-time setup costs. The third check (guarding only the
cheap `move()` call) is the lowest-value of the three to keep: removing
it risks, at most, one extra 200-tick move per straggler drone in the
single iteration where the shared target is actually reached by another
drone mid-reroll-chase — bounded, one-time, and only possible at all in
the run's very last iteration. The second check (guarding the much more
expensive harvest+reroll chase) stays, since overshooting *that* is a
worse trade.

**Variable.** Remove the `if num_items(Items.Hay) >= TARGET: break`
check between the reroll chase and the final `move()` call. The check
before `harvest()`/the reroll chase is unchanged.

**Correctness risk, and how it's covered.** Unlike 079/080's changes,
this one is *not* pure algebraic equivalence — it's a real (bounded)
behavioral difference in the run's endgame. Validated live before the
real run: (a) single-drone, target set to current inventory + 3,000,000
(the real leaderboard target is unusable for this check since the
persistent save's Hay inventory is already ~53.8 billion, far above
2,000,000,000 — `num_items(Items.Hay) < TARGET` would be false from the
very first check and the hot loop would never execute at all) — result:
clean termination, overshoot 45,376 (well under one satisfied-harvest's
81,920 yield, and fully attributable to the *other*, still-present
check's granularity, not this change). (b) Full 32-drone run, target =
current + 30,000,000: clean completion, all 32 drones finished
(`VALIDATE_DONE` reached), overshoot 94,848 — small, bounded, no hang,
no runaway.

**Metric.** Real leaderboard time/rank — this is a hot-loop change,
recurring per-harvest, so (unlike 076/077/080) it should in principle be
visible to a single-drone smoke test too, but the real run is the actual
arbiter given the endgame-behavior risk it carries.

**Baseline.** 079 (`auto_experiment/hay/079`): 01:56.092, #58.
