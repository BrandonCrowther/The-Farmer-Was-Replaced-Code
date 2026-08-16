# exp-007 — farm-state-diagnostic — result

**Outcome.** diagnostic — assumptions confirmed, and the real bottleneck found

**What was measured.** 825 samples: the first 25 passes of each of 33 drones,
logging entity, ground, ripeness and companion face at the top of each pass.

**1. The tile always holds grass.** Every one of the 825 samples reads
`Entities.Grass` on `Grounds.Grassland`. Grass survives its own harvest, so
`get_companion()` always has a plant to answer for. **004 and 006 were fully
exercised and their conclusions stand.**

**2. Companion faces are uniform thirds.**

| face | count | share |
| --- | --- | --- |
| Tree | 293 | 35.5% |
| Carrot | 284 | 34.4% |
| Bush | 248 | 30.1% |

This retroactively confirms 004's reasoning: the Tree face really is about a
third of all companion visits, and every one of them was being satisfied with
grass — silently earning nothing — until 004 fixed it.

**3. The finding that matters: the drones are idle 94% of the time.**

| `can_harvest()` at top of pass | count | share |
| --- | --- | --- |
| False | 776 | **94.1%** |
| True | 49 | 5.9% |

A drone arrives to find its plant unripe on 19 passes out of 20, and then busy-
waits for it. **The bottleneck is growth time, not tick efficiency.**

**This invalidates the premise of most of the queue.** 006 rejected the reroll
because a harvest plus a plant "costs what the multiplier wins" — but ticks
spent while a drone would otherwise be standing still are nearly free. The same
applies to 008 (water) and 009 (harvest-before-till): they shave ticks off a
loop that is not tick-bound. They may still be worth running, but not for the
reason they were queued.

**The fork.** The farm is 32x32 = 1024 tiles worked by 36 drones, each standing
over exactly one of them. Roughly 96% of the field is empty while 36 drones wait
for one plant each.

The fix is to stop waiting: give every drone a **plot** and walk it in rotation,
harvesting whatever is ripe as it comes around. By the time the drone returns to
a tile, that tile has had the whole circuit to grow. Idle time goes to zero and
the field actually gets used.

Queued as 011 (rotation, no polyculture — isolating the idle-time hypothesis)
and 012 (rotation with polyculture restored).
