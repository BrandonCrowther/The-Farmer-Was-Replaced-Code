# exp-033 — probe-the-reroll

**Not an optimisation.** 032 argued the reroll loop cannot work — `harvest()`
fails on an unripe plant, `instructions()` then plants nothing, so
`get_companion()` should return the same preference forever. If true, 020's
`REROLL_LIMIT` has never done anything and a merged champion win is mis-explained.
Print the preference before and after every attempt, and the entity in between.
