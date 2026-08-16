# exp-036 — preference-stability — result

**Outcome.** diagnostic — 013 is safe, 035 is explained, and **033's headline
claim is false**.

## What was measured

Run scored **02:52.418** against the 02:52.32 champion baseline — inside the
noise the probe was designed not to disturb, since `quick_print` costs 0 ticks.

Two `get_companion()` calls bracketing `Common.polyculture_mapped(planted)` —
roughly 800 ticks of movement, and on many passes a harvest and a replant on the
companion tile. Only the main drone reports; a leaderboard run repeats the
program ~20 times, so these are ~20 independent executions, not one lucky plant.

| result | count | share |
| --- | --- | --- |
| same type **and** same position | 16,800 | **100.0%** |
| type changed | 0 | 0% |
| position changed | 0 | 0% |
| companion was None | 0 | 0% |

**`get_companion()` is deterministic for a standing plant.** The preference is a
property of the plant instance, not of the call.

## The contradiction, and how it resolves

033 concluded the opposite — "non-deterministic per call" — from 5,485 reroll
attempts that changed the preference 66.4% of the time. Both measurements are
sound. They disagree only about *what* rerolls it.

The type distribution at this probe point is the independent tiebreaker:

| companion | count | share |
| --- | --- | --- |
| Bush | 8,099 | 48.2% |
| Tree | 8,054 | 47.9% |
| Carrot | 647 | **3.85%** |

Carrot is a third of fresh rolls. Here it is 3.85%, and (1/3)³ = 3.70% is what two
rerolls at 2/3 success each would leave. `REROLL_LIMIT` is 2. **The reroll works,
and it works by actually replanting** — this distribution cannot be produced any
other way.

So: the reroll changes the preference (033, confirmed here twice over), *and*
querying does not (this experiment). The two are only in conflict under 033's
extra claim that the reroll "works without replanting anything", which it
inferred from `mid_entity` reading `Entities.Grass` on every attempt. That
inference is the part that is wrong; what `mid_entity` actually proves is
untested, and 038 tests it.

## Consequences

- **013 stands.** Its 18.5 s map win skips a walk on the strength of an earlier
  observation. With the preference stable for the plant underfoot, that
  observation cannot go stale mid-pass. The doubt raised when 035 was journalled
  is retired.
- **035 is explained, and the explanation I wrote for it was wrong.** 035 called
  `get_companion()` repeatedly hoping for a different answer at 1 tick a throw.
  The answer never changes without a replant, so the loop always ran to its cap
  and then walked anyway — pure added cost, which is the +12.5 s. My write-up
  blamed a stale preference forfeiting the multiplier; the real fault is that the
  reroll mechanism it was built on does not exist. Corrected in 035's file.
- **A cheap reroll is not available.** Rerolling costs a 200-tick plant, not a
  1-tick query. Any future design that assumed otherwise is void.

## Method note

Three write-ups in a row (032, 033, 035) got the measurement right and the
explanation wrong, each time by reasoning about a mechanic instead of testing it.
What broke the deadlock here was not a better argument — it was a distribution I
could compute two ways and check against itself. That is the shape to aim for: a
number that is over-determined, so a wrong story about it fails visibly.
