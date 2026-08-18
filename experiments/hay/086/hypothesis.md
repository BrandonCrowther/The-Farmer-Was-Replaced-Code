# exp-086 — shared-territory-two-phase-spawn

**Hypothesis.** Splitting setup into two full, sequentially-joined
binary spawn trees — a setup-only tree in which each of the 32 drones
plants only its own partitioned ~2/3-3/4 share of the bush wall (a
hardcoded, offline-verified `OWNED_OFFSETS` ownership table, zero
runtime computation), fully joined before a second, fresh spawn tree
starts anyone's hot loop — cuts real setup-phase walk/plant cost
(204 of 960 total per-drone candidate visits, 21.3%, are today's
pairwise-redundant double-planting) without the correctness bug 078
rejected the same underlying idea over. 078's bug was a race: a
drone's hot loop could ask for a companion on a neighbor-owned tile
before that neighbor had actually planted it. This design closes that
race structurally — Phase 2 cannot start for *any* drone until Phase
1's own spawn tree has fully joined for *all* 32 drones (root's
`wait_for` loop transitively depends on the whole tree), so every
owned position is guaranteed Bush before any hot loop can possibly
read it.

**Variable.** `saves/hay/main.py`'s setup structure: one spawn tree
doing full per-drone setup+hotloop (085's champion) → two spawn trees,
`setup_group`/`setup_only` (owned-offsets-only planting) followed by
`hotloop_group`/`driver` (hot loop only, `planted` built from the full
candidate window same as before, but never walked to verify).

**Metric.** Real leaderboard time (target 2,000,000,000 hay), read from
the completion modal via `tools/cycle.sh`.

**Baseline.** 085 (commit on `main`, merged): 01:54.587, Global Rank
#52.

**Correctness risk and how it's closed (the actual crux of this
experiment, per 078's rejection).** Verified offline (script in the
session's scratch notes, re-run directly against the deployed file's
`OWNED_OFFSETS` table): every one of the 960 total per-drone candidate-
window visits across all 32 drones resolves to a position Phase 1 will
have planted (`MISSING = 0`); every `OWNED_OFFSETS[idx]` entry is a
real candidate of its own base (`bad_subset = 0`); the union of all
owned positions is exactly 756 — the same total unique bush-wall
coverage today's champion already achieves, confirming nothing is
dropped, not just nothing double-owned.

**Predicted effect.** Setup-phase walk/plant count drops from 960
total candidate visits to 756 (a ~21% reduction in setup-phase
`move_to_wrapped`/`get_entity_type`/`plant_companion` calls, spread
unevenly — interior drones' setup calls drop by ~1/4, edge drones
less). Expect a small, real, one-time-per-repeat win in the same size
class as 076 (a setup-phase-only cost, paid again every ~2h-simulated
repeat the score averages over), offset partially by Phase 2's fresh
spawn tree adding one more full binary-spawn-tree critical-path
latency (~443 ticks, per 077's own measurement) that 085's single-tree
design didn't pay. Net direction not yet certain from reasoning alone
— genuinely an empirical question, which is why this gets a live run
rather than another analytical closure like 078.

**Falsifier.** If the real run's delta is not clearly outside the
0.069s noise floor in the *predicted* direction (faster), or if
validation surfaces any missing/mis-owned tile, a crash, or evidence
that Phase 2 started before Phase 1 fully joined for someone, the
change is rejected regardless of the offline verification above — a
clean offline check is necessary, not sufficient, per `docs/LOOP.md`'s
"a conclusion needs a test that is not a full run" but also "the real
run is still what decides it" once the offline check has already ruled
out the known failure mode.

**Procedure.**
1. Offline verification (done, see above) — re-derive `OWNED_OFFSETS`
   against the exact deployed file and confirm zero missing positions,
   zero invalid subset offsets, correct union size.
2. Deploy to live, reduced-target validation (`import main` trick,
   target lowered to something achievable in seconds) — confirm no
   crash/hang, `PHASE1_DONE` prints before any hot-loop activity, and
   ideally a per-drone marker confirming Phase 2 only starts after.
3. `tools/cycle.sh hay exp-hay-086-r1 --from <worktree>` for the real,
   full-target run. Re-run once if the delta is within ~2x the floor.
4. Journal the result either way; merge only if it beats 085 by more
   than the floor.
