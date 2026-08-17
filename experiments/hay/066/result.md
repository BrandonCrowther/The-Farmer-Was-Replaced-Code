# exp-066 — does harvest() auto-replant Grass? — result

**Outcome.** Falsified. Grass regrows on its own — `harvest()` never
leaves the tile empty, `get_companion()` rerolls every cycle with no
`plant()` call, and the champion's `instructions()` call costs **7
ticks, not 200**, because its guard (`if entity_type != Grass:
plant()`) never fires. The real own-handling cost is **~207 ticks per
cycle, not 400** — my prior explanation was wrong by roughly 2x.

**Numbers.** Round 1 (does it regrow at all):

```
JUST_AFTER_HARVEST entity Entities.Grass ground Grounds.Grassland
RESULT regrew True regrew_at_ticks 214 final_entity Entities.Grass ...
```

Round 2 (6 cycles, no `plant()` ever called again):

```
INITIAL_COMPANION (Entities.Tree,(31,30))
ITER 0 wait 591 et_before Entities.Grass harvest_ticks 200 et_after Entities.Grass companion (Entities.Tree,(30,0))
ITER 1 wait 407 et_before Entities.Grass harvest_ticks 200 et_after Entities.Grass companion (Entities.Tree,(2,0))
ITER 2 wait 409 et_before Entities.Grass harvest_ticks 200 et_after Entities.Grass companion (Entities.Bush,(31,0))
ITER 3 wait 407 et_before Entities.Grass harvest_ticks 200 et_after Entities.Grass companion (Entities.Tree,(29,0))
ITER 4 wait 409 et_before Entities.Grass harvest_ticks 200 et_after Entities.Grass companion (Entities.Tree,(1,31))
ITER 5 wait 407 et_before Entities.Grass harvest_ticks 200 et_after Entities.Grass companion (Entities.Bush,(0,3))
```

Round 3 (isolating the champion's actual post-harvest call):

```
ITER 0 harvest_ticks 200 instructions_ticks 7 entity_after Entities.Grass companion (Entities.Bush,(0,29))
ITER 1 harvest_ticks 200 instructions_ticks 7 entity_after Entities.Grass companion (Entities.Carrot,(30,1))
ITER 2 harvest_ticks 200 instructions_ticks 7 entity_after Entities.Grass companion (Entities.Carrot,(3,0))
ITER 3 harvest_ticks 200 instructions_ticks 7 entity_after Entities.Grass companion (Entities.Carrot,(1,31))
ITER 4 harvest_ticks 200 instructions_ticks 7 entity_after Entities.Grass companion (Entities.Bush,(30,1))
ITER 5 harvest_ticks 200 instructions_ticks 7 entity_after Entities.Grass companion (Entities.Carrot,(31,30))
```

`Grass.md` (the wiki mirror) says outright: **"Grass grows automatically
on grassland"** — a line that was sitting in the repo the whole time and
should have settled this without needing the experiment. Carrot's page
has no such line (till/plant/harvest is the real cycle there), so this
is specific to Grass, not universal.

**Verdict.** The champion's `instructions()` call after `harvest()` is
not a 200-tick replant — it's a ~7-tick no-op guard, because Grass never
actually leaves the tile. `get_companion()` still rerolls fresh on every
harvest (confirmed 6/6 cycles, different type/position each time), so
the reroll mechanic itself still works exactly as understood — it's
just far cheaper than modeled. Corrected own-handling cost: harvest
(200) + instructions (7) ≈ **207 ticks**, not 400. This directly
propagates into every number downstream that used R=400 as the reroll
cost: the servicing asymptote `S = R(1-p)/p` roughly halves (≈207×2≈414
instead of ≈800), and the "zero-servicing floor" (own-handling + growth)
drops from ~815 to **~622** (207 + 415). The #2-10 cluster's implied
~750-856 ticks/harvest, which looked like a tight, barely-reachable
target above our old floor, now sits comfortably *above* the corrected
floor with real room to spare.

This does **not** overturn the specific empirically-tested rejections
(051, 053-055, 058-061 — real measured game runs, not model
predictions, so the wrong cost model never touched their actual
results). What it does overturn is the *narrative* built on top of
them: "057 is at or near the true local optimum, the paradigm is
servicing-bound with an ~800-tick floor, further tuning is unlikely to
help" was reasoning from a wrong number. The reroll-before-walk design
space is not proven exhausted — it was evaluated against the wrong
budget. `experiments/hay/queue.md` and `record.json` need a correction
note, and the accept-policy family is worth a fresh look under the
right cost model before concluding the gap needs a structurally
different mechanism.
