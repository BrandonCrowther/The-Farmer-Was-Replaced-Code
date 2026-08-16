# exp-024 — lattice-wrapaware — result

**Outcome.** rejected — and the wrap hypothesis is dead too

**Numbers.**

| run | metric | note |
| --- | --- | --- |
| 021 lattice, plain `move_to` | 03:19.653 | |
| 024 lattice, `move_to_wrapped` | **03:19.655** | **2 ms apart** |

**Baseline.** 02:52.271 · **Variant.** 03:19.655 · **Delta.** +27.384 s (+15.9%)

**Verdict.** The wrap fix changed nothing — two milliseconds across two runs, well
inside a 0.15 s floor. So companion requests were never crossing the seam, and
the explanation offered in 023 for 021 and 022 was wrong.

**That is two wrong explanations for the same result.** First "contention is
cooperation", killed by 023's measurement of 0.13%. Then "wrapped walks", killed
by this run. Both were plausible, both fitted the number, and neither was true.

**What the pair does establish.** The 27-second penalty is *structural and
deterministic* — 021 and 024 agree to 2 ms, which is far tighter than the 0.287 s
spread of identical champion code in 002. Something about the lattice reliably
costs 16%, and it is not contention and not movement distance.

**Stop guessing.** 025 runs the same lattice with 023's arrival reporting plus
per-pass tick accounting, so the extra time can be located rather than
hypothesised. The candidates it will separate: more waiting (growth not covered),
more mismatched arrivals (more replanting), or more ticks in the walk itself.
