# exp-032 — reroll-for-map-hit — result

**Outcome.** rejected — and it exposes a flaw in a merged result

**Numbers.** 03:15.214 vs 02:52.32 · **+22.894 s (+13.3%)**

**Verdict, and the part that matters.** Writing this up surfaced that the reroll
cannot do what both this experiment and **020** claim it does.

The loop is:

```
harvest()          # the multiplied harvest — tile now empty
instructions()     # plant grass: roll #1
companion = get_companion()
while <not what we want>:
        harvest()          # tile holds fresh, UNRIPE grass
        instructions()     # entity is already Grass -> plants nothing
        companion = get_companion()   # same plant, same preference
```

`harvest()` fails on an unripe plant, so the tile still holds the grass planted a
moment ago. `instructions()` then sees `get_entity_type() == Entities.Grass` and
does nothing. The preference is a property of that plant, so `get_companion()`
returns the same answer every time. **The loop spins to its cap and rerolls
nothing.**

Which means:

- This experiment could never have worked as designed.
- **020's `REROLL_LIMIT` beyond 1 has never done anything**, and 020 is a merged
  champion win of 12.4 s at 5 sd. Its measured improvement is real — the run
  happened — but the mechanism written in its result file is not the mechanism
  that produced it. The likeliest actual cause is the single `instructions()`
  call after the harvest, which replants immediately instead of leaving the tile
  empty until the next pass, changing when growth starts.

**Not guessing further.** 033 probes the reroll directly: print the companion
before and after each attempt, plus the entity, and count how many attempts ever
change the preference. If the answer is zero, 020's result file needs correcting
and the reroll should be replaced by the plain replant it actually is.


---

**CORRECTED BY 033.** The claim above — that the loop "spins to its cap and
rerolls nothing", and that 020's win is therefore mis-attributed — is **false**.

033 measured 5,485 reroll attempts: the preference changed on 66.4% of them,
exactly the 2/3 expected from a fresh uniform roll. It changes even though the
tile is untouched (`mid_entity` is Grass throughout, the harvest fails on the
unripe plant and `instructions()` plants nothing), because **`get_companion()` is
non-deterministic per call**.

020 stands as written. 032 lost because it demanded a match on type *and*
position, which is far rarer than "not Carrot" — not because rerolling is broken.
