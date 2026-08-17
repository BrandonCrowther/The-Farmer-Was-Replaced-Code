# exp-002 — reroll-to-15 + 10-tile round robin validation — result

**Outcome.** adopted — the paradigm works essentially as predicted.

**Numbers.**

| run | metric | note |
| --- | --- | --- |
| r1 | 29/30 harvests `GAIN` exactly 8; 1/30 `GAIN` 7.79 | the 7.79 is real background Power-for-speed consumption (Sunflowers.md: 1 Power/30 actions while any Power is held), not a bug |
| r1 | `AVG_REROLLS` 6.17 (naive geometric-mean estimate was 9) | real empirical average, used directly rather than the model |
| r1 | `TICKS_PER_HARVEST` 4399.1, `TOTAL_GAIN` 239.17/30 harvests | with 10 tiles (mandatory minimum for bonus eligibility), comfortably above the idle-elimination threshold (growth ≈17,643 vs revisit interval 10×4399≈43,990) — no idle wait |

**Baseline.** 001: lone harvest, exact 8x on the one data point.
**Variant.** 30-harvest round robin, 96.7% exact-8x rate (the one
miss was a fractional background-consumption artifact, not a failed
bonus). **Delta.** Confirms the reroll-to-15 paradigm generalizes.

**Noise floor.** Not established — single 30-cycle sample.

**Screenshots.** None — probe.

**Verdict.** Adopting the design. Projected full run: net gain/harvest
≈7.97 (measured), target 10,000 → ≈1,255 harvests × 4,399.1 ticks/harvest
≈ 5,520,876 ticks ≈ **≈909s ≈ 15.2 minutes** for the first score. The
reroll cost (avg 6.17 attempts × 400 ≈ 2,468 ticks) is over half the
total — the clearest lever for a future optimization pass would be
tracking the dynamic current farm-wide max instead of always targeting
the hardcoded ceiling of 15, but that adds real bookkeeping complexity;
003 ships the simple, robust fixed-target-15 version first as the
real driver.
