# exp-005 — use-shared-helper

**Hypothesis.** `Common.plant_companion()` reproduces 004's local override
exactly, so hay/main.py can drop its private `polyculture()` and the time will
be unchanged.

**Variable.** Where the companion-planting fix lives — hay's `main.py` or the
shared `Common.py`. No behavioural change intended.

**Metric.** Must land at 03:40.911 ± 0.15 s. This is a confirming run: a *change*
in either direction is the failure, not the success.

**Baseline.** `autofarmer` at f01cfff — 03:40.911.
