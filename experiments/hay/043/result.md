# exp-043 — tick-rate-check — result

**Outcome.** rejected — clean, decisive negative result. Rules out the
shared-compute-budget hypothesis entirely.

**Numbers.**

| condition | DTICK | DTIME | RATE |
| --- | --- | --- | --- |
| SOLO (before any drone spawned) | 8,002 | 1.32 | **6,074.97** |
| SWARM32 (all 31 others spawned and actively farming) | 8,002 | 1.32 | **6,074.97** |

Identical to 6 significant figures. Also matches hay_single's directly
measured ~6,070 ticks/s (001) almost exactly.

**Baseline.** hay_single: ~6,070 ticks/s, solo.

**Noise floor.** Not established, but a perfect match to the tick leaves
no room for a hidden effect at any meaningful scale.

**Screenshots.** `logs/captures/20260817-001049-exp-hay-043-r1.png`.

**Process note — a real bug, worth recording.** The first attempt at this
probe spawned drones in an unbounded `while True` loop and did not reap
them. The run never ended: a leaderboard run stays "running" while *any*
spawned drone is still executing, whether or not the main script reaps it
— reaping matters for correctness/ordering, not for whether the program is
considered "done." `Shift+F5` did not stop it either, confirming
docs/LOOP.md's existing warning. Recovered with `tools/tfwr.sh relaunch`
(no data lost, run doesn't count toward anything). Fixed by giving each
spawned drone a small bounded cycle count and reaping them with
`wait_for()` before the script ends. Also hit a separate, unrelated syntax
error first: this game's Python subset does **not** support the ternary
expression `x if cond else y` — worth adding to docs/wiki notes on
Differences-from-python if it isn't already there.

**Verdict.** Tick rate is a fixed constant, independent of concurrent
drone count. 041's ~3x growth-time gap between Hay (~1,183 ticks) and
hay_single (~404 ticks) is **not** explained by a shared per-drone tick
budget — the real cause (a genuine category-level growth-condition
difference, or something else) is still open, but it no longer threatens
039's leader-implied ~441-ticks/harvest estimate, which was computed as a
same-category time ratio and never depended on tick rate being comparable
across categories in the first place. **042 (multi-tile-per-drone) can
proceed on the numbers already in hand** — 041's measured ~492-tick idle
window on hit-cycles, and 039's leader-implied target, both stand.
