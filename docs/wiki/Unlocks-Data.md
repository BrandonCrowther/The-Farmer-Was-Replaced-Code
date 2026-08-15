# Unlocks Data

> Mirrored from <https://thefarmerwasreplaced.wiki.gg/wiki/Unlocks_Data>
> — CC BY-SA. Regenerate with `python3 tools/fetch_wiki.py`.

Here is a function that returns all costs for unlocks

<div id="cb1" class="sourceCode">

``` sourceCode
def GetUnlocksData():
    auto_unlock = [{Items.Pumpkin: 5000}]
    
    cactus = [
        {Items.Pumpkin: 5000},
        {Items.Pumpkin: 20000},
        {Items.Pumpkin: 120000},
        {Items.Pumpkin: 720000},
        {Items.Pumpkin: 4320000},
        {Items.Pumpkin: 25900000}
    ]
    
    carrots = [
        {Items.Wood: 50},
        {Items.Wood: 250},
        {Items.Wood: 1250},
        {Items.Wood: 6250},
        {Items.Wood: 31200},
        {Items.Wood: 156000},
        {Items.Wood: 781000},
        {Items.Wood: 3910000},
        {Items.Wood: 19500000},
        {Items.Wood: 97700000}
    ]
    
    costs = [{Items.Pumpkin: 2500}]
    
    debug = [{
        Items.Hay: 50,
        Items.Wood: 50
    }]
    
    debug_2 = [{Items.Gold: 500}]
    
    dictionaries = [{Items.Pumpkin: 2500}]
    
    dinosaurs = [
        {Items.Cactus: 2000},
        {Items.Cactus: 12000},
        {Items.Cactus: 72000},
        {Items.Cactus: 432000},
        {Items.Cactus: 2590000},
        {Items.Cactus: 15600000}
    ]
    
    expand = [
        {Items.Hay: 30},
        {Items.Wood: 20},
        {Items.Wood: 30, Items.Carrot: 20},
        {Items.Wood: 100, Items.Carrot: 50},
        {Items.Pumpkin: 1000},
        {Items.Pumpkin: 8000},
        {Items.Pumpkin: 64000},
        {Items.Pumpkin: 512000},
        {Items.Pumpkin: 4100000}
    ]
    
    fertilizer = [
        {Items.Wood: 500},
        {Items.Wood: 1500},
        {Items.Wood: 9000},
        {Items.Wood: 54000}
    ]
    
    functions = [{Items.Carrot: 40}]
    
    grass = [
        {Items.Hay: 100},
        {Items.Hay: 300},
        {Items.Wood: 500},
        {Items.Wood: 2500},
        {Items.Wood: 12500},
        {Items.Wood: 62500},
        {Items.Wood: 312000},
        {Items.Wood: 1560000},
        {Items.Wood: 7810000},
        {Items.Wood: 39100000}
    ]
    
    hats = [{Items.Hay: 50}]
    
    imports = [{Items.Carrot: 80}]
    
    leaderboard = [{
        Items.Bone: 2000000,
        Items.Gold: 1000000
    }]
    
    lists = [{Items.Carrot: 500}]
    
    loops = [{Items.Hay: 5}]
    
    mazes = [
        {Items.Weird_Substance: 1000},
        {Items.Cactus: 12000},
        {Items.Cactus: 72000},
        {Items.Cactus: 432000},
        {Items.Cactus: 2590000},
        {Items.Cactus: 15600000}
    ]
    
    megafarm = [
        {Items.Gold: 2000},
        {Items.Gold: 8000},
        {Items.Gold: 32000},
        {Items.Gold: 128000},
        {Items.Gold: 512000}
    ]
    
    operators = [{
        Items.Hay: 150,
        Items.Wood: 10
    }]
    
    plant = [{Items.Hay: 50}]
    
    polyculture = [
        {Items.Pumpkin: 3000},
        {Items.Bone: 10000},
        {Items.Bone: 50000},
        {Items.Bone: 250000},
        {Items.Bone: 1250000}
    ]
    
    pumpkins = [
        {Items.Wood: 500, Items.Carrot: 200},
        {Items.Carrot: 1000},
        {Items.Carrot: 4000},
        {Items.Carrot: 16000},
        {Items.Carrot: 64000},
        {Items.Carrot: 256000},
        {Items.Carrot: 1020000},
        {Items.Carrot: 4100000},
        {Items.Carrot: 16400000},
        {Items.Carrot: 65500000}
    ]
    
    senses = [{Items.Hay: 100}]
    
    simulation = [{Items.Gold: 5000}]
    
    speed = [
        {Items.Hay: 20},
        {Items.Wood: 20},
        {Items.Wood: 50, Items.Carrot: 50},
        {Items.Carrot: 500},
        {Items.Carrot: 1000}
    ]
    
    sunflowers = [{Items.Carrot: 500}]
    
    the_farmers_remains = [{Items.Bone: 100000000}]
    
    timing = [{Items.Pumpkin: 1000}]
    
    top_hat = [{
        Items.Hay: 1000000000,
        Items.Wood: 10000000000,
        Items.Carrot: 1000000000,
        Items.Cactus: 1000000000,
        Items.Gold: 100000000
    }]
    
    trees = [
        {Items.Wood: 50, Items.Carrot: 70},
        {Items.Hay: 300},
        {Items.Hay: 1200},
        {Items.Hay: 4800},
        {Items.Hay: 19200},
        {Items.Hay: 76800},
        {Items.Hay: 307000},
        {Items.Hay: 1230000},
        {Items.Hay: 4920000},
        {Items.Hay: 19700000}
    ]
    
    utilities = [{Items.Pumpkin: 1000}]
    
    variables = [{Items.Carrot: 35}]
    
    watering = [
        {Items.Wood: 50},
        {Items.Wood: 200},
        {Items.Wood: 800},
        {Items.Wood: 3200},
        {Items.Wood: 12800},
        {Items.Wood: 51200},
        {Items.Wood: 205000},
        {Items.Wood: 819000},
        {Items.Wood: 3280000}
    ]
    
    data = {
        Unlocks.Auto_Unlock: auto_unlock,
        Unlocks.Cactus: cactus,
        Unlocks.Carrots: carrots,
        Unlocks.Costs: costs,
        Unlocks.Debug: debug,
        Unlocks.Debug_2: debug_2,
        Unlocks.Dictionaries: dictionaries,
        Unlocks.Dinosaurs: dinosaurs,
        Unlocks.Expand: expand,
        Unlocks.Fertilizer: fertilizer,
        Unlocks.Functions: functions,
        Unlocks.Grass: grass,
        Unlocks.Hats: hats,
        Unlocks.Import: imports,
        Unlocks.Leaderboard: leaderboard,
        Unlocks.Lists: lists,
        Unlocks.Loops: loops,
        Unlocks.Mazes: mazes,
        Unlocks.Megafarm: megafarm,
        Unlocks.Operators: operators,
        Unlocks.Plant: plant,
        Unlocks.Polyculture: polyculture,
        Unlocks.Pumpkins: pumpkins,
        Unlocks.Senses: senses,
        Unlocks.Simulation: simulation,
        Unlocks.Speed: speed,
        Unlocks.Sunflowers: sunflowers,
        Unlocks.The_Farmers_Remains: the_farmers_remains,
        Unlocks.Timing: timing,
        Unlocks.Top_Hat: top_hat,
        Unlocks.Trees: trees,
        Unlocks.Utilities: utilities,
        Unlocks.Variables: variables,
        Unlocks.Watering: watering
    }
    
    return data
```

</div>
