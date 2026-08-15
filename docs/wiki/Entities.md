# Entities

> Mirrored from <https://thefarmerwasreplaced.wiki.gg/wiki/Entities>
> — CC BY-SA. Regenerate with `python3 tools/fetch_wiki.py`.
> Also known as: Tooltips Entities.

This page lists every plantable/harvestable entity currently in the game, with the description shown in-game. Data taken directly from the game's current string files. Exact grow-time and plant-cost numbers are not covered by the available string data and should be verified in-game; see <a href="Entity_Planting_Costs" class="wikilink" title="Entity Planting Costs">Entity Planting Costs</a> for a code-derived cost table.

## `Apple`

Dinosaurs love them apparently. Spawned automatically while wearing the <a href="Dinosaurs" class="wikilink" title="Dinosaur Hat">Dinosaur Hat</a>; see <a href="Dinosaurs" class="wikilink" title="Dinosaurs">Dinosaurs</a>.

## `Bush`

A small bush that drops `Items.Wood`.

## <a href="Cactus" class="wikilink" title="Cactus"><code>Cactus</code></a>

Cacti come in 10 different sizes. When harvested, adjacent cacti that are "sorted" will also be harvested. See <a href="Cactus" class="wikilink" title="Cactus">Cactus</a> for full mechanics.

## `Carrot`

Carrots!

## `Dead Pumpkin`

One in five pumpkins dies when it grows up, leaving behind a dead pumpkin. Dead pumpkins are useless and disappear when something new is planted.

## <a href="Dinosaurs" class="wikilink" title="Dinosaur"><code>Dinosaur</code></a>

A piece of the tail of the dinosaur hat. See <a href="Dinosaurs" class="wikilink" title="Dinosaurs">Dinosaurs</a> for full mechanics.

## `Grass`

Grows automatically on grassland. Harvest it to obtain `Items.Hay`.

## `Hedge`

Part of the <a href="Mazes" class="wikilink" title="maze">maze</a>.

## `Pumpkin`

Pumpkins grow together when they are next to other fully grown pumpkins. About 1 in 5 pumpkins dies when it grows up.

## `Sunflower`

Sunflowers collect the power from the sun. Harvesting them will give you `Items.Power`. If you harvest a sunflower with the maximum number of petals you get bonus power.

## `Treasure`

A treasure that contains gold equal to the side length of the <a href="Mazes" class="wikilink" title="maze">maze</a> in which it is hidden. It can be harvested like a plant.

## `Tree`

Trees drop more wood than bushes. They take longer to grow if other trees grow next to them.

## Grounds

### `Grassland`

The default ground. Grass will automatically grow on it.

### `Soil`

Calling `till()` turns the ground into soil. Calling `till()` again changes it back to grassland.
