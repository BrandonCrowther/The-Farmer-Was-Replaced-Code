# exp-082 — reorder the water-check AND for short-circuit benefit — result

**Outcome.** **Adopted, new champion.** 01:55.590, Global Rank #56 —
down from 081's 01:55.779/#57. A real -0.189s, +1 rank.

**Numbers.**

| run | metric | note |
| --- | --- | --- |
| single-drone correctness check (target = current inventory + 3,000,000) | clean termination, overshoot 43,328 | consistent magnitude with prior single-drone checks |
| real (target=2,000,000,000) | **01:55.590, #56** | `VERDICT=scored` |

**Baseline.** 081: 01:55.779, #57.

**Delta.** -0.189s (-0.16%), +1 global rank.

**Verdict.** Another pure-equivalence, code-proven-safe fix (same class
as 079's, boolean commutativity plus the game's confirmed short-circuit
`and`/`or` semantics) that clears the noise floor on a real run — this
time on the recurring per-iteration water-gating check rather than the
reroll chase or the target check. Champion's remaining hot-loop budget
is increasingly dominated by `reroll` itself (structurally floored at
069's p=1/3), `harvest()` (unavoidable, 200 ticks), and `move()`
(unavoidable, 200-201 ticks after 076) — the guard-check overhead class
that 079/081/082 have been finding is getting smaller each time, which
is the expected shape as the well runs dry. `saves/hay/main.py` updated
and merged to `main`. `record.json` and `queue.md` updated.
