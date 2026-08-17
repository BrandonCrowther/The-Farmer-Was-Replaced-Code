# exp-001 — mechanics-probe — result

**Outcome.** inconclusive (by design — a probe, not an optimisation). Supplies
the numbers the floor design in `queue.md` needed.

**Numbers** (from `output.txt`, one run):

| quantity | value | note |
| --- | --- | --- |
| world size | 8 | confirms the wiki's "8x8 farm" |
| max_drones | 1 | confirms single-drone |
| `Entities.Carrot` cost | 512 hay + 512 wood | matches Hay category exactly |
| Bush/Tree/Grass cost | free | matches Hay category |
| move/till/plant | 200 / 201 / 201 ticks | the +1 on till/plant is the preceding `quick_print` call's own tuple-construction cost, not the operation — 200 is confirmed |
| water | reaches ~1.0 after 1 fill; tank held at 2 units the whole probe (32 ticks / 0.08s, too short to see a refill) | starting tank is small; needs a longer sample before trusting an equilibrium number |
| growth ticks (5 samples) | 401, 402, 404, 407, 407 — mean 404.2 | at water ~0.99–1.0. **Coincidentally close to the "422±14.5" figure docs/LOOP.md attributes to `experiments/hay/037`, which does not exist as a run** (no directory, no result.md — flagged in 001's hypothesis). Treat the closeness as two independent, roughly-agreeing measurements, not as validating the missing one. |
| companion distance | raw Manhattan gave 1, 7, 2, 2, 13 — **wrong metric.** Re-computed wrapped (world size 8, wrap both axes): 1, 1, 2, 2, 3. Every request is ≤3, exactly matching Polyculture.md. The probe's own distance calc didn't wrap; a real driver must use `move_to_wrapped`-style arithmetic (already in Hay's `Common.py`) from the first line, not discover this failure mode itself. |
| tick rate | `TICK_FINAL 4803` at `TIME_FINAL 0.79`s (and `TICK0 9` at `TIME0 0`) → **≈6070 ticks/s**, ~15.2x the base 400/s. Confirms the design note's suspicion: leaderboard categories evidently start with enough Power to multiply execution speed well past the unpowered rate, and it must be read per-category, not assumed. Single sample — worth a longer probe before treating as exact. |
| bare yield | 512, 1024, 1536, 2048, 2560 (cumulative +512 each) | confirms unsatisfied-companion yield is 512, same as Hay — expected, since the probe never walked to a companion tile. |

**Baseline.** None (first-ever hay_single run).

**Noise floor.** Not established — single run, deliberately short, not a scored
cycle. Growth-tick spread (401–407, sd ≈2.6) suggests it's tight at this water
level, but n=5 is not enough to trust that on its own.

**Screenshots.** `logs/captures/20260816-211051-debug-state.png` (the modal —
harmless leftover reused; the actual data lives in `output.txt`, not the
modal, for this probe).

**Verdict — the floor computation queue.md asked for:**

- Ticks available at the leader's pace: `6070 * 137.995 ≈ 837,600`.
- Harvests needed at full multiplier (81,920/harvest, unverified here — see
  falsifier below): `ceil(100,000,000 / 81,920) = 1,221`.
- Required average ticks/harvest to match the leader: `837,600 / 1,221 ≈ 686`.
- Own-tile floor (harvest + replant, no till if ground stays Grassland):
  `~400-404` ticks — leaves only **~282 ticks of average companion-servicing
  budget per harvest**.
- **The schedulability floor is 1 tile**, not more: own-tile handling
  (~400-404 ticks) already exceeds growth time (~404 mean), so a single tile
  is never idle-blocked waiting to ripen, and a second tile would only add
  pure movement overhead across the 8x8 board for zero throughput gain —
  exactly what sank Hay's own 027/029 multi-plot attempts, for the same
  underlying reason.
- **But 1 tile, run the way Hay's champion runs its own tile, is not fast
  enough.** Hay's best measured per-drone pass average is 967 ticks (020's
  queue text) — that includes real companion walks on a large minority of
  passes. hay_single's budget is **686**, tighter than Hay's own champion
  average, with only ~282 ticks of slack for companion work per harvest. A
  single real companion round trip (move + till + plant) costs on the order
  of 800–1,600 ticks depending on distance and whether the tile needs
  changing — several times the whole remaining budget. The arithmetic says
  the **skip rate** (companion tile already correct, cost ≈ a lookup, not a
  walk) needs to be roughly **≥75%**, well above anything the Hay project's
  reactive reroll-until-hit approach reached (their own ceiling analysis
  topped out nearer 45–66%). That points the write-driver experiment (002)
  at Hay's never-tried **038 monocrop-stock** idea — pre-plant all reachable
  companion positions once, so almost every pass is a pure lookup — rather
  than at the reactive skip-and-reroll machinery Hay ended up with.

**Falsifier for 002.** This floor assumes the 160x multiplier (81,920/harvest)
transfers unchanged from Hay. 002's driver must verify a real satisfied
harvest here before trusting that number — if the multiplier differs, every
figure above needs recomputing, not just re-reading.
