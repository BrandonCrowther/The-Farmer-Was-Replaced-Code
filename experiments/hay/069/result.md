# exp-069 — spatial pre-seeding: bush walls around a dynamic core — result

**Outcome.** Both variants confirmed their own mechanism precisely and
neither beat the baseline — a real, convergent null result, not a
failed test. The reroll-side math was exactly right in both directions;
the total didn't move because the walk cost and the reroll cost trade
against each other under these mechanics.

**Numbers.**

v1 (20 static Bush at n=2/3, 4 dynamic n=1):

```
SETUP_DONE ticks 19112 memory_size 20
WINDOW_END 900  TICKS_PER_HARVEST_THIS_WINDOW 1104.11  MEMORY_SIZE 24
CYCLES 900  ELAPSED_TICKS 962612  TICKS_PER_HARVEST 1069.57
ACCEPT_REASON_bush_n1_exhausted [670, 230, 0]   (74.4% bush-match, 25.6% dynamic-n1, 0% exhausted)
```

Avg rerolls/cycle ≈ 1.19 (down from 068's 1.93 — the predicted-boost
mechanism worked). But 230/900 cycles required a real ~800-tick walk
next cycle (the n=1 tile's type changes almost every draw, so it's
essentially never already memory-correct) — that walk cost ate the
reroll savings almost exactly.

v2 (all 24 reachable positions static Bush, zero dynamic tiles):

```
SETUP_DONE ticks 20871 memory_size 24
WINDOW_END 900  TICKS_PER_HARVEST_THIS_WINDOW 1050.35  MEMORY_SIZE 24
CYCLES 900  ELAPSED_TICKS 961518  TICKS_PER_HARVEST 1068.35
ACCEPT_REASON_bush_n1_exhausted [900, 0, 0]   (100% bush-match, 0% walk, ever)
REROLL_HIST [293,190,135,93,65,41,28,16,13,10,4,6,1,3,1,1,0,...]
```

Avg rerolls/cycle ≈ 2.07 — matches the p=1/3 prediction almost exactly
((1-1/3)/(1/3) = 2.0) once the n=1 "any type" shortcut is removed.
Predicted total: 615 + 207×2.07 ≈ 1044; measured: 1068 — within 2.4%.

**Baseline.** 068 (natural accumulation): ~1070-1220 ticks/harvest.

**Verdict.** Both variants land in the *same* ~1000-1200 band as the
champion's own organic accept policy — this is now three independently
structured designs (natural accumulation, hybrid bush+dynamic, fully
static) converging on the same number, for three different, well-
understood reasons. There's a real conservation trade in these
mechanics: any path that's easier to hit (adding the n=1 "any type"
shortcut) costs more when it lands (a walk); removing that shortcut
(pure static) costs more to reach it (more rerolls). Combined with the
eight earlier real-measured rejections (051, 053-055, 058-061), this is
strong, convergent evidence that **accept/reroll policy design has hit
a genuine structural ceiling given the current 24-position/3-type/
207-reroll/~800-walk mechanics** — not a coincidence of any one design
being clever or not. No champion change. Closing the accept-policy
family for real this time, on nine independent confirmations rather
than one model's prediction. If there's a lever left, it's not in this
space at all — it would need to change the mechanics being traded
against (e.g. the number of reachable positions, or the type space),
not the policy operating within them.
