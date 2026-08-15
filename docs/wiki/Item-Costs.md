# Item Costs

> Mirrored from <https://thefarmerwasreplaced.wiki.gg/wiki/Item_Costs>
> — CC BY-SA. Regenerate with `python3 tools/fetch_wiki.py`.

## 

This page describes a feature that is no longer relevant in the game

The trade-based item economy this page originally documented (`Items.Carrot_Seed`, `Items.Sunflower_Seed`, `Items.Pumpkin_Seed`, `Items.Empty_Tank`, and the `trade()` function) has been removed from the game entirely. Seeds are no longer purchased with traded items; entities are now planted directly with `plant(entity)` for a cost in base resources (see <a href="Entity_Planting_Costs" class="wikilink" title="Entity Planting Costs">Entity Planting Costs</a>), and water/fertilizer now accrue automatically over time (see <a href="Watering" class="wikilink" title="Watering">Watering</a> and <a href="Fertilizer" class="wikilink" title="Fertilizer">Fertilizer</a>).

To check the current cost of anything (a plant or an unlock) in-game, use the `get_cost()` function instead of relying on a static table:

<div id="cb1" class="sourceCode">

``` sourceCode
cost = get_cost(Entities.Carrot)
for item in cost:
    amount_needed = cost[item]
```

</div>

See <a href="Costs" class="wikilink" title="Costs">Costs</a> for full details on `get_cost()`.
