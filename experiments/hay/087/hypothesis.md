# exp-087 — same-tree territory partition (no second spawn tree)

**Hypothesis.** 086 showed shared bush-wall planting is real (960→756
candidate visits, 204 redundant) but lost because enforcing the
ownership barrier needed a *second* spawn-tree fan-out, whose fresh
drones had to walk back from a common origin to their own base — a
farm-diameter-scaled cost 085's single-tree design never pays. If a
same-tree mechanism exists that lets a dependent drone safely trust a
neighbor-owned shared tile without a second fan-out, it could capture
some of 086's 21% redundant-visit saving without paying that walk-back
cost, and might beat 085.

**Variable.** The spawn-tree structure and/or per-drone ownership
logic in `saves/hay/main.py`'s `spawn_group()`/`driver()` — candidate
mechanisms explored below.

**Metric.** Real leaderboard time via `tools/cycle.sh`, same as every
other Hay experiment. (Not reached — see Outcome.)

**Baseline.** 085 (champion, merged): 01:54.587, Global Rank #52.

**Falsifier for each candidate mechanism**, checked *before* spending a
real run, per `docs/LOOP.md`'s "measure the mechanic before designing
around it": if the mechanism's own overhead (measured or soundly
modeled from measured constants) is not clearly smaller than the
redundant-visit savings it unlocks, don't build it — this is exactly
what closed 078 analytically, and this experiment applies the same
standard with fresh live-measured numbers instead of reasoning alone.

**Candidate mechanisms considered** (see `result.md` for the full
chain and the real numbers each one was checked against):
1. A shared global "setup done" flag array, polled instead of blocking.
2. Restructuring the spawn tree to follow physical adjacency (a
   spanning tree over the sharing graph), so every tree edge is a
   free, zero-wait "child trusts parent" relationship (parent's setup
   runs, in real program order, before it spawns that child).
3. The same "child trusts parent" idea applied *without* changing
   today's existing tree shape at all — only exploiting whichever of
   its 31 edges happen, by chance, to already be physically-adjacent
   pairs.
4. A dedicated short-lived "signal" drone per shared edge, whose only
   job is to plant the shared subset and return quickly, so a
   dependent can `has_finished()`-poll it non-blockingly instead of
   inserting a hard wait anywhere.

**Procedure.**
1. Re-run and extend the prior session's offline sharing-graph model
   (`placement_analysis.py`, `spanning_tree_v2.py` in scratch) to get
   real capture/depth/fanout numbers for candidates 2 and 3.
2. Probe the *real* game for the two load-bearing unknowns neither
   script nor prior sessions had hard numbers for: (a) the actual tick
   cost of the setup-phase candidate-window scan per drone, isolated
   from the spawn-in walk; (b) the actual critical-path spawn latency
   of a deeper/wider tree shape, using the same live methodology
   077/086 already established (`quick_print` + `get_tick_count()`,
   reduced-TARGET validation run, no real leaderboard cycle spent).
3. Check candidate 1 against `experiments/hay/050` (already measured:
   globals are drone-isolated, not shared) and candidate 4 against
   `max_drones()`'s documented cap before writing any driver code.
4. Only proceed to a real `tools/cycle.sh` run if a candidate survives
   all of the above with a clear (not razor-thin) margin.
