# Lists

> Mirrored from <https://thefarmerwasreplaced.wiki.gg/wiki/Lists>
> — CC BY-SA. Regenerate with `python3 tools/fetch_wiki.py`.

Lists are an easy way to store several values in a single variable. You can create new lists like this:

<div id="cb1" class="sourceCode">

``` sourceCode
list = [2, True, Items.Hay]
```

</div>

The list now holds the values `2`, `True` and `Items.Hay`. A list can also be empty if there are 0 elements in it:

<div id="cb2" class="sourceCode">

``` sourceCode
empty_list = []
```

</div>

You can access an element of a list by its index. The index is `0` for the first element, `1` for the second element, `2` for the third...

<div id="cb3" class="sourceCode">

``` sourceCode
entities = [Entities.Tree, Entities.Carrot, Entities.Pumpkin]
plant(entities[1])
```

</div>

You can iterate over a list using a for loop. The following example sums the<sup>sic</sup> all elements in the list.

<div id="cb4" class="sourceCode">

``` sourceCode
numbers = [4, 7, 2, 5]
sum = 0
for number in numbers:
    sum += number
```

</div>

`sum` is now `18`

The following list methods allow you to add and remove elements:

`elements.append(elem)` adds an element to the end of the list:

<div id="cb5" class="sourceCode">

``` sourceCode
numbers = [2, 6, 12]
numbers.append(7)
```

</div>

`numbers` is now `[2, 6, 12, 7]` `elements.remove(elem)` removes the first occurrence of an element from a list:

<div id="cb6" class="sourceCode">

``` sourceCode
numbers = [1, 2, 4, 2]
numbers.remove(2)
```

</div>

`numbers` is now `[1, 4, 2]` `elements.insert(index, elem)` inserts an element at the given index:

<div id="cb7" class="sourceCode">

``` sourceCode
some_list = [Entities.Tree, Items.Hay]
some_list.insert(1, Items.Wood)
```

</div>

`some_list` is now `[Entities.Tree, Items.Woord, Items.Hay]` `elements.pop(index)` removes the element at a specified index. If no index is specified, the last item is removed.

<div id="cb8" class="sourceCode">

``` sourceCode
numbers = [3, 5, 8, 25]
numbers.pop()
```

</div>

`numbers` is now `[3, 5, 8]`

<div id="cb9" class="sourceCode">

``` sourceCode
numbers.pop(1)
```

</div>

`numbers` is now `[3, 8]`

The `len()` function returns the length of the list.

<div id="cb10" class="sourceCode">

``` sourceCode
numbers = [3, 2, 1]
x = len(numbers)
```

</div>

`x` is now `3` Lists have reference semantics. This means that assigning a list to a variable assigns the same list object to that variable, rather than making a copy of the list. If two variables reference the same list changes to the list will be seen by both.

<div id="cb11" class="sourceCode">

``` sourceCode
a = [1,2]
b = a
b.pop()
```

</div>

`a` and `b` are now both `[1]`
