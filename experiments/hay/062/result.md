# exp-062 — checking two exploit-adjacent candidates — result

**Outcome.** Both candidates closed. Neither is a live mechanism/gap in
the current game version.

**(a) Direct Hay tradeability.** `get_cost(Items.Hay)` errored live:
`"The 1. argument of get_cost() was Items.Hay. This is not a valid
argument."` — confirmed against `docs/api/__builtins__.py`: `get_cost()`
only accepts an `Entity`/`Entities` or `Unlock`/`Unlocks`, never a bare
`Item`. There is also no `trade()`/`sell()`/`buy()` function anywhere in
the builtin API. "Trade Hay directly" isn't a mechanism that exists in
this game at all — the candidate was based on a false premise, not a
closed door on a real one.

**(b) Module-function-call cost gap.** Real tick deltas, r1:

| call shape | ticks | expected |
| --- | --- | --- |
| local fn, direct (`inline_move_east()`, body = `move(East)`) | 200 | 200 (free + body) |
| raw builtin (`move(West)`) | 200 | 200 |
| `Common.move_to(...)`, direct by def-name | 228 | body cost (move + getters/comparisons in the wrapper) |
| `Common.move_to(...)`, direct by def-name (2nd call) | 228 | matches |
| local fn, indirect via variable | 201 | 200 + 1 (documented rule) — matches exactly |
| `Common.move_to`, indirect via variable | 229 | 228 + 1 — matches exactly |

The +28 over a bare `move()` on `Common.move_to` is real, accounted-for
work — the wrapper calls `get_pos_x()`/`get_pos_y()` and does comparisons
before its single `move()` — not a discount or a gap. The indirect-via-
variable premium is exactly the documented +1 tick, identically for both
the local function and the imported-module function. No accounting gap
between local and imported-module calls, direct or indirect.

**Verdict.** Neither candidate is real. Closes both without needing a
target-gated full run — a plain diagnostic print was decisive.
`get_cost`/tradeability was a wrong premise about the API surface, not a
finding about the game. The module-call tick costs match
Operation-Costs.md's documented rules exactly for the imported-module
case too, so there's no residual version of the patched "free function
calls in dynamic modules" exploit reachable through ordinary Python-level
indirection (def-name vs variable). Remaining brainstorm directions for
the user: residual RNG predictability under a specific trigger condition,
or deliberate exploitation of the already-documented drone-concurrency
race (050) — neither has been probed yet. No champion change;
`saves/hay/main.py` here was a probe only, not proposed for adoption.
