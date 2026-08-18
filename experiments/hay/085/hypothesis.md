# exp-085 — setup-tuple-reuse

**Hypothesis.** <one sentence, falsifiable>

**Variable.** <the single thing being changed>

**Metric.** <the number that decides it, and where it is read from — e.g.
`simulate()` return value via `quick_print`, read from the output page>

**Baseline.** <commit ref of the code being varied, and its measured value>

**Procedure.**
1. Write `script.py` into `save/Save0/<Name>.py`.
2. Wait for File Watcher pickup (confirm with a crop diff, ~1 s).
3. `tools/tfwr.sh run`, wait for completion.
4. `tools/tfwr.sh capture` and read the marked output lines.
5. Repeat N times; record every run, not just the best.
