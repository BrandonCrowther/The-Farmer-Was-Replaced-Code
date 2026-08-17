# exp-058 — higher REROLL_LIMIT (10, not 5) — result

**Outcome.** rejected — worse than 057's `REROLL_LIMIT=5`, real full
run.

**Numbers.**

| run | metric | note |
| --- | --- | --- |
| r1 | Time 02:55.859, Global Rank #111 (unchanged, PB stays 02:42.421) | modal, `VERDICT=scored`; run did not beat the existing PB |

**Baseline.** 057: `REROLL_LIMIT=5`, real full run, 02:42.421.

**Variant.** `REROLL_LIMIT=10`. **Delta.** +8.3% wall time — a real
regression, not noise (13.4s on a ~163s baseline).

**Noise floor.** Single real run each side — not independently
repeated, but the direction and size are consistent with a genuine
cost-curve effect, not measurement noise.

**Screenshots.** `logs/captures/20260817-091404-exp-hay-058-r1.png`

**Verdict.** `REROLL_LIMIT=5` was already near (or past) the local
optimum, not under-tuned as hypothesized — raising it further adds
more worst-case reroll cost (paid on every cycle that doesn't hit
early) than it recovers in additional hit-rate. The `1-(2/3)^(k+1)`
compounding intuition undersold how much the *tail* attempts cost on
the cycles that never hit at all. Not adopted; champion stays 057.
Next: try a value *below* 5 (the curve may peak somewhere between 2
and 5, not necessarily at 5 exactly) before concluding this parameter
is settled.
