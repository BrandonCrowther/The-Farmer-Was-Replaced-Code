# exp-089 — hot-loop mechanism probes (reroll-chase correctness, water threshold)

**Hypothesis (as posed).** Following 088's win, the user asked to think
through further speedups; two concrete, previously-unmeasured
candidates surfaced from reading the hot loop against the documented
`harvest()`/water mechanics rather than assumption:

1. The reroll-chase (`while rerolls < REROLL_LIMIT and companion !=
   None: ... harvest() ...`) has no `can_harvest()` guard — `harvest()`
   destroys whatever's under the drone even if immature ("if you
   harvest an entity that can't be harvested, it will be destroyed").
   Own-handling cost per attempt (~207-208 ticks, exp-066) is less
   than the isolated single-tile growth wait exp-066 separately
   measured (~407-409 ticks). Candidate concern: are most reroll
   attempts destroying immature plants for zero yield?
2. Setup never checks water at all (~20,000+ ticks per drone), and
   `Watering.md` documents ground water decaying continuously ("loses
   1% of its current water per second"). Candidate concern: does the
   hot loop pay an avoidable burst catch-up cost at start because of
   this, and would a different `WATER_THRESHOLD` reduce it?

**Variable.** None committed — this is a measurement/mechanism-
verification pass. Two throwaway probes only (`saves/hay/main.py` in
the worktree, never deployed as a real candidate): (a) per-iteration
tick instrumentation of the existing champion's hot loop (wait /
harvest / reroll-chase / move, split out via `get_tick_count()`); (b)
the same instrumentation with `WATER_THRESHOLD` swept to 0.0 and 0.3.

**Metric.** Real per-iteration tick breakdown, read from `output.txt`
markers (`ITER ...`), not a scored leaderboard run — per
`docs/LOOP.md`'s "a conclusion needs a test that is not a full run."

**Falsifier.** For (1): if reroll-chase `harvest()` calls are
destroying immature plants for zero yield on a meaningful fraction of
attempts, `reroll_ticks` should show irregular/non-linear scaling with
`reroll_count` (evidence of wasted, non-productive cycles). For (2):
if a lower `WATER_THRESHOLD` reduces total ticks/drone over a
*representative* window (not just the first few iterations, which
proved actively misleading), it's a real candidate; if the reduction
is a short-window artifact that reverses once growth becomes rate-
limiting, it's not.

**Procedure.**
1. Instrument `saves/hay/main.py`'s hot loop (every drone logs its own
   first N iterations, capped, to bound `output.txt` size), deploy via
   the `zzRunner.py` → `import main` trick with a dynamically-computed
   `TARGET = num_items(Items.Hay) + margin` (the persistent save's Hay
   inventory already sits at/above the real 2B target after 088's real
   run, so a hardcoded reduced TARGET would skip the hot loop entirely
   — a trap this project's own memory already flags).
2. Read the champion's real per-attempt reroll cost against
   `reroll_count`, and the real per-iteration water-check cost against
   iteration number, at the shipped `WATER_THRESHOLD=0.75`.
3. Re-run the same instrumentation at `WATER_THRESHOLD=0.0` and `0.3`,
   extending the observation window (5 → 40 iterations/drone) once the
   short window looked promising, specifically to check for a steady-
   state cost the short window couldn't reveal.
4. Restore the live game to the champion; no code change proposed
   unless a genuine improvement survives the extended window.
