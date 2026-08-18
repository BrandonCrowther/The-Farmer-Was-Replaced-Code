# exp-092 — water-tank contention at launch

**Hypothesis.** User's second observation from watching the champion
at 0.1x speed: "a lot of unfulfilled water requests at launch." The
shared water-tank pool (`num_items(Items.Water)`) regenerates slowly
(1 tank/10s + upgrades, already maxed per 052) and 089 already found
`WATER_THRESHOLD=0.75` pays a real one-time burst catch-up cost at
hot-loop start (~1,390 excess ticks/drone). Candidate concern: with up
to 32 drones all trying to catch up simultaneously, does the shared
pool actually run dry, and does the check-then-act race
(`num_items(Items.Water) > 0` then `use_item(Items.Water)`) cost any
drone real idle/wait time — not just the cheap ~1-tick failed-call
cost the engine's own warning implies?

**Variable.** None committed — measurement only. No code change
proposed regardless of outcome unless the measured cost is large
enough to be worth the risk 089 already established for touching
water-management timing.

**Metric.** Real per-iteration water dynamics (pool size, attempt/fail
counts, `wait` ticks) across all 32 drones, read from `output.txt`
markers — not ticks alone, and not a scored run.

**Baseline.** 091 (champion, merged): 01:53.053, Global Rank #49. Real
`cycle.sh` run for 091 recorded `WARN=2121 Tried to use Items.Water`
(up from 090's 1434/1393) — the number that prompted taking this
seriously rather than dismissing the user's observation.

**Procedure and a real methodology correction mid-investigation.**
1. First attempt: instrumented the real champion's hot loop (`import
   main` trick against the persistent save) to track `use_item()`
   success/failure directly (its own return value, not just the
   engine's log) and `wait` per iteration, across all 32 drones' first
   8 iterations. Result: pool started at **11.3 million tanks** and
   `water_fails` was 0/248 attempts — clearly not representative. The
   persistent save has accumulated an enormous water stockpile from
   this whole session's idle time and prior experiments; this is the
   same class of contamination 091 already found for entity state
   (`nonvirgin` tiles), now showing up for item counts instead.
2. Corrected: ran the same probe logic through `simulate("probe",
   Unlocks, {}, {}, seed, speedup)` instead, matching this project's
   own established pattern for sandboxed, repeatable measurement
   (063/064, wood_single). `sim_items={}` — Grass needs no crafting
   resources to plant, so this is a reasonable proxy for "the
   resources you need to grow the plant" (`docs/wiki/Leaderboard.md`)
   being empty for Hay specifically, and tests the scenario where
   water relies purely on passive regen — the case most likely to show
   real contention if it exists at all. Pool started at a realistic
   ~129 tanks.
3. Extended the observation window from 8 to 26 iterations/drone
   (bounded by hitting the sandbox's own small target) to see whether
   any contention found is a one-time transient or a persistent,
   recurring cost — the exact distinction 089's own water-threshold
   investigation found decisive (a short window there was actively
   misleading).

**Falsifier.** If contention causes real, recurring wait time
throughout a representative window (not just an early transient), it's
a real cost worth sizing for a fix. If it's a small, one-time,
self-resolving transient, closing without a code change is the right
call — 089 already established that touching water-management timing
is a **net loss risk**, not a free lever, so a fix here needs to clear
a real bar, not just "this warning exists."
