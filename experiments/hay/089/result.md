# exp-089 — hot-loop mechanism probes — result

**Outcome.** **Both candidates closed — no code change.** Neither was
a bug and neither is a viable lever, but both are now closed with real
measured data instead of being left as open, tempting-looking
possibilities for a future session to re-discover and waste a cycle
chasing.

## 1. Reroll-chase correctness — confirmed sound, not a bug

Instrumented the real champion's hot loop (every drone, first 5
iterations, `wait`/`harvest`/`reroll_ticks`/`reroll_count`/`move` split
via `get_tick_count()`, 0-tick instrumentation, no scored run). Result:
`reroll_ticks` scales **exactly linearly** with `reroll_count` — 11,
219, 427, 635, 843, 1051, 1259, 1467, 1675, 1883, 2091 for
`reroll_count` 0 through 10, i.e. `11 + 208*count` with zero variance
at every observed count. No sign of wasted/irregular cycles.

The initial concern (each `harvest()` call in the reroll-chase costs
~207-208 ticks, less than exp-066's isolated ~407-409 tick growth
wait, so most reroll attempts should be destroying immature plants for
nothing) turns out to rest on a wrong model of what the reroll-chase
is *for*. Landing a match (`ctype == Entities.Bush and pos in
planted`) just `break`s — **no extra harvest happens on the winning
attempt**. Every `harvest()` call inside the loop exists purely to
force a fresh companion-preference roll via destroy+auto-regrow (036
already established replant is what rerolls the preference); the
freshly-rolled, now-*correctly-preferenced* immature plant is left
standing to mature normally and gets its real (potentially 67x)
harvest on a *later* visit, not this one. There is no growth-wait
needed between reroll attempts because no attempt is trying to harvest
real yield — the flat 208-tick-per-attempt cost is the mechanism
working exactly as designed, confirmed by the perfectly clean linear
scaling. Nothing to fix here.

## 2. Water threshold — confirmed already correctly tuned, not just "no slack"

Setup never checks water (a ~20,000+ tick phase per drone), and
`Watering.md` documents continuous decay ("loses 1% of its current
water per second"). Measured this directly: at the shipped
`WATER_THRESHOLD=0.75`, the hot loop's first water-check pays a real,
one-time **burst catch-up cost, ~1,390 excess ticks/drone**, spread
over the first ~4-5 iterations (639, 646, 69, 43, 18 ticks of excess
over a ~5-tick baseline), then settles to exactly zero for the
remaining ~866 harvests of a full run. `~44,500 ticks fleet-wide`,
real but one-time.

Two follow-up probes tested whether a lower threshold reduces this,
and both would have given the *wrong* answer if judged only on a short
window:

- **`WATER_THRESHOLD=0.0`** (never waters): `wait` (real idle busy-
  wait for ripeness) explodes — mean 4 ticks/iteration at the shipped
  threshold, up to a mean of **1,195 ticks/iteration by iteration 2**,
  still rising with no sign of stabilizing by iteration 4. Growth
  becomes the bottleneck and the deficit compounds. Clear loss,
  confirms watering is load-bearing.
- **`WATER_THRESHOLD=0.3`**: looked like a clear win at first —
  smaller one-time transient (~420 excess ticks/drone vs 0.75's
  ~1,390) that settles by iteration 2. **But extending the observation
  window from 5 to 40 iterations/drone reversed the conclusion
  completely**: `wait` never returns to the ~4-tick baseline — it
  settles into a *persistent* steady-state band of ~20-80 ticks/
  iteration (mean ~35-50) that holds flat across all 40 measured
  iterations with no decay. Extrapolated over a full ~871-harvest run,
  that steady-state cost alone totals **~35,000+ ticks/drone** —
  roughly **25x worse** than 0.75's one-time transient. The short
  window missed this entirely; only extending it caught the reversal.

**Verdict.** `WATER_THRESHOLD=0.75` is not merely "no slack" (083's
framing) — it is the point below which growth starts costing real,
*permanently recurring* idle time instead of a bounded one-time
catch-up. Lowering it is a clear, measured loss, not a neutral
non-improvement. This closes the water-threshold line definitively.

**Method note worth keeping**: a short instrumentation window can be
actively misleading for anything with a steady-state/transient
distinction — the 5-iteration probe pointed the wrong direction here.
Extend the window whenever a candidate looks like a win before trusting
it, per the same "a conclusion needs a test that is not a full run,
but that test must actually observe the mechanism" principle
`docs/LOOP.md` already states for other cases.

**Baseline.** 088: 01:54.162, #52 — unaffected, no code change, no
scored leaderboard cycle spent. Game verified restored to 088
(`live/main.py` hash `080da0218007f4186df896ae90008d3a`, matches
`saves/hay/main.py`) after all probes.

**Verdict.** No merge — journal only. `record.json`/`queue.md` updated.
