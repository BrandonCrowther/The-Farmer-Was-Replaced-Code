# exp-077 — spawn-tree parallelization (move_to_wrapped's sibling: spawn_drone)

**Hypothesis.** 076 fixed the setup phase's *walk*; this is the setup
phase's *spawn*. The champion's spawn loop has one drone (the eventual
main/root) call `spawn_drone()` 31 times in a row before it starts
farming its own tile — every one of those calls is sequential on the
same drone's own instruction stream, so the 31st drone doesn't start
farming until the root has paid for all 31 calls. Per the "repeat until
2h simulated, average the runs" scoring rule (076's same point), this
setup latency is paid again every repeat, not amortized away.

**Measured first** (probe, `experiments/hay/077/result.md` has the raw
numbers): a single isolated `spawn_drone()` call costs exactly 200
ticks (matches Operation-Costs.md's generic "successful operating
function" row — nothing entity-specific here, unlike Hay's own
Grass-auto-regrow exception). The real 31-call sequential loop (with its
own `for`/`if`/append overhead) costs 6745 ticks total, 217.58
ticks/call average — close to the ~6200 estimate in 076's notes.

**Design.** A binary spawn tree. `spawn_group(positions)` is handed a
list of base tiles; it keeps `positions[0]` as its own farming tile,
splits the rest in half, and spawns at most 2 new drones — one per half
— each of which repeats the same pattern before farming. Depth is
`ceil(log2(32))=5`, so no drone in the tree pays more than 2 sequential
`spawn_drone()` calls per level it sits at before it starts farming
(≤10 calls total on the worst path), instead of up to 31 on the old
single-drone chain. Every level's drones spawn their own children truly
concurrently with each other — 043 already confirmed tick rate is
identical regardless of drone count, i.e. drones genuinely run in
parallel rather than being time-sliced against one another, so a
shallower tree really does mean less *wall-clock* latency, not just
less work attributed to one drone's own counter.

**Variable.** Replace the 073-era flat spawn loop (31 sequential
`spawn_drone(driver, x, y)` calls from one drone) with the tree above.
`driver()` itself (the actual farming logic, 076's champion) is
unchanged.

**Correctness risk, and how it's covered.** The flagged risk from 076's
review was exactly this: "needs its own correctness validation — every
position covered exactly once, no gaps, no double-spawn." Validated
live before the real run (target=200,000, `zzRunner.py` swapped for a
bare `import main`, every drone — root and every `spawn_group` call —
prints its own `(bx,by)` and local `get_tick_count()`): 32/32 `MY_POS`
lines, 32/32 unique positions, set matches the expected 32-tile grid
exactly (checked independently in Python), `SPAWNED_ROOT_CHILDREN 2`,
clean `VALIDATE_DONE`, no warnings, no hang. Max local tick at any
child's `MY_POS` print: 443 (vs the old design's up to 6745 for the
last-spawned drone) — confirms the fan-out actually shortens the
critical path, not just redistributes the same total work.

**Falsifier.** If the real run's global rank/time doesn't improve (or
regresses) despite the validation passing clean, the setup-latency
theory itself would be in question — the tick-rate-independence finding
(043) that this design leans on would need re-checking, since that's
the one load-bearing assumption the validation pass can't test (it
only confirms correctness, not real wall-clock timing, since
`get_tick_count()` reads are per-drone-local, not a shared global
clock — confirmed by this pass, since children showed *lower* absolute
tick values than the root despite being spawned strictly later).
