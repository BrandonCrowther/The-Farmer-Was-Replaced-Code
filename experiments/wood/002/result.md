# exp-002 — raise water threshold for wood (multi)'s blocking growth wait — result

**Outcome.** **Closed, no code change, no live run.** Analytical
closure — see `hypothesis.md` for the full reasoning, built entirely
from 001's own already-recorded real-run numbers (588 water warnings,
the 91-ticks/harvest-summed-across-32-drones figure).

**Baseline.** 001: 06:07.889, #111. Unaffected — no change made.

**Verdict.** The premise (unhidden growth-wait is a free lever here)
doesn't survive checking 001's own numbers: real water contention
already exists at the current threshold (588 warnings), and the
design's real per-drone efficiency is already comparable to
wood_single's newly-optimized number, just achieved through
parallelism instead of interleaving. Raising water usage further has a
real, evidenced downside and a likely-small upside. Not tested live —
the analysis itself was enough to close the line, per `docs/LOOP.md`'s
discipline against spending a real cycle to confirm what the numbers
already argue against.
