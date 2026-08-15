# Name Scopes

> Mirrored from <https://thefarmerwasreplaced.wiki.gg/wiki/Name_Scopes>
> — CC BY-SA. Regenerate with `python3 tools/fetch_wiki.py`.
> Also known as: Name scopes.

Scopes determine which variables can be accessed from where. They function differently than in Python.

Just like Python, there is a global scope, and each function has a local scope. When you define a variable, it gets added to the current scope. Anything outside of a function definition is considered part of the global scope.

<div id="cb1" class="sourceCode">

``` sourceCode
# Assigns a value of 1 to the variable x in the global scope.
x = 1

# Assigns a function to the variable f in the global scope.
def f():
    # Assigns a value of 1 to the variable y in the local scope of f.
    y = 1

    # Assigns a function to the variable g in the local scope of f.
    def g():
        pass

# Retrieves the function stored in f from the global scope.
f()

# y was never declared in the global scope so we can't read
# it here.
# It only exists in the local scope of f.
# This throws an error.
print(y)
```

</div>

Loops and branches do not create their own scopes, so anything declared within them can still be used outside.

<div id="cb2" class="sourceCode">

``` sourceCode
for i in range(3):
    pass

# This will print 2 because the for loop assigned 2 to i.
print(i)
```

</div>

Any functions defined in loaded files will be added to the global scope before execution, so you can use functions declared in other files. Note that global variables are only available when the line where they are assigned is actually executed. Only the global scope of the window on which you click the execute button will be executed.

Variables from the global scope can be read anywhere, but when assigned, they will always go into the current scope.

<div id="cb3" class="sourceCode">

``` sourceCode
x = 1

def f():
    x += 1

f()

print(x)
```

</div>

This code prints `1` not `2` because `x += 1` will first read `1` from the global variable `x` and then assign `2` to a new local variable that is also called `x`. So the global variable `x` is never changed.

This behavior differs slightly from that of Python. Python throws an error here because you are trying to read from a local variable before it is assigned.

In Python it is also possible to use the 'global' keyword to declare that you want to use the global variable instead of the local one, but this is not supported in this game.

They use reference semantics, which means that the variable holds a reference to the underlying dictionary, rather than storing the data structure directly in the variable. A global variable can store a reference to a dictionary that can be read in a function. You can modify the underlying dictionary without updating the variable in the global scope. Since the variable in the global scope still points to the same dictionary, it will also reflect any changes made to that dictionary. To illustrate, consider the following code:

<div id="cb4" class="sourceCode">

``` sourceCode
# Assign dictionary in global scope
d = {"x": 1}

def f():
    # make a change to the dictionary that is referenced by d.
    d["x"] += 1

# prints 2
print(d["x"])
```

</div>
