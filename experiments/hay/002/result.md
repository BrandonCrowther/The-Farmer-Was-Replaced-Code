# exp-002 — baseline — result

**Outcome.** adopted as the Hay baseline

**Numbers.**

| run | seed | metric | note |
| --- | --- | --- | --- |
|  1  | random | **04:55.182** | PB; accepted |
|  2  | random | 04:55.469 | accepted |
|  3  | random | 04:55.310 | accepted |

**Baseline.** 04:55.320 (mean of 3) · **Variant.** n/a · **Delta.** n/a

exp-001's separate run of 04:55.393 sits inside this spread; over all four runs
the mean is 04:55.339.

**Noise floor.** **±0.15 s (1 sd), range 0.287 s over 3 runs — a coefficient of
variation of 0.05%.** Treat anything under ~0.3 s as noise; 1 s is comfortably
real.

This is nothing like `fastest_reset`'s ~10.7 minute floor, and the reason is in
the wiki rather than in the code: every leaderboard run is *repeated until two
hours of simulated time have accumulated, and the average is what gets
uploaded*. The number on the modal is already a mean over many repeats, so the
per-run variance has been averaged away before we ever see it. `fastest_reset`
is noisy because a single reset run is long enough that few repeats fit in the
two hours.

**Practical consequence.** Hay needs far fewer repeats per experiment than the
Phase 3 plan assumes. One run per variant is enough to rank candidates; a
confirming second run is only worth it for a decision that matters.

**Screenshots.** `logs/captures/20260815-2245*-exp-hay-002-r*.png`

**Verdict.** Baseline fixed at **04:55.320**. The warning counts are stable
across runs too (759/761/750 carrot, 714/725/713 water), so they are structural,
not luck — which makes 003 and 004 measurable against this floor.
