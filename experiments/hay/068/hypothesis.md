# exp-068 — where does the real champion actually sit vs. the corrected floor?

**Hypothesis.** 066/067 corrected the reroll cost from 400 to ~207
ticks, dropping the theoretical zero-servicing floor from ~815 to ~622.
But 058/059's real REROLL_LIMIT sweep already ran under the true costs
(the game was never wrong, only the mental model was) — so before
designing any new variant, measure where 057's actual design really
sits, in real ticks/harvest, at full memory maturity. If it's well above
622, there may be real headroom; if it's already close, the "reopen the
family" framing was premature.

**Variable.** None — direct instrumented measurement of the champion's
unmodified per-cycle logic, single drone, no target gate.

**Metric.** `elapsed_ticks / cycles`, windowed every 150 cycles across
900 cycles (matching the real ~871 cycles/drone from a full run), plus
the reroll-count histogram and memory size over time.

**Baseline.** Corrected zero-servicing floor: 622 (207 own-handling +
415 growth). Old (wrong) floor: 815. Cluster's implied band: ~750-856
ticks/harvest.

**Procedure.**
1. `saves/hay/main.py`: single drone at (3,3), champion's exact
   per-cycle logic (`Common.polyculture_mapped`, harvest, reroll loop),
   capped at 900 cycles, windowed `quick_print` every 150.
2. Smoke test only — no `zzRunner.py` in this deploy.
3. `tools/tfwr.sh run`, read `output.txt` (this run takes real minutes,
   not seconds — poll rather than assume the fast-idle pattern of
   earlier short probes).

**Falsifier.** If windowed ticks/harvest keeps trending down toward 622
as memory matures, there's real headroom and a new variant is worth
building. If it plateaus well above both floors, the paradigm's real
ceiling is dominated by something the operation-cost model doesn't
capture (e.g. the reroll-exhaustion tail), and further reroll-policy
tuning isn't where the gain is.
