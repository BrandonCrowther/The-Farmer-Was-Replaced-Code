# exp-002 — reactive-companion-probe

**Hypothesis.** A solo drone's own-memory skip rate (companion tile already
correct, from this drone's own history, no travel needed) settles near the
1/3 structural ceiling implied by IID (type, position) draws over a fixed
memory — not Hay's 44-66%, which is boosted by neighbour drones incidentally
pre-stocking each other's tiles (021). Carrot is permanently unaffordable
(512 wood, and nothing in this design ever produces wood), capping the
multiplier-eligible fraction at Bush+Tree only, ≤2/3 of requests.

**Variable.** None being varied — reactive skip-then-satisfy-then-remember,
run for a fixed 60 cycles, fully instrumented.

**Metric.** Hit rate (`HITS / CYCLES`), satisfied-vs-unaffordable split on
misses, and the yield delta on a satisfied harvest (to confirm or correct
001's assumed 81,920). All from `quick_print` lines in `output.txt`.

**Baseline.** 001's arithmetic: needs ~686 ticks/harvest average against a
~400 tick own-tile floor, i.e. ~282 ticks of companion-servicing slack, which
implied a needed skip rate ≥~75% if a real companion trip costs ~800-1,600
ticks.

**Procedure.**
1. `saves/hay_single/main.py`: 60 harvest cycles, skip on own-memory hit,
   else check affordability, else travel+plant and remember.
2. `tools/cycle.sh hay_single exp-hay_single-002-r1 --from <worktree>`.
3. Read `OUTPUT=` — compute hit rate, confirm/correct the 81,920 figure from
   a `GAINED` value on a `HIT True` cycle, and check `WOOD` stays 0 and
   `CARROT_SEEN` misses are all `AFFORD False`.

**Falsifier.** If the measured hit rate is well above 1/3, the IID-uniform
assumption is wrong (positions or types are not drawn uniformly) and the
whole skip-rate ceiling argument in 001/queue.md needs redoing from the real
distribution, not the assumed one. If any Carrot request is satisfied, the
zero-wood assumption is wrong and Carrot re-enters the design.
