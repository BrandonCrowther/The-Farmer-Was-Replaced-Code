# exp-001 — terminate the seeded achievement driver

**Hypothesis.** The seeded `saves/wood/main.py` (32 drones, one per
column, alternating y-offset, an interleaved Tree/Grass companion
pattern via `instructions()` + a reroll loop) just needs an endless
`while True:` replaced with a target check to terminate and score. This
design is NOT growth-pipelined (each drone fully waits for its current
tree via `Common.await_harvest()` before moving on, unlike
wood_single's reroll-before-walk champion) — real yield/tick behavior
is observed empirically here rather than fully hand-traced, given
time constraints and the risk of misreading pre-existing code.

**Variable.** Seeded `while True:` per-drone loop → target-gated on
`Items.Wood`.

**Metric.** The completion modal's verdict and displayed time —
this category's first-ever leaderboard entry. Given target
10,000,000,000 is huge and this design isn't pipelined, real run time
is uncertain — a smoke test at a small target measures real
ticks/harvest first to set expectations before committing.

**Baseline.** None — first attempt. World size 32, `max_drones()` 32
(probe-confirmed).

**Procedure.**
1. `saves/wood/main.py`: target-gate both per-drone and main loops,
   guard the water topup against depletion (same fix as sunflowers 001).
2. Smoke test at a small target first to measure real ticks/harvest and
   project the full run's real time before committing to it.
3. `tools/cycle.sh wood exp-wood-001-r1 --from <worktree>` for the real
   attempt if the projection looks tractable within the remaining
   session time.

**Falsifier.** If the smoke test's projected real time is too large to
fit the remaining session budget, say so and journal the finding
without forcing a long real run.
