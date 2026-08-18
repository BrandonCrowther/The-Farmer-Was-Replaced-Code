# exp-086 — shared-territory-two-phase-spawn — result

**Outcome.** **Rejected.** 01:55.553, Global Rank #52 — up from 085's
01:54.587, a real **+0.966s regression**, 14x the 0.069s noise floor
and unambiguous in one run (no re-run needed to trust a delta this
size, in either direction). PB/rank on the modal stayed at 085's
01:54.587/#52 — this run never came close to beating it.

**Numbers.**

| run | metric | note |
| --- | --- | --- |
| offline verification | `MISSING=0`, `bad_subset=0`, union=756 (exact match to today's real coverage) | re-derived against the exact deployed `OWNED_OFFSETS` table, not just the earlier scratch analysis |
| validation (target=200,000, `zzRunner.py` → `import main`) | 32/32 unique `SETUP_DONE` indices (0-31), 32/32 unique `HOTLOOP_START` indices (0-31), every `SETUP_DONE` line strictly before `PHASE1_DONE`, strictly before every `HOTLOOP_START` line | barrier holds exactly as designed — the 078 race is closed, confirmed structurally, not just by construction |
| real (target=2,000,000,000) | **01:55.553, #52** | `VERDICT=scored`, `WARN=944 Water` (routine) |

**Baseline.** 085: 01:54.587, #52.

**Delta.** +0.966s (+0.84%), worse. Rejected.

**Why it lost, despite the walk-count math being real (960→756,
21.3% fewer setup-phase candidate visits).** The validation trace
itself points at the mechanism, though this is read from a trace built
for correctness, not isolated for cost attribution, so it's stated as
an inference, not a clean measurement: per-drone `HOTLOOP_START` ticks
(local, counted from each drone's own spawn) ranged from 3294 to 7880
— more than 2x variance across drones that are all doing the same
shape of work (build `planted` from the near-check loop, one
`move_to_wrapped` call). The likely cause is structural, not
incidental: Phase 2 is a **second, independent** spawn-tree fan-out.
085's single-tree design only ever pays one "spawn near a common
origin, then walk out to my own base" cost per drone, for the whole
run. This design pays it **twice** — once during Phase 1's setup tree,
and again during Phase 2's fresh tree, whose drones are all newly
created (not the same physical drones that did Phase 1's work) and all
fan out from wherever Phase 1 left the root standing, near base 0's
territory. Some of the 32 bases (e.g. (28,28), (28,3)) sit up to half
the wrapped world apart from that common origin — a real, uncapped
per-drone walk cost that 085 never pays a second time, and that scales
with the *whole farm's* diameter, not with the ~1-4 saved candidate
positions per drone. 077 already measured a single spawn tree's own
critical-path overhead at ~443 ticks; doubling the number of trees
plausibly doubles that structural cost too, on top of the new walk-
back distance. Both effects push in the losing direction; this result
doesn't need to fully apportion them to explain why the net was
negative.

**What this confirms and what it doesn't.** Confirms 078's original
race-condition concern was the right thing to worry about, and that it
*can* be engineered around soundly (real barrier, verified live, zero
observed correctness issue). Does not confirm the underlying "shared
planting saves time" intuition — the walk-count reduction is real but
small and local (960→756, all short in-window moves), while the cost
of enforcing the barrier via a second spawn tree is a new, larger, and
farm-diameter-scaled cost that 085's single-tree design structurally
avoids. A version that partitioned territory *without* a second spawn
tree — e.g., threading ownership through the *existing* single tree
so each drone does its own owned-planting inline, in the same walk it
was already taking, with the barrier enforced by depth-ordering within
that one tree rather than by a second tree — might avoid this specific
regression, but that reintroduces real design complexity (a drone
would need to guarantee every *other* drone whose territory it
depends on has already run, not just its own descendants) and no
evidence yet that it would actually beat 085 by more than this
regression cost. Not pursued further tonight — the two-phase-spawn
shape specifically is closed; a same-tree variant is a genuinely
different design and would need its own hypothesis if picked up later.

**Verdict.** `saves/hay/main.py` stays on 085 (01:54.587, #52); no
merge. Game restored to 085 and reloaded, hashes verified matching
before and after this experiment. `record.json` and `queue.md`
updated; journal-only push per `docs/LOOP.md`'s "lost or inconclusive"
path (branch `auto_experiment/hay/086` carries the code, `main` gets
only `experiments/hay/086/`).
