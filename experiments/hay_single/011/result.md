# exp-011 — champion-tick-profile — result

**Outcome.** adopted (confirms 010's real number; corrects 009's probe).

**Numbers.** Real scored run, same shape as 010 (29 internal repeats, 697
`PROFILE` lines ≈ 24 per repeat). Ticks/harvest between consecutive
50-harvest checkpoints, one representative repeat (harvest 50→1200):
fluctuates **1,059–1,460**, no downward trend after harvest 100 — it is
*already* at steady state by harvest 100 and stays there (mean ≈1,250 across
the sampled checkpoints), all the way to harvest 1,200.

**This does not match 009's 200-cycle tail estimate (≈829.5) — it matches
010's real score far better** (81,920/64.7 ≈ 1,267 implied).

**The theoretical model, recomputed exactly** (`R`=400 reroll, `W`=1,600
walk, `p`=1/3 hit chance, `REROLL_LIMIT=K`):

| K | predicted ticks/harvest | predicted hay/tick |
| --- | --- | --- |
| 0 (008's walk-always) | 1,466.7 | 55.85 — **matches 008's real 55.8 almost exactly** |
| 2 (010's champion) | 1,318.5 | 62.13 — close to 010's real ≈64.7 |
| 5 | 1,235.1 | 66.33 |
| 7 | 1,215.6 | 67.39 |

The model tracks the real measurements well once corrected for the fact
that 009's *particular* 200-cycle tail window (cycles 175-199) happened to
land on an unusually lucky run of hits — not a bug, just an unrepresentative
sample, exactly the kind of thing docs/LOOP.md warns single short windows
can produce. **The real steady state was there to be read from 011's
profile all along; 009 should have run longer or sampled more of the
trajectory rather than trusting one 25-cycle tail.**

**Diminishing returns are clear and steep.** K=0→2 gains +6.28 hay/tick;
K=2→5 gains only +4.20; K=5→7 gains +1.06. Past K≈5, further tuning is a
small, shrinking return for an unbounded (if cheap) amount of reroll
traffic.

**Baseline.** 009 (≈829.5 ticks/harvest, now known unrepresentative). 010
(real, ≈1,267 ticks/harvest, confirmed representative by this profile).

**Noise floor.** Within-run variance across 50-harvest windows is real
(±15-20% swing, e.g. 1,059 to 1,460) — a single-window estimate from any
probe shorter than a few hundred harvests should be treated as noisy, not
exact, going forward.

**Screenshots.** `logs/captures/20260816-221120-exp-hay_single-011-r1.png` —
this run also scored (04:13.634, rank #182, PB unchanged at 010's
04:13.399), confirming the two runs are the same design within normal
run-to-run noise (0.235s apart). Journal-only: the profiling prints are
diagnostic, not part of the champion, so `saves/hay_single/` stays on this
branch rather than merging over 010's clean version.

**Verdict.** 010's champion is confirmed as a good measurement of the
design's true throughput, not an unlucky undershoot. There is real, modest,
further headroom in raising `REROLL_LIMIT` — the model predicts K=5 at
66.33 vs K=2's 62.13, roughly a further **+7% hay/tick** — worth one more
real run (012) before calling this line exhausted. Past K≈5-7 the model
itself says further tuning isn't worth another experiment.
