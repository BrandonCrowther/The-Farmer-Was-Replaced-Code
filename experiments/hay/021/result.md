# exp-021 — diamond-lattice — result

**Outcome.** rejected — and it inverts the assumption behind it

**Numbers.**

| run | seed | metric | note |
| --- | --- | --- | --- |
|  1  | random | **03:19.653** | +27.382 s vs champion. `SPAWNED 32 of 32` |

**Baseline.** 02:52.271 · **Variant.** 03:19.653 · **Delta.** **+27.382 s (+15.9%)**

**Noise floor.** 0.15 s. The regression is 183x the floor.

**Verdict. Contention was cooperation.**

The geometry did exactly what it was designed to do — 32 disjoint 25-tile
diamonds, no drone able to reach another's tiles — and the farm got 16% slower.
Overlap was not damage being tolerated; it was drones sharing companion
infrastructure without anyone intending it.

**Proposed mechanism (inference, not measurement).** When territories overlap, a
Bush or Tree planted by a neighbour is already standing on a tile when I arrive
with a matching request. 010's check then fires — `get_entity_type() ==
plant_type` — and the 400-tick harvest-and-replant is skipped entirely. The more
drones share a region, the more of it is pre-planted by somebody. Isolate the
drones and every companion has to be planted by its own drone from scratch.

**How to test that properly**, rather than believing this write-up: count arrivals
where the tile already holds the requested plant, under both layouts, with
`quick_print`. If the rate collapses under the lattice, the mechanism is
confirmed. That is the measurement this result deserves and did not get.

**What it also explains.** 015 marked contested tiles permanently untrusted and
lost 3.9 s. Read through this lens, 015 was not merely adding bookkeeping — it was
opting out of the same shared planting, refusing to trust exactly the tiles that
other drones were maintaining.

**And it complicates 013/014.** 013's map wins by skipping trips to tiles it
planted itself; 014 won slightly by *reducing* neighbour overlap. If overlap is
valuable, 014's small win needs re-examining — it may have been noise dressed as
a result, or the two effects may trade off at some optimum spacing that neither
5 nor 8 hits.
