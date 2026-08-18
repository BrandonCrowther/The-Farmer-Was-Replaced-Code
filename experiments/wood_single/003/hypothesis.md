# exp-003 — measure Tree's harvest/reroll mechanics (probe-only)

**Motivation.** While porting Hay's tonight's stray-tick fixes to
`hay_single` (017, a big -7.9s win), a closer read of `wood_single`'s
own champion (002, a direct transplant of `hay_single`'s much *older*
008-013-era single-tile design) showed two real gaps against the
current best-known pattern: (a) it never received Hay's later
069/070/073+ upgrade (full upfront position pre-seeding, two-tile
interleaving) — its `planted` memory only grows *reactively*, after a
real walk, exactly the "natural accumulation" shape 068 measured as
worse than full pre-seeding for Hay; (b) it uses the exact same
"harvest-to-reroll" idiom Hay uses for Grass, but Tree's own wiki page
has no "grows automatically" exception the way Grass.md does — worth
checking whether that idiom is even doing what it's assumed to do for
Tree specifically, per `docs/LOOP.md`'s own repeated lesson about
checking a mechanic's *own* page for exceptions before reusing a
cost/behavior model across entities.

**Method.** The live/shared save is heavily farmed by tonight's own
Hay/hay_single work (every checked coordinate across 100 samples had
*something* already planted — no clean tile available), and repeated
probing on it gave inconsistent reads run to run (real-time passive
growth continues on the live world between script invocations even
with no drone active, contaminating anything ripeness-dependent).
Switched to `simulate()` — genuine sandbox isolation (fresh world,
controlled starting items/unlocks, `docs/RNG-Seed-Mechanism.md`'s
mechanism, same tool 063/064 used) — running a small `probe.py` inside
it via `simulate("probe", Unlocks, {Items.Wood: 0, Items.Hay: 0}, {},
seed=1, speedup=64)`.

**Result (clean, in-sandbox).**
- `plant(Entities.Tree)` succeeds over auto-grown Grass — Grassland's
  natural Grass cover does **not** count as "already a plant" for
  `plant()`'s own failure condition (Tooltips-Code.md: fails "if...
  there's already a plant there"), only an intentionally-planted entity
  would block it. So `own_tile_ready()`'s replant always works.
- **Harvesting an unripe Tree yields 0 wood and destroys it, reverting
  the tile to Grassland's natural Grass** — confirmed directly
  (`UNRIPE_HARVEST WOOD_GAIN 0 ENTITY_AFTER Entities.Grass`). Tree has
  no Grass-style "grows automatically" exception; the reroll idiom
  ported from Hay works here too, but via a *destructive* path
  (harvest-that-fails-but-still-clears → reverts to Grass → replant),
  not Grass's cheap self-regrow. `own_tile_ready()` does correctly
  recover (replants Tree successfully next call, confirmed).
- This means each reroll attempt for Tree genuinely costs the *old*,
  stale "~400 ticks" model (harvest-that-clears + a real `plant()`)
  that Hay itself had to correct away from (066) specifically *because*
  Grass is exceptional — Wood/Tree is not, so 400 is very plausibly the
  **real** number here, not a mistake to correct.

**Open question, not yet resolved.** Whether a reroll-triggered replant
*resets the current tree's growth clock* (i.e., whether the tree that
eventually gets left standing to mature always starts counting from its
*last* replant, or from something else) is not yet directly measured —
a naive model using 001's isolated growth figure (34,718 ticks) plus
up-to-`REROLL_LIMIT×400` reroll churn predicts a per-harvest cost far
higher (~37k ticks) than the real measured champion average (9,551
ticks/harvest), a ~3.9x gap. The likely explanation is the same one
Hay's own history warns about repeatedly (`docs/LOOP.md`'s "a constant
carries its conditions with it"): 001's 34,718-tick figure may be an
unwatered (water≈0) measurement, the same mistake 019's original
2,819-tick Grass figure made before 037 corrected it 6.7x downward at
real water levels. **Not resolved tonight** — needs its own clean
`simulate()`-based re-measurement (water level controlled, growth timed
precisely) before any redesign, not assumed.

**Status: probe-only, no code change, no adoption.** This is
measurement and a well-reasoned lead, not a finished design. Queued as
004 for a focused follow-up session (re-measure real-water growth time
via `simulate()`; then decide whether full pre-seeding alone helps a
single Tree tile, or whether a genuinely different multi-tile layout is
needed given Tree's cardinal-neighbor 2.44x growth penalty, which rules
out Hay's exact adjacent-tile offset and needs a diagonal or wider
spacing instead). Not attempted live against the real champion given
real remaining uncertainty about the growth-reset question — rushing a
change here risks the same category of mistake this project's own
retrospective (docs/LOOP.md) warns about repeatedly.
