# exp-040 — draw-pattern-check

**Hypothesis.** 013 confirmed the (type, position) companion draw is
IID-uniform for hay_single's solo drone. This checks the same thing for
Hay's main drone, with 31 neighbours actively farming around it — if the
draw is *also* IID-uniform here, 039's ~441-tick leader estimate needs a
different explanation than "the leader escaped the 1/3 draw probability."
If it isn't IID here, that's a genuinely new, multi-drone-specific finding
neither 011 nor 013 could have surfaced from hay_single alone.

**Variable.** None — 020's champion unchanged for the 31 spawned drones;
the main drone samples 300 raw draws (plant → read → discard, no
servicing) before joining the normal farming loop for the rest of the run.

**Metric.** The 300 `DRAW` lines: type frequency, position frequency,
autocorrelation, and (new for this context) whether the drawn position's
*current physical occupant* (if we can infer it) correlates with what gets
drawn — same statistical checks as 013.

**Baseline.** 013's hay_single result: type freq within 0.4% of 1/3, no
autocorrelation, no type-position correlation — the null hypothesis this
run is tested against.

**Procedure.**
1. `saves/hay/main.py`: add a `sample` flag to `driver()`; the main drone
   runs 300 sample cycles first, then falls through to the normal champion
   loop so the run still reaches the real 2,000,000,000 target and scores.
2. `tools/cycle.sh hay exp-hay-040-r1 --from <worktree>` (background — this
   is a real, full scored run, same wall-clock cost as 038/039).
3. Read `OUTPUT=`, parse the 300 `DRAW` lines, run the same statistical
   checks as 013 offline.

**Falsifier.** If the draw is IID-uniform here too (matching 013 closely),
039's ~441-tick estimate is not explained by "beating the draw" — recheck
the same-drone-count/tick-rate assumptions behind that ratio, or look for
an entirely different explanation (a different plot layout, a mechanic
neither hay_single nor Hay's current champion uses at all) rather than
continuing to chase the companion-draw angle.
