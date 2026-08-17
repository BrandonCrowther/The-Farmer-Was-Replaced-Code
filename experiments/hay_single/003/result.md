# exp-003 — price-carrot-lever — result

**Outcome.** rejected — settled from the wiki, no game cycle run (consistent
with docs/LOOP.md: "Check the API and the wiki first. They are free.").

**Numbers.**

| step | value |
| --- | --- |
| wood needed for all ≈407 Carrot occurrences | `407 * 512 = 208,384` |
| tree-harvests needed (Tree.md: 5 wood/tree) | `208,384 / 5 = 41,677` |
| floor ticks (plant+harvest only, **ignoring growth wait and all movement**) | `41,677 * 400 = 16,670,800` |
| whole-run budget (001) | `≈837,600` |

The most generous possible floor for the wood-income lever is already **~20x
the entire run's tick budget**, before counting a single tick of tree growth
time or the movement to/from a separate wood tile. No probe changes that
ratio enough to matter — even if trees turned out to grow instantly for free,
the plant+harvest floor alone still blows the budget by 20x.

**Baseline.** 002's measured design (~1,221 harvests, ≈407 Carrot misses at
512 each instead of 81,920).

**Noise floor.** N/A — arithmetic, not a measurement.

**Screenshots.** None — no game cycle run.

**Verdict.** Carrot is not a lever at any achievable wood-income design; the
5-wood tree yield against a 512-wood cost is a >100x mismatch that no amount
of tuning survives. This closes the queue's second candidate from 002's
result.md. Combined with 002's own finding (companion-servicing efficiency
tops out ~3x short of the leader) and the standing "no-polyculture" dead end
(inherited from Hay's 011, and worse here without 32x parallelism), **every
lever queued so far is now closed.** 004 has to be the fundamental-fork
question docs/LOOP.md requires before stopping on an empty queue — see
`queue.md` for the one live candidate: whether a single drone tending a
*small cluster* of grass tiles (not for idle-hiding, which 001 already ruled
out, but so the drone's own visits to overlapping companion zones recreate
Hay's 021 "contention is cooperation" effect solo) can push the skip rate
past the ~25-30% solo ceiling 002 measured.
