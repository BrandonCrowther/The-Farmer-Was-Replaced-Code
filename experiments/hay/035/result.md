# exp-035 — query-until-hit — result

**Outcome.** rejected

**Numbers.** 03:04.853 vs 02:52.32 · **+12.533 s (+7.3%)**

**Verdict.** Asking repeatedly for a favourable request made the run slower, not
faster, even though each ask costs 1 tick against the 200 a replant costs.

**Explanation — CORRECTED 2026-08-16 by 036.** The account below was wrong, and
is kept because the way it was wrong is the point.

*What I wrote:* that the preference rerolls on every call, so the companion we
satisfy is not the one in force at `harvest()`, and the skip forfeits the 160x
multiplier — a loss rather than a wash because more querying means more drift.

*What 036 measured:* `get_companion()` is **deterministic for a standing plant**
— 7,958 bracketed query pairs, zero changes in type or position. Nothing drifts,
no multiplier is forfeited, and 013 is unaffected.

*The actual fault:* this experiment was built on a mechanism that does not exist.
It queried repeatedly waiting for a different answer, and the answer cannot
change without a replant. So every pass ran the query loop to its cap and then
walked anyway — the walk it meant to avoid, plus the cap in wasted queries. That
is the +12.5 s, and it is a straightforward cost, not a subtle yield loss.

The root error is upstream, in 033: it saw the preference change across a reroll
and concluded the *query* was non-deterministic, when what changed it was the
replant. I built 035 on that reading without testing it. See `036/result.md`.

**Three failed attempts preceded this one**, all mine: a crash with 54 GB free
(so `Fatal error in GC` is not only OOM), a silently no-op `.replace()` that left
`QUERY_LIMIT` undefined and produced an in-game ERROR, and a wedged UI where a
code window swallowed Escape so `reload` could not open the pause menu. Only the
relaunch cleared the last one.
