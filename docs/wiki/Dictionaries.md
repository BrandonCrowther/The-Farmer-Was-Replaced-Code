# Dictionaries

> Mirrored from <https://thefarmerwasreplaced.wiki.gg/wiki/Dictionaries>
> — CC BY-SA. Regenerate with `python3 tools/fetch_wiki.py`.

Dictionaries are a datastructure that allows you to map keys to values in the way that a real dictionary maps words to their definition and you can look them up very quickly.

A dictionary can be created like this: `rotation = {North:East, East:South, South:West, West:North}`

The expression before the colon is the key and the expression after the colon is the value the key maps to. The dictionary above maps directions to the direction to their right.

Accessing the value mapped to a key can be done similarly to accessing an element in a list: `value = dict[key]`

Example: `orientation = rotation[South]` This sets orientation to `West`.

You can add a new key value pair to a dictionary like this: `dict[key] = value` This will map the key to the value.

Keys are unique so adding a key that is already in the dictionary will override the previous value.

Use `dict.pop(key)` to remove a key value pair from `dict`.

<div id="cb1" class="sourceCode">

``` sourceCode
key in dict
```

</div>

evaluates to `True` if `key` is a key in the `dict` and `False` otherwise. So you can use

<div id="cb2" class="sourceCode">

``` sourceCode
if key in dict:
```

</div>

to check if `dict` contains the key.

Putting a dictionary into a for loop allows you to iterate through all keys:

<div id="cb3" class="sourceCode">

``` sourceCode
for key in dict:
    value = dict[key]
```

</div>

There are no guarantees for the order in which the keys will be iterated.

Sets are like dictionaries but without values. You only have a set of keys.

They are created similar to dictionaries just without values. `set = {North, East, West}`

Use `set.add(elem)` to add a new element to the set.

Use `set.remove(elem)` to remove an element from a set.

Use

<div id="cb4" class="sourceCode">

``` sourceCode
if elem in set:
```

</div>

to check if the set contains an element.

Use

<div id="cb5" class="sourceCode">

``` sourceCode
for elem in set:
```

</div>

to iterate all elements in the set.

Just like dictionaries sets are unordered so there are no guarantees for the order in which the elements are iterated.

Also elements in sets are unique so adding an element to a set that is already in it will not change the set.
