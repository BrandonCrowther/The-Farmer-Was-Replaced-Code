# exp-001 — terminate — result

**Outcome.** adopted

**Numbers.**

| run | seed | metric | note |
| --- | --- | --- | --- |
|  1  | random (leaderboard) | **04:55.393** | accepted; PB 04:55.393, global rank **#422** |

**Baseline.** none — the seed cannot finish · **Variant.** 04:55.393 · **Delta.** n/a

**Noise floor.** not yet established for Hay; exp-002 takes the mean over 3 runs.
The `fastest_reset` floor (~10.7 min on a ~15 min run, ≈4%) does not transfer.

**Screenshots.** `logs/captures/20260815-222805-exp-hay-001-run1.png` (modal),
`20260815-222954-warning-output.png` (warnings).

**Verdict.** Termination works and the category now scores. Bounding each drone's
loop on `num_items(Items.Hay)` is enough — no cross-drone signalling needed,
because inventory is shared state every drone can read. `wait_for` over the spawn
handles is what makes the main drone outlive its drones.

Leader is 00:58.549, so there is 5x on the table. The run's own warnings say where
most of it is; `output.txt` (game root, not the save dir) held 7385 lines:

| count | warning |
| --- | --- |
| 760 | Didn't have the required items to plant `Entities.Carrot` |
| 711 | Tried to use `Items.Water` but didn't have enough of it |
| 6 | Cannot plant `Entities.Carrot` on `Grounds.Grassland` |

Both are the seeded achievement strategy meeting leaderboard start conditions it
was never written for. The Hay run starts with what grass needs and lots of
power — no carrot seeds — so `Common.polyculture()` keeps asking for a companion
it cannot plant, and the unconditional `while get_water() < 0.75` keeps reaching
for water that is not there. Neither is fatal, both burn ticks.

That makes the next experiments obvious, and they are worth more than tuning the
grid: **003** drop or condition polyculture for this category, **004** water only
when there is water to use.

**Method note.** `output.txt` is a far better telemetry channel than screenshots
and Phase 3 should read it directly: it lives at the game root (beside
`options.txt` and `Player.log`), *not* in the save directory, so nothing about
reading it touches the `live/save.json` rule.
