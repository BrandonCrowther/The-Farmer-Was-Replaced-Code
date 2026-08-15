# Expand

> Mirrored from <https://thefarmerwasreplaced.wiki.gg/wiki/Expand>
> — CC BY-SA. Regenerate with `python3 tools/fetch_wiki.py`.

Your farm has grown! This space is not much use if you can't move the drone, so there is a new function `move()` that moves the drone. `move()` requires that you specify the direction in which you want the drone to move. There are four new constants for this: `North, East, South, West`

For example, `move(North)` will move the drone one square to the north.

If you move over the edge of the farm the drone will be moved to the other side of the farm. The following example code will keep moving the drone north and wrap back to the start when it reaches the edge of the farm:

<div id="cb1" class="sourceCode">

``` sourceCode
while True:
    move(North)
```

</div>

See also: <a href="Expand_2" class="wikilink" title="Expand 2">Expand 2</a>
