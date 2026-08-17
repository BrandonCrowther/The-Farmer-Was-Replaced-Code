# exp-002 — reactive-companion-probe — result

**Outcome.** inconclusive (probe) — but decisive about the design question:
**the reactive/memory-skip approach, as coded, misses the leader's pace by
~3x.**

**Numbers** (60 cycles, one run):

| quantity | value | vs. prediction |
| --- | --- | --- |
| satisfied-harvest yield | **81,920** confirmed (every `HIT True` and `AFFORD True` line) | matches 001's carried-over Hay figure — confirmed, not just assumed, now |
| Carrot | 19/60 requests (31.7%, ≈1/3 as expected) — **0 affordable, ever** | confirms 001/002's wood-cost deduction; `WOOD` stayed **0** the entire run |
| own-memory hit rate | **8/60 = 13.3% overall**, but **0/31 in the first half, 8/29 (27.6%) in the second half** — rising as the ~24-position companion space fills | well under the naive 1/3 structural estimate *and* far under the ~75% the budget needs. The rise-then-plateau shape says the steady state is nearer 25-30%, not converging toward 75% no matter how long the run goes — more cycles fill in the same fixed ~24-cell neighbourhood, they don't change the per-visit odds. |
| steady-state ticks/harvest | tail-window (cycles 40-59): `(88155-62180)/20 ≈ 1,299` ticks/harvest; last 10: `≈1,341` | **1.9-2x over the ~686 budget from 001.** Not improving further by cycle 60 — this looks like the actual plateau, not a warm-up artifact still falling. |
| extrapolated finish | 3,459,584 hay in 14.51s (sim time) → linear extrapolation to 100,000,000: **≈419s ≈ 6:59** | **~3.0x slower than the leader's 02:17.995.** |

**Baseline.** 001's arithmetic (≥75% skip rate needed, ~686 ticks/harvest
budget).

**Noise floor.** Not established (single run, deliberately short). The
hit-rate trend (0% → 27.6%) is the more informative signal than the point
estimate; treat 13.3% as a lower bound on steady state, not the steady-state
value itself.

**Screenshots.** None read — probe terminates before a meaningful modal;
`output.txt` carries all the data.

**Verdict.** Two of 001's open questions are now closed, cleanly:

1. **81,920 confirmed** — the multiplier transfers unchanged from Hay.
2. **Carrot is permanently dead weight** under this design — 512 hay per hit,
   1/3 of all requests, zero path to ever afford it without a deliberate wood
   investment this design never makes.

The third finding is the important one, and it overturns part of 001's own
plan: **the solo-drone skip rate does not approach Hay's 44-66%** (that range
depended on neighbour drones incidentally pre-stocking each other's tiles,
per Hay's 021 — hay_single has no neighbours to borrow that from). It settles
near **25-30%**, and 001's "038 monocrop-stock" prescription — pre-plant
everything once, then mostly skip — doesn't beat this ceiling either: the
~24 reachable positions each get a *fresh, independent* type draw on every
visit, so **no static stock, however complete, can be right more than 1/3 of
the time per position**, and the measured 25-30% is already close to that
structural cap once Carrot's 1/3 share (permanently a miss) is priced in.

**This changes what 003 should test — not "build the driver," but "find a
lever that isn't companion-servicing efficiency," since ~3x is too large a
gap for tuning the skip rate to close.** Two candidates worth a cheap probe
each before committing engineering time to either:

- **Buy into Carrot.** It's 1/3 of requests, each worth 81,920 instead of the
  512 they currently score — the single largest wasted fraction in the trace.
  A dedicated wood income (grow one Tree tile off to the side purely to
  harvest for wood, amortized) could unlock it. Needs pricing: how many ticks
  of diverted drone-time per unit of wood, against how often Carrot's
  512-hay-and-512-wood cost can then be paid.
- **Reroll-before-ripening was considered and priced out arithmetically, not
  run:** `harvest()` on an unripe plant still destroys it at 200 ticks
  (Available-Functions.md: "if you harvest an entity that can't be harvested,
  it will be destroyed"), so a reroll-until-hit costs ~400 ticks/attempt
  (destroy+replant) at a ~27.5% hit chance — expected ~1,250+ ticks just to
  land a preference, *before* the growth wait even starts. That is worse than
  the current blended average, not better. **Rejected without a run** — the
  arithmetic is decisive enough on its own and a run would only spend a cycle
  confirming what `harvest()`'s documented cost already settles.
