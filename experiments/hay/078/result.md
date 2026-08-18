# exp-078 — shared bush-wall planting / territory partitioning — result

**Outcome.** **Rejected — analytical closure, no live run needed.**

**Numbers.** None taken; no code was written or deployed. See
`hypothesis.md` for the reasoning chain, built entirely from already-
measured facts in this investigation (043's tick-rate/parallelism
finding, 050's drone-isolation finding, 069's memory-coverage-vs-walk-
cost trade-off measurement) plus a direct check of `docs/api/` for any
cross-drone read/sync primitive (none exists beyond `wait_for()` on a
direct spawn handle).

**Baseline.** 077: 01:56.890, #59 (unaffected — no code change).

**Delta.** None.

**Verdict.** A genuine walk-skipping partition needs a non-owning drone
to trust a shared tile is already planted without visiting it — the API
has no remote-read, and the only alternative (trust an ownership rule
without observing the tile) is a real correctness bug given that 077's
own spawn tree made setup order across drones provably unordered: a
drone could draw a companion request for a neighbor-owned tile before
that neighbor has actually planted it, silently `break` out of its
reroll-chase believing the request satisfied, and lose the polyculture
multiplier on that harvest with no warning. Even a hypothetically
race-free version of this idea would likely lose anyway — 069 already
measured that *reducing* proactive tile coverage (069v1's 20/24
partial pre-seed) barely helps over no coverage at all, because the
uncovered positions' real walk cost eats the savings; full coverage
(069v2) won outright. Closing this line without a run rather than
spending a real 2h-simulated scored cycle to re-derive a conclusion
already implied by three separate measured results. Next: scour the
champion's code for remaining stray-tick overhead of the 075/076/077
kind, per the queue.
