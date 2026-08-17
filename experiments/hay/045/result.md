# exp-045 — unlock-level-check — result

**Outcome.** rejected (the hypothesis that Grass yield isn't already
maxed) — a clean, valuable negative result that closes a real gap in prior
verification, not a re-derivation of something already known.

**Numbers.**

| unlock | level | max (from Unlocks-Data.md array length) | next cost |
| --- | --- | --- | --- |
| `Unlocks.Grass` | 10 | 10 | `{}` (nothing more to buy) |
| `Unlocks.Polyculture` | 5 | 5 | `{}` |
| `Unlocks.Watering` | 9 | 9 | `{}` |

All three at max. `get_cost` returning `{}` confirms there's no further
upgrade available at all, not just an unaffordable one.

**Baseline.** Assumed max per Simulation.md's semantics — now independently
confirmed, not just assumed.

**Noise floor.** N/A — direct reads.

**Screenshots.** None — probe.

**Verdict.** `Unlocks.Grass` ("increases the yield of grass") is real and
was never checked in this project's history, but it is already fully
captured in the measured 512-base / 81,920-satisfied figures used all
night — there is no unrealized yield lever here. This closes the one
genuinely unexamined assumption underlying every yield number computed
tonight (hay_single and Hay alike). Combined with 040 (draw is IID),
043 (tick rate is constant), and 044 (idle window too small for a second
tile), **every mechanism this project can directly inspect via the API has
now been checked and confirmed as expected.** The leader's ~3x edge on Hay
remains unexplained by anything discoverable this way. The most likely
remaining candidates are either (a) 039's same-drone-count assumption
behind the ~441-tick estimate, which cannot be verified without knowing
the leader's actual code, or (b) a structurally different approach (e.g.
layout/spacing retested with tonight's understanding, or something outside
the polyculture-servicing model entirely) that hasn't been tried.
