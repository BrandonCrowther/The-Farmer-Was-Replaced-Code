# exp-078 — shared bush-wall planting / territory partitioning

**Hypothesis (as queued in 077).** Every drone walks and checks all ~30
of its reachable companion positions even when a neighbor already
planted a shared one — the redundant *plant* is skipped (the
`get_entity_type() != Bush` guard), but not the redundant *walk-to-
check*. Partitioning tile ownership across neighbors (each shared tile
visited by exactly one owning drone) would cut the remaining setup-phase
walk cost, mirroring 076/077's setup-phase wins.

**Analysis before writing any code** (docs/LOOP.md's "measure/reason
before designing around it" rule, applied to a mechanism that's already
been directly measured rather than assumed): a genuine walk-skipping
partition needs a non-owning drone to trust that a *different* drone
has already planted a shared tile, without itself visiting to check.
That trust has to come from somewhere, and there are only two
candidates, both already closed by evidence from this investigation:

1. **A cross-drone read of the world state, cheaply.** No API exists
   for it. `get_entity_type()` only reads the *current* tile position —
   there is no "peek at a distant tile" builtin (checked against
   `docs/api/`). The only way to observe a tile's true state is to walk
   to it, which is the exact cost being avoided.
2. **Trusting a deterministic ownership rule *without* observing the
   tile.** This needs either (a) accepting the tile might not be Bush
   yet when trusted, or (b) a guarantee that the owner always plants
   first. (a) is a real correctness bug, not a performance trade — see
   below. (b) needs synchronization between unrelated drones, which
   does not exist: 050 already confirmed drones share **no** mutable
   state, and the wiki/API's only cross-drone primitive is `wait_for()`
   on a drone's own direct spawn handle — a drone cannot wait on a
   sibling or cousin it did not itself spawn. 077's own spawn tree
   makes this *worse*, not better: setup order across the 32 drones is
   now genuinely concurrent and unordered (043 already confirmed tick
   rate — and by extension execution — is identical/parallel regardless
   of drone count; nothing serializes one drone's setup before
   another's).

**Why option (a) is a correctness bug, not a speed/quality trade-off.**
If drone B skips visiting a neighbor-owned tile and just marks it
`planted[key] = Bush` on trust, and B's hot loop later draws a companion
request for that exact tile *before* the owning drone has actually
gotten around to planting it (entirely possible — no ordering guarantee,
see above), B's reroll-chase sees the memory "hit," `break`s out
believing the request is satisfied, and takes the harvest *without* the
polyculture multiplier the code thinks it earned. `harvest()` and
`get_companion()` return no error for this — it is a legal action that
silently loses yield, exactly the shape of the polyculture bug
`docs/LOOP.md` already warns about (`p_planting_table` reused for the
wrong question). This would not show up in a validation pass the way
076/077's arrival/position checks did, because the bug is a silent
*value* loss on a shared global counter (`num_items(Items.Hay)`), not a
crash, a hang, or a wrong position — it would only surface as an
unexplained shortfall in a real scored run, exactly the kind of thing
this project's retrospective in `docs/LOOP.md` (the "rule can exist and
still get missed" section) warns is easy to build on top of without
noticing.

**Why the "safe" version (skip the plant, still do the walk) doesn't
help.** That's already what the champion does — the `get_entity_type()
!= Bush` guard already skips the redundant *plant*. The walk itself is
unavoidable if the check has to stay honest, per point 1 above.

**Precedent that a coverage-reducing shortcut here would likely lose
anyway, even if it were race-free.** 069 tested exactly this trade-off
for the *hot loop*: partial pre-seeding (only 20/24 positions,
`069v1`) measured barely better than no pre-seeding at all (1069.57 vs
068's ~1070-1220) because the un-seeded positions needed real walks
often enough to eat the savings, while full pre-seeding (`069v2`, all
24) was clearly better (1068.35) — *more* coverage won, not less. A
territory partition is a coverage reduction of the same shape (some
positions no longer get proactively serviced by every drone that might
need them), applied one level up (setup instead of hot-loop), and
069's finding is the closer available evidence on which way that trade
goes.

**Status: REJECTED — analytical closure, no live run.** The available
"safe" version does not exist as described (would still require the
same walk it's trying to remove), and the only way to actually skip
the walk introduces a real, silent correctness bug given how spawn
order works after 077. Not spending a real 2B-hay scored run to
confirm a mechanism-level dead end that's already derivable from 043,
050, and 069's own measured results, and the API's documented absence
of any cross-drone read/sync primitive beyond `wait_for()` on a direct
child. If a future session finds a genuine way to make ownership
provably ordered (e.g. restructuring the spawn tree so a drone only
starts its OWN bush-wall setup after `wait_for`-ing the specific
sibling that owns any tile it depends on), this could be revisited —
but that reintroduces exactly the sequential-latency cost 077 just
removed, so the net win is unclear even in principle.
