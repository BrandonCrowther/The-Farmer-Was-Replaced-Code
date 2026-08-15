# Differences from python

> Mirrored from <https://thefarmerwasreplaced.wiki.gg/wiki/Differences_from_python>
> — CC BY-SA. Regenerate with `python3 tools/fetch_wiki.py`.

While the game's langauge is very similar to python there are a number of differnces.

## Missing features

The game doesn't use a full python interpreter, it implements its own interpreter that lacks certain features. Notable missing features include

- All methods on lists other than append, pop and remove.
- All methods on dictionaries other than pop.
- All methods on sets other than add and remove.
- All methods on strings and numbers.
- Classes.
- Lambdas.
- The `int(x)` function (use `x // 1` if you need to floor).
- `async`/`await`.
- Named arguments.
- `*args` and `**kwargs`.
- List comprehension.
- Ternary operator (`a if condition else b`).

For the missing functions and methods, you can always implement your own function in the game that does the same thing.

## Changes from python

Some existing features behave slightly differently to python:

- All numbers are floats, not integers, and as such arithmetic involving fractions can result in inexact answers.
- Default paramters "bind on call", rather than on defintion.

<div id="cb1" class="sourceCode">

``` sourceCode
def print_pos(x = get_pos_x(), y = get_pos_y):
    print(x, y)
move(North)
print_pos() # Python: Always prints the postion at function defintion
            # Game:   Prints the current position
```

</div>

- `a, b += tuple`, creates a new tuple with `(a, b)` at the end.
- Rounding of indexes to lists, `lst[1.2]` is valid in game and is the same as `lst[1]`.
- Ranges with fractional bounds and/or step (unless that one was removed), e.g. `range(0, 1, 0.1)`.
- The ability to call `foo(x, y)` as `x.foo(y)`.
- `print(x)` prints in smoke, not to standard output, use `quick_print(x)` to print to `output.txt`.
