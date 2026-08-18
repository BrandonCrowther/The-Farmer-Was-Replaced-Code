# exp-084 — reroll accept-check reorder + avoid rebuilding an existing tuple — result

**Outcome.** **Adopted, new champion.** 01:54.669, Global Rank #53 —
down from 082's 01:55.590/#56. A real -0.921s (-0.80%), +3 ranks —
larger than the smoke test's inconclusive ~8-tick signal suggested,
the same underestimation shape 079's own smoke test had.

**Numbers.**

| run | metric | note |
| --- | --- | --- |
| single-drone smoke test (900 cycles) | 865.09 ticks/harvest (windows 819-881) | vs. 082's 873.02; small, inside window-to-window noise |
| real (target=2,000,000,000) | **01:54.669, #53** | `VERDICT=scored`, `WARN=1443 Water` (routine) |

**Baseline.** 082: 01:55.590, #56.

**Delta.** -0.921s (-0.80%), +3 global ranks.

**Verdict.** The reroll chase's accept-check had two more of exactly
079's class of stray-tick sitting in the same three lines: an
unnecessary tuple rebuild, and an AND ordered against the actual
probability distribution instead of with it. Both provable safe by
reading the code alone, no new game mechanic assumed — and despite
running on every reroll attempt (the hot loop's own dominant cost,
per 069's structural analysis), the real win here (-0.921s) is the
*largest* single stray-tick fix since 079 itself (-0.798s), bigger
than 081 or 082 individually. Directly confirms the user's framing:
this class of fix was not exhausted after 083's "closing scour" —
083 checked macro-level ideas (more tiles, mixed pre-seeding, dropping
the position check) and correctly found those closed, but didn't
re-derive the accept-check's own internals from scratch a second time.
Worth another pass over the same three lines and the water-check block
for anything else in this shape before assuming it's dry again.
`saves/hay/main.py` updated and merged to `main`. `record.json` and
`queue.md` updated.
