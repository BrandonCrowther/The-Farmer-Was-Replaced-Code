# exp-002 — natural-grass-growth-check

**Hypothesis.** Grass.md's "Grass grows automatically on grassland"
applies to any untouched grassland tile on the board over real time, not
just ones the drone interacts with — explaining 001's 3/3 free Grass-type
companion satisfactions.

**Variable.** None — direct before/after observation of one untouched
tile's entity type.

**Metric.** `get_entity_type()` at a distant tile (5,5), sampled once near
the start and again after several real seconds of unrelated work — with
the drone never having planted anything there.

**Baseline.** 001's indirect evidence: 3/3 Grass companion requests
multiplied without ever being serviced; 0/2 Bush/Tree requests were.

**Procedure.**
1. `saves/carrots_single/main.py`: check tile (5,5), do ~6 unrelated
   carrot cycles at home (~6+ real seconds, matching 001's timescale),
   check (5,5) again.
2. `tools/cycle.sh carrots_single exp-carrots_single-002-r1 --from <worktree>`.
3. Read `OUTPUT=`; compare the two `ENTITY` readings.

**Falsifier.** If `(5,5)`'s entity type is still `None`/unchanged on the
second check, 001's pattern was coincidence (or explained by something
else — e.g., maybe the specific positions named in 001 happened to be ones
the *drone's own carrot-growing cycle* incidentally touched) and needs a
different explanation before designing around it.
