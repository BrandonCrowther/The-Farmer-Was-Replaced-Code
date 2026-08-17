# exp-002 — natural-grass-growth-check — result

**Outcome.** confirmed, and stronger than the stated hypothesis — a real,
directly-observed, high-value mechanic.

**Numbers.**

| check | value |
| --- | --- |
| tile `(5,5)`, first check (tick 2, ≈time 0) | `Entities.Grass` on `Grounds.Grassland` |
| tile `(5,5)`, second check (tick 233,387, ≈38.4s later, 6 unrelated Carrot cycles elapsed) | `Entities.Grass` on `Grounds.Grassland` — unchanged |

**The tile already had Grass at tick 2** — not something that grew in over
the 38 real seconds between checks. **Untouched grassland starts with
Grass on it, standing, from the very beginning of the run.**

**Baseline.** 001's indirect evidence (3/3 Grass-companion requests
multiplied without servicing).

**Noise floor.** N/A — direct observation, n=1 but decisive (a tile either
has Grass or it doesn't).

**Screenshots.** None — probe.

**Verdict — this changes the whole design shape for any category that
doesn't farm Grass itself.** Any companion request naming `Entities.Grass`
at a position this drone has never touched is **already satisfied, for
free, with certainty** — no plant, no till, no tick cost beyond the
`get_companion()` read itself. That's not a probabilistic memory-hit the
way hay_single's `Bush`/`Tree` stock was; it's the board's default state.
Structurally: of the 3 possible companion types (Grass/Bush/Tree — Carrot
never requests itself), **1/3 of all draws are free by construction**,
before any reroll or memory-building at all. The remaining 2/3
(Bush/Tree) still need real servicing — but note the asymmetry: satisfying
one *consumes* the free-grass property at that specific position (planting
Bush/Tree there overwrites the natural grass), so a design that reverts a
position back to Grass after using it keeps that 1/3-free rate available
indefinitely, rather than slowly eroding it. 003 should design the driver
around this directly, and also settle the second major finding from 001:
Carrot's own growth (~7,196 ticks mean) is ~17.8x slower than hay_single's
Grass (~404 ticks) — this category is very likely growth-bound rather than
servicing-bound, reopening multi-tile as a serious design (a large idle
window, unlike Hay's too-small one and hay_single's nonexistent one).
