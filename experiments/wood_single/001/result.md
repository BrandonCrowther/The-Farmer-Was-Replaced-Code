# exp-001 — mechanics-probe — result

**Outcome.** probe — labels were backwards but the real numbers are
clear and very promising.

**Numbers.**

| run | metric | note |
| --- | --- | --- |
| r1 | `START` all 0, `COST_TREE {}` | free to plant, no bootstrap resources at all |
| r1 | `TILE_A_ISOLATED GROWTH_TICKS 34718 BASE_GAIN 409600` | mislabeled — see verdict, this is actually the *multiplied* yield (an accidental free-Grass companion hit) |
| r1 | `TILE_C_NEIGHBOR GROWTH_TICKS 84651` | a tree planted immediately adjacent to another growing tree takes **2.44x longer** to grow (Entities.md's warning, confirmed real and large) |
| r1 | `TILE_D_MULTIPLIED GAIN 2560 RATIO 0.01` | mislabeled — this is the *true base* (unmultiplied) yield; the attempted companion (Carrot) couldn't be afforded (0 starting Hay), so `Common.affordable()` correctly skipped it, leaving this harvest genuinely unsatisfied |

**Baseline.** None — first probe.

**Noise floor.** Not established.

**Screenshots.** None — probe.

**Verdict.** True base yield is **2,560**; true full-multiplier yield is
**409,600** — exactly `2560 * 160`, matching this save's known maxed
Polyculture multiplier (160x, established earlier tonight for Hay/Carrot).
Tile A's "base" harvest actually got the full 160x by accident — almost
certainly the same free-Grass mechanic carrots_single found (untouched
grassland already has standing Grass, satisfying a Grass-companion draw
for free) applies here too. `500,000,000 / 409,600 ≈ 1,221` harvests
needed at full multiplier — nearly identical to carrots_single's harvest
count. The real constraint to design around is the **2.44x neighbor
growth penalty**: any multi-tile design needs real spacing between farm
tiles, not just the companion-range self-collision safety margin. 002
builds the single-tile reactive design (reroll-before-walk, same
paradigm as hay_single/carrots_single) — safe from the neighbor penalty
since only one Tree exists on the farm at a time.
