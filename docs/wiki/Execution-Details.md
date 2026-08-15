# Execution Details

> Mirrored from <https://thefarmerwasreplaced.wiki.gg/wiki/Execution_Details>
> — CC BY-SA. Regenerate with `python3 tools/fetch_wiki.py`.

This page documents details about how the game executes instructions, which the game does not provide.

### The Base Operation Time is 2.5ms

This equates to 0.5 seconds for a 200-operation "action" such as `harvest` at the beginning of the game. This is equivalent to 400 ticks per second. All upgrades reduce this time by a factor of 1.5, so for example unlocking the Speed 1 upgrade means all ticks take 2/3 the normal time, or about 1.667ms. Having <a href="Sunflowers" class="wikilink" title="Sunflower">Sunflower</a> power doubles speed. In the table below while factors and ticks personcd are accurate, the length of a tick in milliseconds is approximate.

| Speed unlocks | Speed factor | Ticks per second | ms per tick (approx) |  |  |  |
|----|----|----|----|----|----|----|
| no power | with power | no power | with power | no power | with power |  |
| 0 | 1 | 2 | 400 | 800 | 2.500 | 1.250 |
| 1 | 1.5 | 3 | 600 | 1200 | 1.667 | 0.833 |
| 2 | 2.25 | 4.5 | 900 | 1800 | 1.111 | 0.556 |
| 3 | 3.375 | 6.75 | 1350 | 2700 | 0.741 | 0.370 |
| 4 | 5.0625 | 10.125 | 2025 | 4050 | 0.494 | 0.247 |
| 5 | 7.59375 | 15.1875 | 3037.5 | 6075 | 0.329 | 0.165 |

Speed with unlocks

### All Side-Effects Happen at the Start of the Function

For instance: When `harvest()` is called, the harvesting action happens immediately, then 200 operations of delay pass. When `plant()` is called, the entity is planted and then 200 ticks (during which the plant grows) pass. Similarly, when `get_time()` is called, the time is gotten immediately, and then 1 tick passes.

### Power is Burned Faster with More Speed Upgrades

1 <a href="Sunflowers" class="wikilink" title="Sunflower">Sunflower</a> power lasts 30 "actions," or 6000 total ticks. Since ticks pass at a constant rate, power is also consumed at a constant rate per drone, as long as code is executing. This rate is proportional to the speed factor which depends on how many speed upgrades you have, see the above table.

### Estimating Ticks

Some operations are free in the sense that they do not advance the tick counter, and thus take no time. Other operations take a variable amount of time depending on the arguments or whether it suceeded. This makes it quite dificult to estimate exactly how long a section of code will take. For instance, in the following code can you guess how many ticks the following code takes?

<div id="cb1" class="sourceCode">

``` sourceCode
my_list = list(range(20))
my_list.insert(3, 30)
```

</div>

The answer is 40. The order of operations is:

- `list` (Variable lookup, free)
- `range` (Variable lookup, free)
- `20` (Constant evaluation, free)
- `range()` (Function call, costing 1)
- `list()` (Function call, costing 21)
- `my_list =` (Assignment, free)
- `my_list` (Variable lookup, free)
- `insert` (Variable lookup, free)
- `.` (Method operator, free)
- `3` (Constant evaluation, free)
- `30` (Constant evaluation, free)
- `insert()` (Function call, costing 18)

Other interesting things to note: Unlike in early access statements like `if`, `else` and `while` do take one tick to execute, in addition to evaluating the condition, which might be as little as 0 for a simple variable lookup. This also means if-chaining is more efficient than using the `and`, `or` and `not` operators. See <a href="Operation_Costs" class="wikilink" title="Operation_Costs">Operation_Costs</a> for more concrete details.
