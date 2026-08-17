# exp-074 — measure the real adopted champion's actual ticks/harvest

**Hypothesis.** 073's real `main.py` (the adopted champion) carries none
of 071/072's measurement-harness overhead — no accumulator tracking, no
windowed-print check inside the hot loop, which 071 found cost ~27
ticks/harvest on its own. The real deployed code should therefore beat
072's instrumented 923.53 by roughly that amount.

**Variable.** None — direct measurement of the exact, unmodified
`saves/hay/main.py` driver logic (073), single drone, capped cycle
count.

**Metric.** Windowed ticks/harvest over 900 cycles, same methodology
as 068/071/072.

**Baseline.** 072 (instrumented): 923.53 ticks/harvest.

**Procedure.**
1. Copy 073's exact driver logic verbatim, wrap in a 900-cycle loop
   with windowed `quick_print` (no per-category accumulators — those
   were exactly the overhead being tested for).
2. Smoke test only — no `zzRunner.py` in this deploy.
3. `tools/tfwr.sh run`, poll `output.txt`.

**Falsifier.** If the real code doesn't beat 923.53 by roughly the
~27-tick margin 071 identified, that overhead wasn't really
instrumentation-specific.
