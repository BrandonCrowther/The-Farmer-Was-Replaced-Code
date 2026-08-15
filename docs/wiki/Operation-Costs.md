# Operation Costs

> Mirrored from <https://thefarmerwasreplaced.wiki.gg/wiki/Operation_Costs>
> — CC BY-SA. Regenerate with `python3 tools/fetch_wiki.py`.

Note: The following table only includes the cost of the operation itself; not any of its operands. The cost of the operands must be included. For example:

- `return 27 + len([1,2,3])` costs 5 ticks, as `return` costs 0, its operand `27 + len(..)` costs 1 from the `+` and 0 from the literal `27`, 3 ticks for constructing the list and 1 more from `len()`.

| Operation | Cost (ticks) |
|----|----|
| Any simple literal (`1`, `True`, `North`, etc) | Free |
| Any string literal (`"abcde"`) | Free |
| Any empty (zero length) list, tuple, set, or dict literal | 1 |
| Any tuple literal | 1 + the cost of each item |
| Any list or dict literal | Number of items in the literal + the cost of each item |
| Any dict literal | 1 + Number of items in the literal + the cost of each item |
| Variable assignment | Free |
| Variable lookup | Free |
| Any of `+` `-` `*` `/` `//` `%` `**` `and` `or` (Excluding concatenation, see below.) | 1 |
| Unary `+` or `-`, or `not` | Free |
| Any of `pass` `def` | 1 |
| Any of `break` `continue` `return` | Free |
| Length of any collection (`len(list_or_tuple_or_dict_set)`) | 1 |
| List or tuple indexing (`list_or_tuple[index]`) | 1 |
| Dictionary lookup (`dictionary[key]`) or (`key in dictionary`), where key is a number | 1 |
| Dictionary lookup (`dictionary[key]`), where key is a string | max(len(key) // 8, 1) |
| Dictionary lookup (`dictionary[key]`) or (`key in dictionary`), where key is a tuple | Sum of the cost of looking up each item in `key` recursively. |
| Set lookup (`key in set`) | Depends on type of `key`. Same as dictionary lookup, above |
| Getter functions (`get_pos_x()`, `can_harvest()`, `measure()`, `get_time()`, etc) | 1 |
| Successful operating function (`move()`, `clear()`, `swap()`, etc) | 200 |
| Failed fallible operating functions (`move()`, `harvest()`, `use_item()`, etc) | 1 |
| Any of `==` `>=` `<=` `>` `<` `!=` | See <a href="#Comparisons" class="wikilink" title="comparisons">comparisons</a> section |
| `min()` or `max()` | See <a href="#Comparisons" class="wikilink" title="comparisons">comparisons</a> section |
| Concatenation (`+`) on lists, strings, or tuples | `len(arg1)` + `len(arg2)` |
| `in` on list or tuple where item exists | 1 + `indexof(item)` |
| `in` on list or tuple where item doesn't exist | 1 + `len(list_or_tuple)` |
| List slicing (`lst[from:to:step]` or `lst[from:to]`) | 1 + `len(result_of_slice)` |
| `.insert()` | 1 + `len(tuple_or_list)` - `insertion_index` |
| `.remove()` | `len(list)` |
| `set()` or `list()` with one argument | 1 + `len(arg)` |
| Calling a user defiend function by its `def`'ed name | Free + the cost of the code in the function body |
| Calling a user defined function indirectly via a variable | 1 + the cost of the code in the function body |
| Calling a builtin function indirectly via a variable | Exactly the same cost as calling the function directly |
| Entering a `for` loop | 1 |
| Entering a `while condition` loop | 1 + cost of `condition` |
| `if condition` or `elif condition` | 1 + cost of `condition` |
| else | Free |
|  |  |

## Fixed time operations

Some operations are unaffected by the speed factor, and always take the same amount of time.

| Operation          | Cost (seconds) |
|--------------------|----------------|
| `do_a_flip()`      | 1 second       |
| `print()`          | 1 second       |
| `quick_print()`    | 0 seconds      |
| `get_tick_count()` | 0 seconds      |

## Comparisons

Comparison costs are surprisingly complicated in this game. The following are the rules to comparison, where `a` and `b` are the arguments:

1.  `a` and `b` are different types: 1 tick
2.  both are numbers, enums (`North`, `Items`, etc): 1 tick
3.  both are sets: 1 tick
4.  both are lists or tuples, and they have different lengths: 1 tick
5.  both are lists or tuples, but same length: 1 + sum of ops of comparing all elements up to and including the first different element.
6.  both are dictionaries: I don't actually know, if you know, edit this wiki!

Examples:

- Comparing `(1, (2, 3), 4)` and `(1, (2, 3), 5)`
  - They are both tuples, of length 3. Thus, use rule 5. Their first different element the last element, so it's the sum of all element costs. The first elements are both numbers, so 1 op; the second is a tuple, with 2 elements, all the same, so 1 + 2 ticks; the third is another number, so 1 tick. This totals to 5 ticks, add 1 for tuple itself, to get 6 ticks.

## Function calls

Calling user defined function cost zero ticks, only the function body costs any ticks.

<div id="cb1" class="sourceCode">

``` sourceCode
def func():
    pass # 1 tick

func() # Takes 1 tick, only for the function body
```

</div>

Calling any function indrectly via a variable cost 1 more tick. Using the above example.

<div id="cb2" class="sourceCode">

``` sourceCode
func_variable = func
r = func_variable() # Now takes 2 ticks, 1 for the indirection, 1 for the `pass` function body
```

</div>

Binding builtin functions to variaibles does not increase the cost.

<div id="cb3" class="sourceCode">

``` sourceCode
builtin_func_var = harvest
r = builtin_func_var() # Takes 200 ticks
```

</div>

## Acknowledgements

Note: Some information transcribed from 2024/8/23. Credit: [kit !!](https://discord.com/users/963434203402358834) from discord. [original message](https://discord.com/channels/988081966035402783/1276266294416637962/1276325129193787525). Since updated to version 1.0.
