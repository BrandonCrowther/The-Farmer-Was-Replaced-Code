# Variables

> Mirrored from <https://thefarmerwasreplaced.wiki.gg/wiki/Variables>
> — CC BY-SA. Regenerate with `python3 tools/fetch_wiki.py`.

Variables can be thought of as named containers that can hold a value. The `=` operator is used to declare a variable and store a value in it.

<div id="cb1" class="sourceCode">

``` sourceCode
variable_name = value
```

</div>

The left hand side of the operator is the variable name. You can give it any name you want. The right hand side is an expression whose resulting value will be stored in the variable.

Declare a variable named `a` and store the value `5` in it:

<div id="cb2" class="sourceCode">

``` sourceCode
a = 5
```

</div>

Declare a variable named `b` and store the return value if `can_harvest()` in it:

<div id="cb3" class="sourceCode">

``` sourceCode
b = can_harvest()
```

</div>

Do not confuse the `=` operator with the `==` operator. The `==` operator checks if two values are equal and returns `True` or `False`. The `=` operator assigns the value on the right to the name on the left.

After a variable has been assigned you can use it in the code to retrieve the value it contains

<div id="cb4" class="sourceCode">

``` sourceCode
a = 5
for i in range(a):
    do_a_flip()
```

</div>

The above loop executes 5 times because `a` is set to `5`. The `i` in the `for` loop is also a variable that is automatically assigned the current value of the sequence at each iteration of the loop. (it doesn't have to be called `i`, you can give it any valid variable name.)

Variables also let you do the same thing with a while loop:

<div id="cb5" class="sourceCode">

``` sourceCode
a = 5
i = 0
while i < a:
    do_a_flip()
    i = i + 1
```

</div>

This does the same thing as the for loop above. We just have to manually increment i. Note how to increment i we set it to be it's own value plus `1`. Changing the value of a variable based on it's previous value is something very common. It can be shortened using these operators: `+=, -=, *=, /=, %=`

`i = i + 1` is the same as `i += 1` `a = a / 3` is the same as `a /= 3`
