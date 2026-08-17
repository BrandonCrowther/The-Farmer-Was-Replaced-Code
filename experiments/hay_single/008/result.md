# exp-008 — finish-and-score — result

**Outcome.** **adopted — hay_single's first-ever score.**

**Numbers.** Modal: **04:49.565**, `VERDICT=scored`, **global rank #302**,
Personal Best 04:49.565 (first run, so PB = this run). Confirmed on-screen
against the leaderboard: leader `□萌萌的新□` at 02:17.995 (#1).

Per Leaderboard.md, the score is an average of runs repeated internally
until 2 real hours of simulated time accumulate — `output.txt` shows all 25
internal repeats:

| stat | value |
| --- | --- |
| runs | 25 |
| `TIME_FINAL` range | 280.58s – 296.83s |
| `TIME_FINAL` mean | ≈289.6s ≈ 04:49.6 — matches the displayed 04:49.565 |
| `HAY` at finish | 100,001,792 – 100,081,152 (target overshoot is small and expected — the loop's `can_harvest()` wait can only check the target between harvests, not mid-growth) |
| `TICK_FINAL` range | 1,704,484 – 1,803,248 |
| implied hay/tick | ≈55.6-57.0 — **better than 007's 49.9 projection** |

**Baseline.** 007's projection: ≈330s (≈05:30) at ≈49.9 hay/tick. Actual:
**≈289.6s (04:49.565)** at ≈55.8 hay/tick average — the real run beat the
projection by about 12%, likely because 007's tail window (cycles 100-195)
still had slightly more Bush/Tree-only traffic than the true long-run
steady state, where Carrot has been affordable for almost the entire run.

**Delta vs. the leader:** `289.565 / 137.995 ≈ 2.10x` — **≈2.1x off the
leader**, better than every earlier estimate in this queue (002: ~3x, 004's
best case: ~1.6-2x, 007: ~2.4x). Global rank **#302**.

**Noise floor.** Not established for this category's real scoring
mechanism (each score is already itself an average of 25 runs, so it should
be far more stable than a single probe — matches Hay's own finding that the
game's built-in 2-hour repeat-and-average makes categories "barely vary").

**Screenshots.** `logs/captures/20260816-215624-exp-hay_single-008-r1.png`.

**Verdict.** hay_single is no longer an empty category. The single-tile,
reactive-skip-and-remember design (settled by 001-007, correctly
free-riding on wood accumulation from ordinary companion churn rather than
a dedicated wood investment) works end-to-end: it terminates correctly, it
scores, and it lands at **rank #302, 2.1x off the world #1**. This is the
new champion by definition (first score) and should merge to `autofarmer`.

Given four independent multi-tile/lever rejections (001, 003 corrected,
005, 006) and a design that already beats its own projection, further
optimisation here is a smaller, harder-won gain than it was for Hay (which
started from a similarly bad baseline and ground it down over 36
experiments). Worth queuing for a future session, not immediately: the
inner `can_harvest()` wait loop is the only remaining obvious inefficiency
(it cannot detect the target being crossed mid-growth, only between
harvests, hence the ~65-81k hay overshoot each run — negligible against
100M, not worth chasing).
