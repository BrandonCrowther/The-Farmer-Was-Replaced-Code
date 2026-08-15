# Entity Planting Costs

> Mirrored from <https://thefarmerwasreplaced.wiki.gg/wiki/Entity_Planting_Costs>
> — CC BY-SA. Regenerate with `python3 tools/fetch_wiki.py`.

This function returns all the costs for planting an entity:

<div id="cb1" class="sourceCode">

``` sourceCode
def GetEntityCosts():
    planting_costs = {
        Entities.Apple: {Items.Cactus:64},
        Entities.Bush: {},
        Entities.Cactus: {Items.Pumpkin:64},
        Entities.Carrot: {Items.Hay:512,Items.Wood:512},
        Entities.Dead_Pumpkin: {},
        Entities.Dinosaur: {},
        Entities.Grass: {},
        Entities.Hedge: {Items.Weird_Substance:32},
        Entities.Pumpkin: {Items.Carrot:512},
        Entities.Sunflower: {Items.Carrot:1},
        Entities.Treasure: {Items.Weird_Substance:32},
        Entities.Tree: {}
    }
    return planting_costs
```

</div>
