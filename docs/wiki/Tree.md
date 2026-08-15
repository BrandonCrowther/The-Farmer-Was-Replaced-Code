# Tree

> Mirrored from <https://thefarmerwasreplaced.wiki.gg/wiki/Tree>
> — CC BY-SA. Regenerate with `python3 tools/fetch_wiki.py`.

Trees are a better way of getting wood than bushes. They yield 5 wood each. Just like bushes they can be planted on grass or soil.

Trees like to have some space and planting them right next to each other will slow down their growth. The grow time will double for every tree that is on one of the tiles directly to the `North`, `East`, `West` or `South` of it. So if you plant trees on every tile they will take `2*2*2*2 = 16` times longer to grow.

<div class="mw-collapsible mw-collapsed" expandtext="show hint" collapsetext="hide hint" style="border:black solid 1px;padding:0 1em">

hint

<div class="mw-collapsible-content">

The `%` operator may be useful here. Remember the `%` operator returns the remainder of the division. Even numbers divided by `2` have a remainder of `0` and odd numbers divided by `2` have a remainder of `1`. So you can check if a number is even like this:

<div id="cb1" class="sourceCode">

``` sourceCode
def is_even(n):
    return n % 2 == 0
```

</div>

This returns `True` if n is even and `False` if it isn't.

</div>

</div>
