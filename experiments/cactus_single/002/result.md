# exp-002 — resources, unlocks, cascade-yield scaling — result

**Outcome.** adopted — found the exact yield formula, and it points
straight at the intended full-grid design.

**Numbers.**

| run | metric | note |
| --- | --- | --- |
| r1 | `PUMPKIN` 1,000,000,000, `CACTUS_UNLOCK` 6, `COST_CACTUS {Items.Pumpkin:64}` | huge stockpile, resource cost a non-issue (same as carrots_single/hay_single) |
| r1 | 2-cactus forced cascade (sizes 1, 9 after one `swap()`): `GAINED` 128 | |

**Baseline.** 001: lone harvest (n=1), 32 gained.
**Variant.** n=2 cascade, 128 gained. **Delta.** `128 / 32 = 4 = 2**2`
exactly — **yield = `32 * n**2`**, independent of the individual cactus
sizes involved (sizes 1 and 9 here vs size 2 for 001's lone harvest,
same flat 32 multiplier either way).

**Noise floor.** Not applicable — an exact `n**2` ratio from 2 data
points isn't noise, and 003 (n=16) reconfirms it exactly.

**Screenshots.** None — probe.

**Verdict.** `32 * n**2` with `n=64` (a full 8x8 grid, fully sorted,
harvested in one cascade) is `32 * 4096 = 131,072` — **exactly**
Cactus_Single's target (Leaderboard.md). This is not a coincidence: the
category is designed to be solved by building one perfectly sorted 8x8
grid and harvesting a single corner. The only remaining unknown is
whether an 8x8 grid can be fully sorted cheaply enough via adjacent
`swap()`s — 003 validates the sort algorithm at 4x4 scale before
committing to the full grid.
