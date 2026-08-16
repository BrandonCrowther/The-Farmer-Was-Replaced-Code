# exp-006 — reroll-companion

**Hypothesis.** A plant's companion preference is rerolled by replanting, and
grass is free. With 004 making Bush and Tree pay out, Carrot is the only face
that costs anything, so rerolling it should convert ~1/3 of companion visits
from "unaffordable, no multiplier" into "free, multiplier earned".

**Variable.** `Common.reroll_companion(entity, 3)` before the companion walk.
Nothing else changes.

**Metric.** Time vs the 03:40.911 champion; floor 0.15 s. Cross-check: the
"didn't have the required items to plant Carrot" count should fall sharply.

**Baseline.** `autofarmer` at 1848fb4 — 03:40.911.

**Cost model.** Each reroll is a harvest plus a plant. Two of three faces are
free, so a reroll clears in ~1.5 tries and only ~1/3 of iterations need one.
Capped at 3 so a bad run of luck cannot spend unboundedly.
