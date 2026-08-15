# While

> Mirrored from <https://thefarmerwasreplaced.wiki.gg/wiki/While>
> — CC BY-SA. Regenerate with `python3 tools/fetch_wiki.py`.

You have unlocked the `while` loop and the values `True` and `False`. The `while` loop keeps executing the loop body as long as the condition is `True`.

<div id="cb1" class="sourceCode">

``` sourceCode
while condition:
    #loop body
```

</div>

Don't worry about creating infinite loops. The delays in the execution will prevent the program from freezing.

### For Beginners

Perhaps you already tried putting several `harvest()` calls in a row:

<div id="cb2" class="sourceCode">

``` sourceCode
harvest()
harvest()
harvest()
```

</div>

This will allow you to harvest several times in one program execution. However it would be nice to keep harvesting more than three times and writing the same code several times is bad practice. The solution is a loop. A loop allows you to execute the same lines of code several times.

The while loop takes a condition which is a logic value that can only be in one of two states: `True` or `False`. Such a value is called a Boolean value.

The loop then executes the code inside the loop until the condition is False. The while loop looks like this:

<div id="cb3" class="sourceCode">

``` sourceCode
while condition:
    #loop body
    #loop body
    #...
```

</div>

Where you have to replace "condition" with a boolean value and `#loop body` with whatever you want to execute in the loop.

There are two constant boolean values available. Constants are values that never change during the program.

To create a constant boolean value that is always `True` you can just write `True`. Write `False` as a constant boolean value that will always be `False`. So you could either write

<div id="cb4" class="sourceCode">

``` sourceCode
while False:
    do_a_flip()
```

</div>

or

<div id="cb5" class="sourceCode">

``` sourceCode
while True:
    do_a_flip()
```

</div>

The first one will never do a flip and the second one will keep doing flips for ever (An infinite loop).

Usually creating an infinite loop is a bad idea because it will freeze the program, but in this game there are delays between every iteration of the loop, so it will cause the drone to keep doing a flip until you manually stop it by pressing the execute button again.

Note how the line after the colon is indented. Indentation like this is used to separate blocks of code. Just press Tab to add indentation and Shift + Tab (or Backspace) to remove it.

The loop will repeat all indented statements after the colon. Statements after the indented block will execute after the loop has finished.
