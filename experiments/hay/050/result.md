# exp-050 — is a global dict actually shared across spawned drones? — result

**Outcome.** rejected the shared-memory idea — confirmed drones are
fully isolated.

**Numbers.**

| run | metric | note |
| --- | --- | --- |
| r1 | `WRITER wrote {'from_writer':12345}` | the spawned writer drone did write to the top-level dict |
| r1 | `READER sees {}`, `MAIN sees {}` | neither the reader drone nor the main drone can see that write |

**Baseline.** None — first direct check of this assumption tonight.

**Noise floor.** N/A — deterministic behavior.

**Screenshots.** None — probe.

**Verdict.** Each spawned drone runs in a fully isolated execution
context — a plain Python variable defined once at the top level is
NOT shared state across drones, only a per-drone independent copy.
The only channel between drones is the physical game world (entity
positions, item counts, ground types). This rules out any design that
would rely on a shared companion-memory dict across the 32 drones —
"neighbor cooperation" can only ever happen through the physical
side-effect of one drone's `plant()` call, never through direct
information sharing.
