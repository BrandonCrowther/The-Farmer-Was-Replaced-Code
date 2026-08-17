# exp-012 — reroll-limit-5 — result

**Outcome.** **adopted — new champion.**

**Note on this cycle.** The first attempt hit the game's known memory-leak
crash ("Fatal error in GC", docs/LOOP.md) mid-deploy. `tools/tfwr.sh
relaunch` recovered cleanly and the re-run scored normally — one failure in
the consecutive-failure count, not a stop condition, exactly as documented.

**Numbers.** Modal: **03:57.198**, `VERDICT=scored`, **global rank #169**
(up from #182), PB 03:57.198. Leader unchanged, 02:17.995 (#1).

30 internal repeats in `output.txt`: `TIME_FINAL` range 230.35s-249.99s,
mean ≈237.2s ≈ 03:57.2 — matches the displayed time. `TICK_FINAL` range
1,399,366-1,518,699. Implied hay/tick ≈ 65.8-71.5 (e.g.
100,023,808/1,409,612 = 70.95) — **beats 011's model prediction for K=5
(66.33)**, the same direction 010 beat its own K=2 prediction (62.13 model
vs ≈64.7 real).

**Baseline.** 010 (champion before this): 04:13.399, rank #182, ≈64.7
hay/tick. 011's model for K=5: ≈66.33 hay/tick.

**Delta.** **−16.2s (−6.4%)** vs. 010; rank #182 → #169. Real throughput
≈68.7 hay/tick average (100,019,700-ish/1,441,150-ish across repeats) —
beating both 010's real number and 011's model. Gap to the leader:
`237.198 / 137.995 ≈ 1.719x` (from 010's 1.836x).

**Noise floor.** Not established for real scored runs (each is a
30-repeat average). The pattern of real runs consistently beating the exact
model (010 and 012 both) suggests the model's `W=1,600` walk-cost constant
is a slight overestimate of the real average walk cost, not that anything
is wrong with the reroll mechanism itself.

**Screenshots.** `logs/captures/20260816-221812-exp-hay_single-012-r1.png`.

**Verdict.** Adopt as champion. 011's diminishing-returns table (K=5→7 only
+1.06 modeled hay/tick) plus this run beating its own model prediction
suggests K=5 is a reasonable stopping point for this specific knob — pushing
to K=7 would very likely land in the 68-72 hay/tick range already achieved
here, not clearly higher. `REROLL_LIMIT` tuning is treated as done; 013
should look at the fundamental-fork question (per docs/LOOP.md's own bar for
an empty queue) rather than sweep K further for shrinking returns.
