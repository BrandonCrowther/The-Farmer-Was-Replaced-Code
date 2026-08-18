# exp-076 — fix setup-phase movement (move_to → move_to_wrapped) — result

**Outcome.** **Adopted, new champion.** 01:57.195, Global Rank #60 — down
from 075's 01:58.059/#63. A real -0.864s improvement, +3 ranks — small,
exactly as expected for a setup-phase-only fix on top of an already
heavily-optimized hot loop (this changes movement paid once per drone
at spawn, not per harvest).

**Numbers.**

| run | metric | note |
| --- | --- | --- |
| validation (target=200,000, `zzRunner.py` replaced with `import main`, arrival check after every `move_to_wrapped` call) | 64/64 `CHECK ... ok`, 0 `MISMATCH` | confirms `move_to_wrapped` lands on the exact same tile `move_to` would have, for both tiles of all 32 drones; `SPAWNED 32 of 32`, no warnings, clean completion |
| real (target=2,000,000,000) | **01:57.195, #60** | `VERDICT=scored`, `WARN=1110 Water` (routine, same shape as prior runs) |

**Baseline.** 075: 01:58.059, #63.

**Delta.** -0.864s (-0.73%), +3 global ranks.

**Verdict.** Confirms the setup-phase theory from the interrupted 076
session: `Common.move_to()`'s unwrapped direct-path walk from spawn to
base, paid once per drone per run (and again every ~2h repeat the
leaderboard averages over, per `docs/LOOP.md`'s "speedup is not a
lever" note), was real avoidable cost — `move_to_wrapped()` has
identical semantics (guaranteed exact arrival, confirmed by the 64/64
validation check) at the shorter wrapped path, plus drops the unused
`protocol()`/`Unlocks.Mazes` overhead `move_to()` always pays. Small
relative to 073's macro-layout change or even 075's hot-loop fix,
because this only touches the one-time setup walk, not the ~871
harvests/drone that follow it — consistent with the user's framing
that Hay's remaining headroom is now made of small increments, not
another structural jump. `saves/hay/main.py` updated and merged to
`main`. `record.json` and `queue.md` updated. Deferred in the same
review, still open: spawn-tree parallelization (~6200 ticks of
sequential spawn latency) and shared bush-wall planting/territory
partitioning — queued as 077.
