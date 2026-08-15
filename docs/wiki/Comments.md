# Comments

> Mirrored from <https://thefarmerwasreplaced.wiki.gg/wiki/Comments>
> — CC BY-SA. Regenerate with `python3 tools/fetch_wiki.py`.

Comments are parts of the code that are ignored during execution. Comments can be added using `#`. Anything on the same line after the `#` is a comment and will be ignored.

<div id="cb1" class="sourceCode">

``` sourceCode
#this is a comment
```

</div>

This can be useful to add notes to the code, and also to temporarily disable parts of the code without deleting them.

Any comment on the line before a function definition will be interpreted as documentation for that function.

<div id="cb2" class="sourceCode">

``` sourceCode
#This function does nothing.
def f():
    pass
```

</div>

It will be part of the popup information that appears when you mouse over the function name.
