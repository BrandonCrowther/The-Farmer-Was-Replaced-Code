# exp-012 — skip-unaffordable — result

**Outcome.** adopted — new champion, small but confirmed

**Numbers.**

| run | seed | metric | note |
| --- | --- | --- | --- |
|  1  | random | 03:24.327 | −0.225 s |
|  2  | random | 03:24.367 | −0.185 s, confirming run |

**Baseline.** 03:24.552 · **Variant.** 03:24.347 (mean) · **Delta.** **−0.205 s**

**Noise floor.** 0.15 s. The first run cleared it by only 1.5x, under the 2x bar
for believing a single result, so it was re-run. Both runs land on the same side
by a similar margin, which is what makes this a result rather than a coin toss.

**Warning histogram.**

| warning | 010 champion | 012 |
| --- | --- | --- |
| Didn't have the required items to plant `Entities.Carrot` | 1094 | 224 / 338 |
| Cannot plant `Entities.Carrot` on `Grounds.Grassland` | 11 | 256 / 210 |

The skip clearly works — unaffordable attempts collapse. Two leftovers explain
why the win is smaller than the tick arithmetic suggests:

- **~220-340 attempts still fail on affordability**, which looks like a race:
  `affordable()` sees enough wood, another drone spends it before this drone
  arrives and plants.
- **"Cannot plant on Grassland" rose to ~230**, the same occupied-tile problem
  003 and 006 hit — `till()` will not convert ground a plant is standing on, so
  when carrot *is* briefly affordable the planting fails anyway.

So the walk is now skipped when carrot is unaffordable, but carrot is still never
successfully planted. A third of companion requests continue to earn no
multiplier at all. **That, not tick-shaving, is the largest thing left on the
table** — see the queue's carrot-when-rich line.
