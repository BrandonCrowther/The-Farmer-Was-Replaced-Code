# exp-003 — measure Tree's harvest/reroll mechanics — result

**Outcome.** **Probe-only, no champion change.** Real, clean measurement
gathered via `simulate()`'s sandbox; a concrete redesign lead identified
but deliberately not attempted this session given one open question.

**Numbers.**

| check | result | note |
| --- | --- | --- |
| `plant(Entities.Tree)` over auto-grown Grass | succeeds | Grassland's natural Grass cover doesn't block `plant()` |
| `harvest()` on an unripe Tree | 0 wood, entity reverts to `Entities.Grass` | destructive, unlike Grass's own auto-regrow-as-itself |
| `own_tile_ready()` recovery after that | succeeds, replants Tree | the reroll idiom still works end-to-end, just via a costlier path |
| naive ticks/harvest model (001's 34,718-tick isolated growth + reroll churn) | ~37,000 predicted | vs. 002's real measured 9,551 — a ~3.9x gap, unresolved |

**Baseline.** 002 (current champion): 31:59.849, #89. Unaffected —
no code change made.

**Verdict.** Confirmed a real, Tree-specific mechanic difference from
Hay's Grass (destructive unripe-harvest, no auto-regrow exception) that
the current champion's code already handles correctly by accident (it
recovers), but the ~3.9x gap between the naive growth-time model and
the real measured average means at least one assumption is wrong —
most likely 001's 34,718-tick growth figure being an unwatered (water
≈0) measurement, mirroring Hay's own 019→037 correction. **Did not**
build or test a redesign tonight: the missing 069-style full-pre-seed
lever is real and well-motivated, but committing to a specific shape
(single-tile pre-seed only, vs. a multi-tile layout respecting Tree's
2.44x cardinal-neighbor growth penalty) needs the growth-time question
resolved first, per this project's own repeated lesson about not
designing around an unmeasured or wrongly-measured constant. Queued as
004 for a focused follow-up. `saves/wood_single/main.py` unchanged.
