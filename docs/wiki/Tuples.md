# Tuples

> Mirrored from <https://thefarmerwasreplaced.wiki.gg/wiki/Tuples>
> — CC BY-SA. Regenerate with `python3 tools/fetch_wiki.py`.

Tuples are a great way to combine multiple values into a single value. To create a tuple, just separate the values with commas:

<div id="cb1" class="sourceCode">

``` sourceCode
tuple = 1, 2
```

</div>

You can also unpack them into several variables again. In the code below, the `tuple (1,2)` is unpacked into two variables `a` and `b`.

<div id="cb2" class="sourceCode">

``` sourceCode
a, b = 1, 2
```

</div>

Tuples can be indexed like lists, but they are immutable and cannot be changed after creation.

<div id="cb3" class="sourceCode">

``` sourceCode
tuple = 1, 2

# prints 2
print(tuple[1])

# throws an error
tuple[0] = 3
```

</div>

Unlike lists tuples can be used as keys in dictionaries.

<div id="cb4" class="sourceCode">

``` sourceCode
d = {(1,2):(4,5)}

# prints (4,5)
print(d[(1,2)])
```

</div>

They can also be useful for returning several values in a function.

<div id="cb5" class="sourceCode">

``` sourceCode
def f():
    return 1, 2

a, b = f()
```

</div>
