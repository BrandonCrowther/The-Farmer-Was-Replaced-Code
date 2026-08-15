# Reset

> Mirrored from <https://thefarmerwasreplaced.wiki.gg/wiki/Reset>
> — CC BY-SA. Regenerate with `python3 tools/fetch_wiki.py`.

### 

This page previously described a "golden piggy" prestige loop that has been removed from the game. It is replaced by the <a href="Leaderboard" class="wikilink" title="Leaderboard">Leaderboard</a>/<a href="Simulation" class="wikilink" title="Simulation">Simulation</a> system below.

`reset()` resets the farm back to a 1x1 square, removes all resources, and locks most unlocks. It does not remove any of your code.

<div id="cb1" class="sourceCode">

``` sourceCode
reset()
```

</div>

returns `None` and takes `200` ticks to execute.

Rather than a manual reset-for-reward loop, the current progression endgame is the <a href="Leaderboard" class="wikilink" title="Leaderboard">Leaderboard</a> system: `leaderboard_run(leaderboard, filename, speedup)` starts a timed, repeatable <a href="Simulation" class="wikilink" title="simulation">simulation</a> run from a fixed starting state (similar to what a "reset run" used to be), and successful runs are scored and ranked on the leaderboard. See <a href="Leaderboard" class="wikilink" title="Leaderboard">Leaderboard</a> and <a href="Simulation" class="wikilink" title="Simulation">Simulation</a> for details, including the `Leaderboards.Fastest_Reset` category which is the closest current equivalent to the old reset-loop challenge.

Remember that you can use `num_unlocked(unlock) > 0` to check if something is unlocked and you can use `get_cost()` on your unlocks to see what they cost so you can automate progress.
