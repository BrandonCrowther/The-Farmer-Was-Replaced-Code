# Debug

> Mirrored from <https://thefarmerwasreplaced.wiki.gg/wiki/Debug>
> — CC BY-SA. Regenerate with `python3 tools/fetch_wiki.py`.

Sometimes your code just doesn't work and you need to find out why. There are couple of tools to help you do that.

The first is to execute the program step by step. You can go into step by step mode with the button next to the Execute button or by setting a breakpoint.

Breakpoints can be added by clicking on the breakpoint panel to the left of the code.

<figure>
<img src="Breakpoints.png" />
</figure>

When execution reaches the line where the breakpoint is, it will automatically switch to step-by-step mode.

When you move your mouse over a variable, its current value is displayed.

The `print()` function can also be very useful. It will write any value passed into it directly into the air.

Examples:

Print "0.24".

<div id="cb1" class="sourceCode">

``` sourceCode
print(0.24)
```

</div>

Print "True" or "False".

<div id="cb2" class="sourceCode">

``` sourceCode
print(can_harvest())
```

</div>

Print the current position.

<div id="cb3" class="sourceCode">

``` sourceCode
print(get_pos_x(), get_pos_y())
```

</div>

The print function prints the value directly into the air and to the Output page.

<span class="toccolours" style="font-size:105%;padding:0.33em"><a href="Output" class="wikilink" title="Output">Output</a></span>

Writing into the air can sometimes be a bit slow if you want to print a lot of values. In this case you can use the `quick_print()` function which prints only to the output window.

The output window also logs warnings and errors so if something isn't working as expected it can be useful to check that.

### Debug 2

When your drone gets too fast and the grid too big it can be hard to see what's going on anymore.

For this reason there are the `set_execution_speed()` and `set_world_size()` functions. They allow you to reduce the execution speed and the farm size.

The farm size and the execution speed will be reset to the default values at the end of the execution
