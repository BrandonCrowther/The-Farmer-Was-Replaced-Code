# Available Functions

> Mirrored from <https://thefarmerwasreplaced.wiki.gg/wiki/Available_Functions>
> — CC BY-SA. Regenerate with `python3 tools/fetch_wiki.py`.
> Also known as: Available functions.

## harvest()

Harvests the entity under the drone. If you harvest an entity that can't be harvested, it will be destroyed.

returns `True` if an entity was removed, `False` otherwise.

takes the time of **200** operations to execute if an entity was removed, **1** operation otherwise.

example usage:

<div id="cb1" class="sourceCode">

``` sourceCode
harvest()
```

</div>

## can_harvest()

Used to find out if plants are fully grown.

returns `True` if there is an entity under the drone that is ready to be harvested, `False` otherwise.

takes the time of **1** operation to execute.

example usage:

<div id="cb2" class="sourceCode">

``` sourceCode
if can_harvest():
    harvest()
```

</div>

## swap(direction)

Swaps the entity under the drone with the entity next to the drone in the specified `direction`. Doesn't work on all entities. Also works if one (or both) of the entities are `None`.

returns `None`

takes the time of **200** operations to execute.

example usage:

<div id="cb3" class="sourceCode">

``` sourceCode
swap(North)
```

</div>

## range()

Generates a sequence of numbers.

overloads: `range(end)` returns a sequence of numbers from `0` (inclusive) to `end` (exclusive). `range(start,end)` returns a sequence of numbers from `start` (inclusive) to `end` (exclusive). `range(start,end,step)` returns a sequence of numbers from `start` (inclusive) to `end` (exclusive) in steps of size `step`

takes the time of **1** operation to execute.

example usage:

<div id="cb4" class="sourceCode">

``` sourceCode
for i in range(10):
    print(i)

for i in range(2,6):
    print(i)

for i in range(10, 0, -1):
    print(i)
```

</div>

## plant(entity)

Plants the specified entity under the drone if it can be planted. Otherwise it just does nothing.

returns `True` if it succeeded, `False` otherwise.

takes the time of **200** operations to execute if it succeeded, **1** operation otherwise.

example usage:

<div id="cb5" class="sourceCode">

``` sourceCode
plant(Entities.Bush)
```

</div>

## move(direction)

Moves the drone into the specified `direction` by one tile. If the drone moves over the edge of the farm it wraps back to the other side of the farm.

`East` = right `West` = left `North` = up `South` = down

returns `True` if the drone has moved, `False` otherwise.

takes the time of **200** operations to execute if the drone has moved, **1** operation otherwise.

example usage:

<div id="cb6" class="sourceCode">

``` sourceCode
move(North)
```

</div>

## till()

Tills the ground under the drone into `Grounds.Soil`. If it's already soil it will change the ground back to `Grounds.Grassland`.

returns `None`

takes the time of **200** operations to execute.

example usage:

<div id="cb7" class="sourceCode">

``` sourceCode
till()
```

</div>

## get_pos_x()

Gets the current x position of the drone. The x position starts at `0` in the `West` and increases in the `East` direction.

returns a number representing the current x coordinate of the drone.

takes the time of **1** operation to execute.

example usage:

<div id="cb8" class="sourceCode">

``` sourceCode
x, y = get_pos_x(), get_pos_y()
```

</div>

## get_pos_y()

Gets the current y position of the drone. The y position starts at `0` in the `South` and increases in the `North` direction.

returns a number representing the current y coordinate of the drone.

takes the time of **1** operation to execute.

example usage:

<div id="cb9" class="sourceCode">

``` sourceCode
x, y = get_pos_x(), get_pos_y()
```

</div>

## get_world_size()

Get the current size of the farm.

returns the side length of the grid in the north to south direction.

takes the time of **1** operation to execute.

example usage:

<div id="cb10" class="sourceCode">

``` sourceCode
for i in range(get_world_size()):
    move(North)
```

</div>

## get_entity_type()

Find out what kind of entity is under the drone.

returns `None` if the tile is empty, otherwise returns the type of the entity under the drone.

takes the time of **1** operation to execute.

example usage:

<div id="cb11" class="sourceCode">

``` sourceCode
if get_entity_type() == Entities.Grass:
    harvest()
```

</div>

## get_ground_type()

Find out what kind of ground is under the drone.

returns the type of the ground under the drone.

takes the time of **1** operation to execute.

example usage:

<div id="cb12" class="sourceCode">

``` sourceCode
if get_ground_type() != Grounds.Soil:
    till()
```

</div>

## get_tick_count()

Used to measure the number of ticks performed.

returns the number of operations performed since the start of execution.

takes the time of **0** operations to execute.

example usage:

<div id="cb13" class="sourceCode">

``` sourceCode
do_something()

print(get_tick_count())
```

</div>

## get_time()

Get the current game time.

returns the time in seconds since the start of the game.

takes the time of **1** operation to execute.

example usage:

<div id="cb14" class="sourceCode">

``` sourceCode
start = get_time()

do_something()

time_passed = get_time() - start
```

</div>

## get_op_count()

Used to measure the number of operations performed.

returns the number of operations performed since the start of execution.

takes the time of **1** operation to execute.

example usage:

<div id="cb15" class="sourceCode">

``` sourceCode
do_something()

print(get_op_count())
```

</div>

This function has been removed from the game. See `get_tick_count()` above for a replacement.

== use_item(item, n=1) == Attempts to use the specified `item` `n` times. Can only be used with some items including `Items.Water_Tank`, `Items.Fertilizer` and `Items.Egg`.

returns `True` if an item was used, `False` otherwise.

takes the time of **200** operations to execute if it succeeded, **1** operation otherwise.

example usage:

<div id="cb16" class="sourceCode">

``` sourceCode
use_item(Items.Fertilizer)
```

</div>

## get_water()

Get the current water level under the drone.

returns the water level under the drone as a number between `0` and `1`.

takes the time of **1** operation to execute.

example usage:

<div id="cb17" class="sourceCode">

``` sourceCode
if get_water() < 0.5:
    use_item(Items.Water_Tank)
```

</div>

## do_a_flip()

Makes the drone do a flip! This action is not affected by speed upgrades.

returns `None`

takes 1s to execute.

example usage:

<div id="cb18" class="sourceCode">

``` sourceCode
while True:
    do_a_flip()
```

</div>

## print(something)

Prints something into the air above the drone using smoke. This action is not affected by speed upgrades. Multiple values can be printed at once.

returns `None`

takes 1s to execute.

example usage:

<div id="cb19" class="sourceCode">

``` sourceCode
print("ground:", get_ground_type())
```

</div>

## quick_print()

Prints a value just like `print()` but it doesn't stop to write it into the air so it can only be found on the output page.

returns `None`

takes the time of **1** operations to execute.

example usage:

<div id="cb20" class="sourceCode">

``` sourceCode
quick_print("hi mom")
```

</div>

## len(collection)

Get the number of elements in a list, set, dict or tuple.

returns the length of the `collection`.

takes the time of **1** operation to execute.

example usage:

<div id="cb21" class="sourceCode">

``` sourceCode
for i in range(len(list)):
    list[i] += 1
```

</div>

## num_items(item)

Find out how much of `item` you currently have.

returns the number of `item` currently in your inventory.

takes the time of **1** operation to execute.

example usage:

<div id="cb22" class="sourceCode">

``` sourceCode
if num_items(Items.Fertilizer) == 0:
    trade(Items.Fertilizer)
```

</div>

## get_cost(thing)

Gets the cost of a `thing`

If `thing` is an item get the cost of buying it when using `trade(item)`. If `thing` is an entity get the seed needed to plant it. If `thing` is an unlock get the cost of unlocking it. returns a dictionary with items as keys and numbers as values. Each item is mapped to how much of it is needed. returns `None` when used on an upgradeable unlock that is already at the max level.

takes the time of **1** operation to execute.

example usage:

<div id="cb23" class="sourceCode">

``` sourceCode
cost = get_cost(Unlocks.Carrots)
for item in cost:
    if num_items(item) < cost[item]:
        print("not enough items to unlock carrots")
```

</div>

## clear()

Removes everything from the farm, and moves the drone back to position `(0,0)`.

returns `None`

takes the time of **200** operations to execute.

example usage:

<div id="cb24" class="sourceCode">

``` sourceCode
clear()
```

</div>

## get_companion()

Get the companion preference of the plant under the drone.

returns a list of the form `[companion_type, companion_x_position, companion_y_position]`

takes the time of **1** operation to execute.

example usage:

<div id="cb25" class="sourceCode">

``` sourceCode
companion = get_companion()
if companion != None:
    print(companion)
```

</div>

## unlock(unlock)

Has exactly the same effect as clicking the button corresponding to `unlock` in the research tree.

returns `True` if the unlock was successful, `False` otherwise.

takes the time of **200** operations to execute if it succeeded, **1** operation otherwise.

example usage:

<div id="cb26" class="sourceCode">

``` sourceCode
unlock(Unlocks.Carrots)
```

</div>

## num_unlocked(thing)

Used to check if an unlock, entity, ground or item is already unlocked.

returns `1` plus the number of times `thing` has been upgraded if `thing` is upgradable. Otherwise returns `1` if `thing` is unlocked, `0` otherwise.

takes the time of **1** operation to execute.

example usage:

<div id="cb27" class="sourceCode">

``` sourceCode
if num_unlocked(Unlocks.Multi_Trade) > 0:
    trade(Items.Carrot_Seed, 10)
else:
    for i in range(10):
        trade(Items.Carrot_Seed)
```

</div>

## timed_reset()

Starts a timed run for the leaderboard. Saves the game before the run and then loads that save afterwards so you can't gain any items during the run.

returns `None`

takes the time of **200** operations to execute.

example usage:

<div id="cb28" class="sourceCode">

``` sourceCode
timed_reset()
```

</div>

## measure()

Can measure some values on some entities. The effect of this depends on the entity.

overloads: `measure()` measures the entity under the drone. `measure(direction)` measures the neighboring entity in the `direction` of the drone.

returns the number of petals of a sunflower. returns the next position for a treasure or apple. returns the size of a cactus. returns a mysterious number for a pumpkin. returns `None` for all other entities.

takes the time of **1** operation to execute.

example usage:

<div id="cb29" class="sourceCode">

``` sourceCode
num_petals = measure()
```

</div>

## min(a,b)

Gets the minimum of a sequence of elements or several passed arguments. Can be used on numbers and strings.

overloads: `min(a,b,c)`: Returns the minimum of the passed arguments. `min(sequence)`: Returns the minimum of all values in a sequence.

execution time depends on the input.

<div id="cb30" class="sourceCode">

``` sourceCode
example usage:
min([3,6,34,16])
```

</div>

## max(a,b)

Gets the maximum of a sequence of elements or several passed arguments. Can be used on numbers and strings.

overloads: `max(a,b,c)`: Returns the maximum of the passed arguments. `max(sequence)`: Returns the maximum of all values in a sequence.

takes the time of \#comparisons *\[sic\]* operations to execute.

example usage:

<div id="cb31" class="sourceCode">

``` sourceCode
max([3,6,34,16])
```

</div>

## abs(number)

Computes the absolute value of a `number`.

returns `number` if `number` is positive, `-number` otherwise.

takes the time of \#comparisons *\[sic\]* operations to execute.

example usage:

<div id="cb32" class="sourceCode">

``` sourceCode
abs(-69)
```

</div>

## random()

Samples a random number between 0 (inclusive) and 1 (exclusive).

returns the random number.

takes the time of **1** operations to execute.

example usage:

<div id="cb33" class="sourceCode">

``` sourceCode
def random_elem(list):
    index = random() * len(list) // 1
    return list[index]
```

</div>

## list()

Creates a new list.

overloads: `list(collection)`: Creates a list with the elements of an existing list, set, dict or tuple.

returns a list.

takes the time of `1 + len(collection)` operations to execute.

example usage:

<div id="cb34" class="sourceCode">

``` sourceCode
new_list = list((1,2,3))
```

</div>

## set()

Creates a new set.

overloads: `set(collection)`: Creates a set with the elements of an existing list, set, dict or tuple.

returns a set.

takes the time of `1 + len(collection)` operations to execute.

example usage:

<div id="cb35" class="sourceCode">

``` sourceCode
new_set = set((1,2,3))
```

</div>

## dict()

Creates a new empty dictionary.

returns an empty dictionary.

takes the time of **1** operation to execute.

example usage:

<div id="cb36" class="sourceCode">

``` sourceCode
new_dict = dict()
```

</div>

## set_execution_speed(speed)

Limits the speed at which the program is executed to better see what's happening.

A `speed` of `1` is the speed the drone has without any speed upgrades. A `speed` of `10` makes the code execute 10 times faster and corresponds to the speed of the drone after 9 speed upgrades. A `speed` of `0.5` makes the code execute at half of the speed without speed upgrades. This can be useful to see what the code is doing.

If `speed` is faster than the execution can currently go it will just go at max speed.

If `speed` is `0` or negative, the speed is changed back to max speed. The effect will also stop when the execution stops.

returns `None`

takes the time of **200** operations to execute.

example usage:

<div id="cb37" class="sourceCode">

``` sourceCode
set_execution_speed(1)
```

</div>

## set_farm_size(size)

Limits the size of the farm to better see what's happening. Also clears the farm. Sets the farm to a `size` x `size` grid. The smallest `size` possible is `3`. A `size` smaller than `3` will change the grid back to its full size. The effect will also stop when the execution stops.

returns `None`

takes the time of **200** operations to execute.

example usage:

<div id="cb38" class="sourceCode">

``` sourceCode
set_farm_size(5)
```

</div>
