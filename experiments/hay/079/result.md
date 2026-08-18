# exp-079 — stray-tick scour — result

**Outcome.** **Adopted, new champion.** 01:56.092, Global Rank #58 —
down from 077's 01:56.890/#59. A real -0.798s, +1 rank.

**Numbers.**

| run | metric | note |
| --- | --- | --- |
| single-drone smoke test (900 cycles, hot loop only, measured after setup) | 884.06 ticks/harvest (windows 849-910) | noisier than the ~1.3-tick/harvest predicted effect of the reroll fix alone — see verdict; this smoke test could not resolve the change either way |
| validation (target=200,000, `zzRunner.py` → `import main`, `MY_POS` per drone) | 32/32 unique positions, clean, no warnings | confirms the wdist short-circuit didn't change which positions get walked/planted |
| real (target=2,000,000,000) | **01:56.092, #58** | `VERDICT=scored` |

**Baseline.** 077: 01:56.890, #59.

**Delta.** -0.798s (-0.68%), +1 global rank.

**Verdict.** Three mechanical fixes, each provable safe by reading the
code rather than by measurement (unlike 078's rejected idea, none of
these assume anything about game mechanics beyond documented language
rules): (1) reroll chase compared `planted[key]` (a second tuple-keyed
dict lookup) against `ctype`, when `planted` has exactly one write site
in the whole file and it's always `Entities.Bush` — replaced with a
direct constant comparison, the one change here that touches the
~871-harvest/drone hot loop rather than one-time setup; (2) bush-wall
setup computed both `wdist()` calls (~11 ticks each) before checking
either against the threshold, when `or` already short-circuits —
reordered to compute the second only when needed; (3) bush-wall setup
called `get_entity_type()` twice with nothing in between that could
change its answer — cached in a local. The single-drone smoke test
couldn't detect these (predicted hot-loop effect ~1.3 ticks/harvest
from fix (1) alone, versus ~60-tick window-to-window noise in this
particular 900-cycle sample — a real instance of "small-sample probes
undersample" from this session's own priors), but the *real* run shows
a clear win close in size to 077's, likely dominated by the two
setup-phase fixes ((2) and (3)) which the hot-loop-only smoke test
never measures at all (same blind spot 076/077 had — setup gains are
invisible to this smoke-test methodology by construction). Confirms the
queue's framing: there was still real, if small, stray-tick overhead
left after 075/076/077, findable by reading the code rather than
inventing new macro-structure — matches the user's steer that Hay's
remaining headroom now looks like exactly this shape. `saves/hay/main.py`
updated and merged to `main`. `record.json` and `queue.md` updated.
