# API reference (authoritative)

`__builtins__.py` here is a snapshot of the file the game generates into the save
folder. It is the **ground truth** for function signatures, enum members, tick
costs and semantics, because it is emitted by the running game at this version and
this unlock state. The wiki mirror in `../wiki/` is conceptual/tutorial material and
lags the game.

Refresh after a game update or a new unlock:

```sh
cp save/Save0/__builtins__.py docs/api/__builtins__.py
git diff docs/api/__builtins__.py   # shows exactly what the update changed
```

The copy under `save/Save0/` is gitignored on purpose — it is game-owned and gets
rewritten, so only this reviewed snapshot is tracked.

## Things worth knowing that the signatures alone don't tell you

- `simulate(filename, unlocks, items, globals, seed, speedup) -> float` **returns
  the run time**. That return value is the measurement channel for experiments —
  no save file parsing, no stopwatch.
- `leaderboard_run(leaderboard, file_name, speedup) -> None` returns nothing; the
  result only appears on screen, so timed runs must be read visually.
- `quick_print()` costs 0 ticks and writes to the output page; `print()` costs 1
  second of drone time. Instrumentation must use `quick_print`.
- `import` is ignored by the game engine — it exists for editor tooling only. Names
  from other files resolve at run time regardless.
