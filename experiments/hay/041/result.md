# exp-041 — growth-schedulability — result

**Outcome.** **adopted as a real finding — reopens multi-tile-per-drone
for Hay, unlike hay_single.** The 037 plan sat unrun for a full day; this
finally answers it.

**Numbers.** 2,520 samples (60/repeat × 42 internal repeats, pooled) from
the main drone (3,3).

| quantity | mean | median |
| --- | --- | --- |
| service cost (`SVC_DONE - PLANT`) | 1,022.6 | 1,300 |
| idle time (`RIPE - SVC_DONE`) | 160.5 | 3 |
| total growth-to-ripe (`RIPE - PLANT`) | 1,183.1 | 1,303 |

**The distribution is bimodal, and that's the finding.** Splitting on
`idle > 50` ticks:

- **67.8% of passes** (misses — real walk): idle ≈ **3 ticks**. Servicing
  alone (900-1,600+ ticks) already exceeds growth, exactly like
  hay_single's single-tile case — no slack here.
- **32.2% of passes** (hits — memory skip, ~20-30 tick service): idle ≈
  **492 ticks average**. On these passes the drone finishes all its
  companion-servicing work almost instantly and then **genuinely sits idle
  waiting for the plant to ripen** — this is real, measured slack that
  does not exist anywhere in hay_single's proven-tight schedule.

**Baseline.** hay_single's 001: own-tile handling ≈ growth time, idle time
≈ 0 on every pass, which is *why* multi-tile was closed there (001, and
re-confirmed 015). Hay's ~32%-of-passes idle window is a structurally
different situation.

**Noise floor.** Not established; n=2,520 across many repeats gives
reasonable confidence in the ~32%/~492-tick split as a real, not sampled,
feature — the split is far too clean (idle ≈3 vs ≈492, not a smooth
distribution) to be noise.

**Screenshots.** `logs/captures/20260816-235228-exp-hay-041-r1.png` — run
scored normally (02:52.690), confirming the instrumentation doesn't
disturb the champion.

**Verdict.** hay_single's "multi-tile is closed" conclusion does **not**
automatically transfer to Hay. The mechanism that closed it there
(schedulability — 001) does not hold here: on roughly a third of passes,
this drone has ~492 idle ticks it is currently wasting. A second tile that
could be serviced *during* that window — without adding it to the *other*
68% of passes, where there's no slack — is a real, measured opportunity,
not a hope. This converges with two independent estimates now: 039's
leader-implied ~441 ticks/harvest, and the old queue's own "leader implies
~2.2 tiles per drone at 466 ticks" figure. **042 should design and test a
genuine multi-tile-per-drone layout for Hay**, scheduled to exploit this
specific idle window rather than repeating 027/029's mistake (adding a
plot without first establishing that idle time exists to hide it in —
030's postmortem named this exact failure, and this measurement is what
030 never had).
