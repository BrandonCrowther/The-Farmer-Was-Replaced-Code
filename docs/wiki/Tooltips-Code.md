# Tooltips Code

> Mirrored from <https://thefarmerwasreplaced.wiki.gg/wiki/Tooltips_Code>
> — CC BY-SA. Regenerate with `python3 tools/fetch_wiki.py`.
> Also known as: Tooltips.

## `abs(number)`

Computes the absolute value of a number.

returns `number` if `number` is positive, `-number` otherwise.

takes 1 tick to execute.

example usage:

<div id="cb1" class="sourceCode">

``` sourceCode
abs(-69)
```

</div>

## `set.add(element)`

Adds `element` to the `set`.

returns `None`

takes `element size` ticks to execute.

example usage:

<div id="cb2" class="sourceCode">

``` sourceCode
set = {0}
set.add(1)
```

</div>

## `and`

Evaluates the first operand. If it's falsy (`False`, `0` and empty collections), it returns that value immediately (short-circuiting the evaluation), otherwise, it evaluates and returns the second operand.

## `list.append(element)`

Adds `element` to the end of the `list`.

returns `None`

takes `1` ticks to execute.

example usage:

<div id="cb3" class="sourceCode">

``` sourceCode
list = []
list.append(1)
```

</div>

## `break`

Break out of a loop and continue executing the statements after the loop. If there are nested loops, this will always affect the innermost loop.

## `can_harvest()`

Used to find out if plants are fully grown.

returns `True` if there is an entity under the drone that is ready to be harvested, `False` otherwise.

takes `1` tick to execute.

example usage:

<div id="cb4" class="sourceCode">

``` sourceCode
if can_harvest():
    harvest()
```

</div>

## `can_move(direction)`

Checks if the drone can move in the specified `direction`.

returns `True` if the drone can move, `False` otherwise.

takes `1` tick to execute.

example usage:

<div id="cb5" class="sourceCode">

``` sourceCode
if can_move(North):
    move(North)
```

</div>

## `change_hat(hat)`

Changes the hat of the drone to `hat`.

returns `None`

takes `200` ticks to execute.

example usage:

<div id="cb6" class="sourceCode">

``` sourceCode
change_hat(Hats.Dinosaur_Hat)
```

</div>

## `clear()`

Removes everything from the farm, moves the drone back to position `(0,0)` and changes the hat back to the straw hat.

returns `None`

takes `200` ticks to execute.

example usage:

<div id="cb7" class="sourceCode">

``` sourceCode
clear()
```

</div>

## `continue`

Immediately continue with the next loop iteration. If there are nested loops, this will always affect the innermost loop.

## `def`

Defines a function.

## `dict(dictionary = None)`

Creates a new dictionary. If `dictionary` is None, it creates an empty dictionary. If `dictionary` is a dictionary, it creates a copy of it.

returns a dictionary.

takes `1 + len(dictionary)` ticks to execute.

example usage:

<div id="cb8" class="sourceCode">

``` sourceCode
new_dict = dict()
```

</div>

## `do_a_flip()`

Makes the drone do a flip! This action is not affected by speed upgrades.

returns `None`

takes 1s to execute.

example usage:

<div id="cb9" class="sourceCode">

``` sourceCode
while True:
    do_a_flip()
```

</div>

## `East`

The right direction on the screen. Unless you turn your screen around.

## `elif`

Does the same thing as:

<div id="cb10" class="sourceCode">

``` sourceCode
else:
    if condition:
```

</div>

## `else`

Executes code if the previous `if` condition was `False`.

## <a href="Entities" class="wikilink" title="Entities"><code>Entities</code></a>

Contains all plant types. Can be iterated with a `for` loop.

<div class="toccolours mw-collapsible mw-collapsed" expandtext="show values" collapsetext="hide values" style="max-width:32em">

`values`

<div class="mw-collapsible-content">

  
.Apple

.Bush

.Cactus

.Carrot

.Dead_Pumpkin

.Dinosaur

.Grass

.Hedge

.Pumpkin

.Sunflower

.Treasure

.Tree

</div>

</div>

## `False`

A boolean value that is always false.

## `for`

A loop that iterates over all elements of a sequence. Some programming languages call this a "foreach" loop.

## `get_companion()`

Get the preferred companion of the plant under the drone.

returns a tuple of the form `(companion_type, (companion_x_position, companion_y_position))`

takes `1` tick to execute.

example usage:

<div id="cb11" class="sourceCode">

``` sourceCode
companion = get_companion()
if companion != None:
    plant_type, (x, y) = companion
    print("Companion:", plant_type, "at", x, ",", y)
```

</div>

## `get_cost(thing)`

Gets the cost of a `thing`

If `thing` is an entity get the cost of planting it. If `thing` is an unlock get the cost of unlocking it.

returns a dictionary with items as keys and numbers as values. Each item is mapped to how much of it is needed. returns `{}` when used on an upgradeable unlock that is already at the max level.

takes `1` tick to execute.

example usage:

<div id="cb12" class="sourceCode">

``` sourceCode
cost = get_cost(Unlocks.Carrots)
for item in cost:
    if num_items(item) < cost[item]:
        print("not enough items to unlock carrots")
```

</div>

## `get_entity_type()`

Find out what kind of entity is under the drone.

returns `None` if the tile is empty, otherwise returns the type of the entity under the drone.

takes `1` tick to execute.

example usage:

<div id="cb13" class="sourceCode">

``` sourceCode
if get_entity_type() == Entities.Grass:
    harvest()
```

</div>

## `get_ground_type()`

Find out what kind of ground is under the drone.

returns the type of the ground under the drone.

takes `1` tick to execute.

example usage:

<div id="cb14" class="sourceCode">

``` sourceCode
if get_ground_type() != Grounds.Soil:
    till()
```

</div>

## `get_pos_x()`

Gets the current x position of the drone. The x position starts at `0` in the west and increases in the east direction.

returns a number representing the current x coordinate of the drone.

takes `1` tick to execute.

example usage:

<div id="cb15" class="sourceCode">

``` sourceCode
x, y = get_pos_x(), get_pos_y()
```

</div>

## `get_pos_y()`

Gets the current y position of the drone. The y position starts at `0` in the south and increases in the north direction.

returns a number representing the current y coordinate of the drone.

takes `1` tick to execute.

example usage:

<div id="cb16" class="sourceCode">

``` sourceCode
x, y = get_pos_x(), get_pos_y()
```

</div>

## `get_tick_count()`

Used to measure the number of ticks performed.

returns the number of ticks performed since the start of execution.

takes `0` tick to execute.

example usage:

<div id="cb17" class="sourceCode">

``` sourceCode
do_something()

print(get_tick_count())
```

</div>

## `get_time()`

Get the current game time.

returns the time in seconds since the start of the game.

takes `0` ticks to execute.

example usage:

<div id="cb18" class="sourceCode">

``` sourceCode
start = get_time()

do_something()

time_passed = get_time() - start
```

</div>

## `get_water()`

Get the current water level under the drone.

returns the water level under the drone as a number between `0` and `1`.

takes `1` tick to execute.

example usage:

<div id="cb19" class="sourceCode">

``` sourceCode
if get_water() < 0.5:
    use_item(Items.Water)
```

</div>

## `get_world_size()`

Get the current size of the farm.

returns the side length of the grid in the north to south direction.

takes `1` tick to execute.

example usage:

<div id="cb20" class="sourceCode">

``` sourceCode
for i in range(get_world_size()):
    move(North)
```

</div>

## <a href="Grounds" class="wikilink" title="Grounds"><code>Grounds</code></a>

Contains all possible ground types. Can be iterated with a `for` loop.

<div class="toccolours mw-collapsible mw-collapsed" expandtext="show values" collapsetext="hide values" style="max-width:32em">

`values`

<div class="mw-collapsible-content">

  
.Grassland

.Soil

</div>

</div>

## `harvest()`

Harvests the entity under the drone. If you harvest an entity that can't be harvested, it will be destroyed.

returns `True` if an entity was removed, `False` otherwise.

takes `200` ticks to execute if an entity was removed, `1` tick otherwise.

example usage:

<div id="cb21" class="sourceCode">

``` sourceCode
harvest()
```

</div>

## `has_finished(drone)`

Checks if the given `drone` has finished.

returns `True` if the `drone` has finished, `False` otherwise.

takes `1` tick to execute.

example usage:

<div id="cb22" class="sourceCode">

``` sourceCode
drone = spawn_drone(function)
while not has_finished(drone):
    do_something_else()
result = wait_for(drone)
```

</div>

## <a href="Hats" class="wikilink" title="Hats"><code>Hats</code></a>

Contains all hat types. Can be iterated with a `for` loop.

<div class="toccolours mw-collapsible mw-collapsed" expandtext="show values" collapsetext="hide values" style="max-width:32em">

`values`

<div class="mw-collapsible-content">

  
.Straw_Hat

.Brown_Hat

.Cactus_Hat

.Carrot_Hat

.Dinosaur_Hat

.Gold_Hat

.Gold_Trophy_Hat

.Golden_Gold_Hat

.Gray_Hat

.Green_Hat

.Pumpkin_Hat

.Purple_Hat

.Silver_Trophy_Hat

.Sunflower_Hat

.Top_Hat

.Traffic_Cone

.Traffic_Cone_Stack

.Tree_Hat

.Wizard_Hat

.Wood_Trophy_Hat

</div>

</div>

## `if`

Executes code if the condition is `True`.

## `list.insert(i, element)`

Inserts `element` into the `list` at index `i`.

returns `None`

takes `len(list) - i + 1` ticks.

example usage:

<div id="cb23" class="sourceCode">

``` sourceCode
list = [1,2]
list.insert(0, 0)
```

</div>

## <a href="Items" class="wikilink" title="Items"><code>Items</code></a>

Contains all items that can be in the inventory. Can be iterated with a `for` loop.

<div class="toccolours mw-collapsible mw-collapsed" expandtext="show values" collapsetext="hide values" style="max-width:32em">

`values`

<div class="mw-collapsible-content">

  
.Bone

.Cactus

.Carrot

.Fertilizer

.Gold

.Hay

.Power

.Pumpkin

.Water

.Weird_Substance

.Wood

</div>

</div>

## `leaderboard_run(leaderboard, file_name, speedup)`

Starts a timed simulation for the `leaderboard` using the specified `file_name` as a starting point. `speedup` sets the starting speedup.

returns `None`

takes `200` ticks to execute.

example usage:

<div id="cb24" class="sourceCode">

``` sourceCode
leaderboard_run(Leaderboards.Fastest_Reset, "full_run", 256)
```

</div>

## <a href="Leaderboards" class="wikilink" title="Leaderboards"><code>Leaderboards</code></a>

Contains all leaderboard categories. Can be iterated with a `for` loop.

<div class="toccolours mw-collapsible mw-collapsed" expandtext="show values" collapsetext="hide values" style="max-width:32em">

`values`

<div class="mw-collapsible-content">

  
.Fastest_Reset

.Maze

.Dinosaur

.Cactus

.Sunflowers

.Pumpkins

.Wood

.Carrots

.Hay

.Maze_Single

.Cactus_Single

.Sunflowers_Single

.Pumpkins_Single

.Wood_Single

.Carrots_Single

.Hay_Single

</div>

</div>

## `len(collection)`

Get the number of elements in a list, set, dict or tuple.

returns the length of the `collection`.

takes `1` tick to execute.

example usage:

<div id="cb25" class="sourceCode">

``` sourceCode
for i in range(len(list)):
    list[i] += 1
```

</div>

## `list(collection = None)`

Creates a new list. If `collection` is None, it creates an empty list. If `collection` is any sequence, it creates a new list with the element of the sequence.

returns a list.

takes `1 + len(collection)` ticks to execute.

example usage:

<div id="cb26" class="sourceCode">

``` sourceCode
new_list = list((1,2,3))
```

</div>

## `max(*args)`

Gets the maximum of a sequence of elements or several passed arguments. Can be used on numbers and strings.

`max(a,b,c)`: Returns the maximum of `a`, `b` and `c`. `max(sequence)`: Returns the maximum of all values in a sequence.

takes \#comparisons ticks to execute.

example usage:

<div id="cb27" class="sourceCode">

``` sourceCode
max([3,6,34,16])
```

</div>

## `max_drones()`

returns the maximum number of drones that you can have in the farm.

takes `1` tick to execute.

example usage:

<div id="cb28" class="sourceCode">

``` sourceCode
while num_drones() < max_drones():
    spawn_drone(task)
    move(East)
```

</div>

## `measure(direction = None)`

Can measure some values on some entities. The effect of this depends on the entity.

If `direction` is not `None` it measures the neighboring entity in the given direction.

returns the number of petals of a sunflower. returns the next position for a treasure or apple. returns the size of a cactus. returns a mysterious number for a pumpkin. returns `None` for all other entities.

takes `1` tick to execute.

example usage:

<div id="cb29" class="sourceCode">

``` sourceCode
num_petals = measure()
```

</div>

## `min(*args)`

Gets the minimum of a sequence of elements or several passed arguments. Can be used on numbers and strings.

`min(a,b,c)`: Returns the minimum of `a`, `b` and `c`. `min(sequence)`: Returns the minimum of all values in a sequence.

takes \#comparisons ticks to execute.

example usage:

<div id="cb30" class="sourceCode">

``` sourceCode
min([3,6,34,16])
```

</div>

## `move(direction)`

Moves the drone into the specified `direction` by one tile. If the drone moves over the edge of the farm it wraps back to the other side of the farm.

`East` = right `West` = left `North` = up `South` = down

returns `True` if the drone has moved, `False` otherwise.

takes `200` ticks to execute if the drone has moved, `1` tick otherwise.

example usage:

<div id="cb31" class="sourceCode">

``` sourceCode
move(North)
```

</div>

## `None`

A value representing that there is no value.

## `North`

The up direction on the screen. Unless you turn your screen around.

## `not`

`not True` is `False` and `not False` is `True`.

## `num_drones()`

returns the number of drones currently in the farm.

takes `1` tick to execute.

example usage:

<div id="cb32" class="sourceCode">

``` sourceCode
while num_drones() < max_drones():
    spawn_drone(task)
    move(East)
```

</div>

## `num_items(item)`

Find out how much of `item` you currently have.

returns the number of `item` currently in your inventory.

takes `1` tick to execute.

example usage:

<div id="cb33" class="sourceCode">

``` sourceCode
if num_items(Items.Fertilizer) > 0:
    use_item(Items.Fertilizer)
```

</div>

## `num_unlocked(thing)`

Used to check if an unlock, entity, ground, item or hat is already unlocked.

returns `1` plus the number of times `thing` has been upgraded if `thing` is upgradable. Otherwise returns `1` if `thing` is unlocked, `0` otherwise.

takes `1` tick to execute.

example usage:

<div id="cb34" class="sourceCode">

``` sourceCode
plant(Entities.Bush)
n_substance = get_world_size() * num_unlocked(Unlocks.Mazes)
use_item(Items.Weird_Substance, n_substance)
```

</div>

## `or`

Evaluates the first operand. If it's truthy (anything other than `False`, `0` and empty collections), it returns that value immediately (short-circuiting the evaluation), otherwise, it evaluates and returns the second operand.

## `pass`

Does nothing. Can be useful because empty code blocks aren't allowed.

## `pet_the_piggy()`

Pets the piggy! This action is not affected by speed upgrades.

returns `None`

takes 1s to execute.

example usage:

<div id="cb35" class="sourceCode">

``` sourceCode
while True:
    pet_the_piggy()
```

</div>

## `plant(entity)`

Spends the cost of the specified `entity` and plants it under the drone. It fails if you can't afford the plant, the ground type is wrong or there's already a plant there.

returns `True` if it succeeded, `False` otherwise.

takes `200` ticks to execute if it succeeded, `1` tick otherwise.

example usage:

<div id="cb36" class="sourceCode">

``` sourceCode
plant(Entities.Bush)
```

</div>

## `collection.pop()`

Removes the last element from a list or the specified element from a dictionary. `list.pop(i)` removes the element at the index `i` from the `list`.

returns the removed element

takes `key size` ticks to execute on a dictionary, `len(list) - i + 1` ticks on a list.

example usage:

<div id="cb37" class="sourceCode">

``` sourceCode
list = [True, False, None]
list.pop(0)
```

</div>

## `print(*args)`

Prints all `args` into the air above the drone using smoke. This action is not affected by speed upgrades. Multiple values can be printed at once.

returns `None`

takes 1s to execute.

example usage:

<div id="cb38" class="sourceCode">

``` sourceCode
print("ground:", get_ground_type())
```

</div>

## `quick_print(*args)`

Prints a value just like `print(*args)` but it doesn't stop to write it into the air so it can only be found on the output page.

returns `None`

takes `0` ticks to execute.

example usage:

<div id="cb39" class="sourceCode">

``` sourceCode
quick_print("hi mom")
```

</div>

## `random()`

Samples a random number between 0 (inclusive) and 1 (exclusive).

returns the random number.

takes `1` ticks to execute.

example usage:

<div id="cb40" class="sourceCode">

``` sourceCode
def random_elem(list):
    index = random() * len(list) // 1
    return list[index]
```

</div>

## `range(start = 0, end, step = 1)`

Generates a sequence of numbers starting at `start`, ending right before reaching `end` (so `end` is excluded) using steps of size `step`.

Note that start is set to `0` by default, and if only one argument is given, it will bind to `end`. This isn't normally possible. In Python, `range` is a class constructor that allows this strange behavior.

takes `1` tick to execute.

example usage:

<div id="cb41" class="sourceCode">

``` sourceCode
for i in range(10):
    print(i)

for i in range(2,6):
    print(i)

for i in range(10, 0, -1):
    print(i)
```

</div>

## `collection.remove(element)`

Removes the first occurrence of `element` from the `collection`.

returns `None`

takes `element size` ticks to execute on a set, \#comparisions + \#shifts ticks on a list.

example usage:

<div id="cb42" class="sourceCode">

``` sourceCode
list = [True, False, None]
list.remove(False)
```

</div>

## `reset()`

Resets the farm back to a 1x1 square, removes all resources and locks most unlocks. It doesn't remove any of your code.

returns `None`

takes `200` ticks to execute.

example usage:

<div id="cb43" class="sourceCode">

``` sourceCode
reset()
```

</div>

## `return`

Used to return a value from a function.

## `set(collection = None)`

Creates a new set. If `collection` is None, it creates an empty set. If `collection` is a collection of values, it creates a new set with those values in it.

returns a set.

takes `1 + len(collection)` ticks to execute.

example usage:

<div id="cb44" class="sourceCode">

``` sourceCode
new_set = set((1,2,3))
```

</div>

## `set_execution_speed(speed)`

Limits the speed at which the program is executed to better see what's happening.

A `speed` of `1` is the speed the drone has without any speed upgrades. A `speed` of `8` makes the code execute `8` times faster and corresponds to the speed of the drone after `3` speed upgrades. A `speed` of `0.5` makes the code execute at half of the speed without speed upgrades. This can be useful to see what the code is doing.

If `speed` is faster than the execution can currently go it will just go at max speed.

If `speed` is `0` or negative, the speed is changed back to max speed. The effect will also stop when the execution stops.

returns `None`

takes `200` ticks to execute.

example usage:

<div id="cb45" class="sourceCode">

``` sourceCode
set_execution_speed(1)
```

</div>

## `set_world_size(size)`

Limits the size of the farm to better see what's happening. Also clears the farm and resets the drone position. Sets the farm to a `size` x `size` grid. The smallest `size` possible is `3`. A `size` smaller than `3` will change the grid back to its full size. The effect will also stop when the execution stops.

returns `None`

takes `200` ticks to execute.

example usage:

<div id="cb46" class="sourceCode">

``` sourceCode
set_world_size(5)
```

</div>

## `simulate(filename, sim_unlocks, sim_items, sim_globals, seed, speedup)`

Starts a simulation for the leaderboard using the specified `filename` as a starting point.

`sim_unlocks`: A sequence containing the starting unlocks. `sim_items`: A dict mapping items to amounts. The simulation starts with these items. `sim_globals`: A dict mapping variable names to values. The simulation starts with these variables in the global scope. `seed`: The random seed of the simulation. Must be a positive integer. `speedup`: The starting speedup.

returns the time it took to run the simulation.

takes `200` ticks to execute.

example usage:

<div id="cb47" class="sourceCode">

``` sourceCode
filename = "f1"
sim_unlocks = Unlocks
sim_items = {Items.Carrot : 10000, Items.Hay : 50}
sim_globals = {"a" : 13}
seed = 0
speedup = 64

run_time = simulate(filename, sim_unlocks, sim_items, sim_globals, seed, speedup)
```

</div>

## `South`

The down direction on the screen. Unless you turn your screen around.

## `spawn_drone(function, *args)`

Spawns a new drone in the same position as the drone that ran the `spawn_drone(function, *args)` command. The new drone then begins executing the specified function. The rest of the arguments are copied and passed into the specified function. After the drone is done, it will disappear automatically.

returns the handle of the new drone or `None` if all drones are already spawned.

takes `200` ticks to execute if a drone was spawned, `1` otherwise.

example usage:

<div id="cb48" class="sourceCode">

``` sourceCode
def harvest_column(message):
    for _ in range(get_world_size()):
        harvest()
        move(North)
    print(message)

i = 0
while True:
    if spawn_drone(harvest_column, i):
        move(East)
        i = (i + 1) % 10
```

</div>

## `str(object)`

returns a string representation of `object`.

takes `1` ticks to execute.

example usage:

<div id="cb49" class="sourceCode">

``` sourceCode
string = str(1000)
```

</div>

## `swap(direction)`

Swaps the entity under the drone with the entity next to the drone in the specified `direction`. Doesn't work on all entities. Also works if one (or both) of the entities are `None`.

returns `True` if it succeeded, `False` otherwise.

takes `200` ticks to execute on success, `1` tick otherwise.

example usage:

<div id="cb50" class="sourceCode">

``` sourceCode
swap(North)
```

</div>

## `till()`

Tills the ground under the drone into `Grounds.Soil`. If it's already soil it will change the ground back to `Grounds.Grassland`.

returns `None`

takes `200` ticks to execute.

example usage:

<div id="cb51" class="sourceCode">

``` sourceCode
till()
```

</div>

## `True`

A boolean value that is always true.

## `unlock(unlock)`

Has exactly the same effect as clicking the button corresponding to `unlock` in the research tree.

returns `True` if the unlock was successful, `False` otherwise.

takes `200` ticks to execute if it succeeded, `1` tick otherwise.

example usage:

<div id="cb52" class="sourceCode">

``` sourceCode
unlock(Unlocks.Carrots)
```

</div>

## <a href="Unlocks" class="wikilink" title="Unlocks"><code>Unlocks</code></a>

Contains all the unlocks and upgrades in the research menu. Can be iterated with a `for` loop.

<div class="toccolours mw-collapsible mw-collapsed" expandtext="show values" collapsetext="hide values" style="max-width:32em">

`values`

<div class="mw-collapsible-content">

  
.Auto_Unlock

.Cactus

.Carrots

.Costs

.Debug

.Debug_2

.Dictionaries

.Dinosaurs

.Expand

.Expand_2

.Fertilizer

.Functions

.Grass

.Hats

.Import

.Leaderboard

.Lists

.Loops

.Mazes

.Megafarm

.Operators

.Plant

.Polyculture

.Pumpkins

.Senses

.Simulation

.Speed

.Sunflowers

.The_Farmers_Remains

.Timing

.Top_Hat

.Trees

.Utilities

.Variables

.Watering

</div>

</div>

## `use_item(item, n=1)`

Attempts to use the specified `item` `n` times. Can only be used with some items including `Items.Water`, `Items.Fertilizer`.

returns `True` if an item was used, `False` otherwise.

takes `200` ticks to execute if it succeeded, `1` tick otherwise.

example usage:

<div id="cb53" class="sourceCode">

``` sourceCode
use_item(Items.Fertilizer)
```

</div>

## `wait_for(drone)`

Waits until the given `drone` terminates.

returns the return value of the function that the `drone` was running.

takes `1` tick to execute if the awaited `drone` is already done.

example usage:

<div id="cb54" class="sourceCode">

``` sourceCode
def get_entity_type_in_direction(dir):
    move(dir)
    return get_entity_type()

def zero_arg_wrapper():
    return get_entity_type_in_direction(North)
handle = spawn_drone(zero_arg_wrapper)
print(wait_for(handle))
```

</div>

## `West`

The left direction on the screen. Unless you turn your screen around.

## `while`

Loops until the condition is false.
