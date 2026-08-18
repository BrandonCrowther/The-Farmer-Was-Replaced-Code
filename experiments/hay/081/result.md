# exp-081 — drop the move()-guarding redundant target check — result

**Outcome.** **Adopted, new champion.** 01:55.779, Global Rank #57 —
down from 079's 01:56.092/#58. A real -0.313s, +1 rank.

**Numbers.**

| run | metric | note |
| --- | --- | --- |
| single-drone correctness check (target = current inventory + 3,000,000) | clean termination, overshoot 45,376 | well under one satisfied harvest (81,920); consistent with the *other*, still-present check's granularity, not a new problem |
| 32-drone correctness check (target = current inventory + 30,000,000) | clean completion, all 32 finished, overshoot 94,848 | small, bounded, no hang |
| real (target=2,000,000,000) | **01:55.779, #57** | `VERDICT=scored` |

**Baseline.** 079: 01:56.092, #58.

**Delta.** -0.313s (-0.27%), +1 global rank.

**Verdict.** Confirms the theory: unlike 080's setup-phase relocation
(which tied, undetectable against the noise floor), this change touches
the hot loop directly — ~2600 ticks/drone recurring over ~871 harvests
— and the real run shows a clear, floor-clearing win, closer in size to
079's than to 080's. The asymmetric choice (drop the check guarding the
cheap `move()`, keep the one guarding the expensive harvest+reroll
chase) paid off without any observed correctness cost in either
validation pass. `saves/hay/main.py` updated and merged to `main`.
`record.json` and `queue.md` updated. The second, more expensive target
check (before harvest()/the reroll chase) is intentionally NOT touched
here — removing that one trades a much larger overshoot risk for a
similar per-iteration saving, a worse trade than this one; if revisited,
it needs its own careful measurement, not reuse of this experiment's
reasoning.
