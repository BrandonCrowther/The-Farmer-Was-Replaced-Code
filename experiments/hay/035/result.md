# exp-035 — query-until-hit — result

**Outcome.** rejected

**Numbers.** 03:04.853 vs 02:52.32 · **+12.533 s (+7.3%)**

**Verdict.** Asking repeatedly for a favourable request made the run slower, not
faster, even though each ask costs 1 tick against the 200 a replant costs.

**Leading explanation — inference, and the test is cheap.** If the preference
rerolls on every call, then the preference we *satisfy* is not necessarily the
one in force when we harvest. This experiment skips the walk on the strength of
an observation that may already be stale by the time the harvest happens, so it
forfeits the 160x multiplier on exactly the passes it was meant to make cheap.
Losing the multiplier on even a small fraction of passes swamps a saving of a few
hundred ticks.

That would also explain why the effect is a *loss* rather than a wash: the more
we query, the longer between observation and harvest, and the more drift.

**How to test it directly** (queued as 037): record the companion at the moment
of the skip decision, then query again immediately before `harvest()` and compare.
If they disagree often, the map-skip path is fundamentally lossy and 013's win
comes from something narrower than it appears — which would matter, because 013
is a merged 18.5 s champion result.

**Three failed attempts preceded this one**, all mine: a crash with 54 GB free
(so `Fatal error in GC` is not only OOM), a silently no-op `.replace()` that left
`QUERY_LIMIT` undefined and produced an in-game ERROR, and a wedged UI where a
code window swallowed Escape so `reload` could not open the pause menu. Only the
relaunch cleared the last one.
