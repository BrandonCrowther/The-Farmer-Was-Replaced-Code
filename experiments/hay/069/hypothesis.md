# exp-069 — spatial pre-seeding: bush walls around a dynamic core

**Hypothesis (user's proposal).** The reroll chase is sequential
(207/attempt) and only distance-1 walks are cheap enough to be worth
servicing dynamically. So: pre-seed every n=2/n=3 reachable position (20
of 24) with permanent Bush before the loop starts, leaving only the 4
n=1 tiles genuinely dynamic. A draw is accepted the instant it's either
(a) a memory-matched Bush at an n=2/3 tile (free, pre-seeded) or (b) any
type at an n=1 tile (cheap to walk); anything else (n=2/3, non-Bush) is
rerolled. Predicted accept probability: 1/6 (n=1) + (20/24)(1/3) (bush
match) = 32/72 ≈ 0.444, vs ~0.288 measured for the natural-accumulation
champion (068).

**Variable.** v1: hybrid (20 static bush, 4 dynamic n=1). v2 (follow-up,
same run): fully static — all 24 reachable positions pre-seeded Bush,
zero dynamic tiles, zero walks ever attempted.

**Metric.** Same as 068: windowed ticks/harvest, reroll histogram,
memory size, over 900 cycles (single drone, no target gate).

**Baseline.** 068: real champion, steady state ~1070-1220 ticks/harvest,
avg 1.93 rerolls/cycle, 17.2% exhaustion rate.

**Procedure.**
1. `saves/hay/main.py` (as `zzDriver.py` to force harness window
   selection — `Common.py` was winning the top-of-pile slot otherwise):
   one-time setup loop pre-plants Bush at the target positions, then the
   same windowed 900-cycle measurement loop as 068.
2. Smoke test only — no `zzRunner.py` in this deploy.
3. `tools/tfwr.sh run`, poll `output.txt` (multi-minute real run, not a
   fast probe).

**Falsifier.** If total ticks/harvest doesn't drop meaningfully below
068's baseline despite the higher accept probability, the walk cost for
servicing the "cheap" n=1 tiles is eating the reroll savings, and the
idea needs the zero-walk (v2) variant instead. If v2 *also* doesn't
improve on 068, accept/reroll policy design in general has hit a real
structural ceiling given the 24-position/3-type/207-reroll/~800-walk
mechanics, independent of policy cleverness.
