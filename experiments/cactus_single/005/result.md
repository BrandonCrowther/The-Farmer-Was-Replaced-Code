# exp-005 — insertion-sort validation (4x4) — result

**Outcome.** adopted — validated cleanly, first try.

**Numbers.**

| run | metric | note |
| --- | --- | --- |
| r1 | `GAINED` 8192 (exact `32*16**2` match), `SORT_TICKS` 20,059 | vs 003's bubble sort 34,852 for the same 4x4 grid |

**Baseline.** 003: 4x4 bubble sort, `SORT_TICKS` 34,852.
**Variant.** 4x4 insertion sort, `SORT_TICKS` 20,059. **Delta.** **-42.4%**
sort ticks, same exact cascade yield.

**Noise floor.** Not applicable — an exact formula match isn't noise.

**Screenshots.** None — probe.

**Verdict.** Insertion sort (single forward walk, backward-correct on
each inversion) is a real, substantial win over bubble sort's full
re-walk-per-pass approach, exactly as the O(n+inversions) vs O(n²)
reasoning predicted. 006 takes this straight to the real 8x8 scored
run (design is proven correct twice now — 003's bubble sort and this
insertion sort both hit the exact formula value).
