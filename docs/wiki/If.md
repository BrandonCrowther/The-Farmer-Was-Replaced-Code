# If

> Mirrored from <https://thefarmerwasreplaced.wiki.gg/wiki/If>
> — CC BY-SA. Regenerate with `python3 tools/fetch_wiki.py`.

The execution speed has been doubled. The problem is that the drone now harvests faster than the grass can grow resulting in no harvest at all. To deal with this if branches and the `can_harvest()` function are unlocked now.

### Checking Before Harvesting

So far we only had `True` and `False` as conditions, which is of course not very useful with `if`.

The new function can_harvest() offers a better condition. `can_harvest()` returns `True` if the plant under the drone can be harvested and `False` otherwise.

<div id="cb1" class="sourceCode">

``` sourceCode
if can_harvest():
    #do something
```

</div>

The reason you can use this function as a condition like this is because it returns a boolean value.

A return value essentially means that after executing the functionality the function call expression takes on the returned value.

What happens when the above code gets executed:

  
\- the if runs

\- `can_harvest()` is called

\- `can_harvest()` does it's thing

\- `can_harvest()` returns `True` or `False`

\- the statement is now `if True:` or `if False:`

\- the code block is only executed if it can harvest

So we can now use `if` to prevent the drone from harvesting too early.
