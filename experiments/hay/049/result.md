# exp-049 — reroll-before-walk retest, correctly timed, REROLL_LIMIT=5 — result

**Outcome.** looked like a rejection here — **see 057: this was a
time-horizon artifact, not a real rejection.**

**Numbers.**

| run | metric | note |
| --- | --- | --- |
| r1 | `HITS_SKIP` 118/150 (78.7%), `HITS_WALK` 32/150 | skip rate more than doubled vs 047's no-reroll baseline (36.7%) |
| r1 | `TICKS_PER_HARVEST` 1,471.41 | *worse* than 047's 1,390 despite the much higher skip rate |

**Baseline.** 047: 1,390 ticks/harvest, no reroll.

**Variant.** 1,471.41. **Delta.** +5.9% (regression, matching 038's
original rejection direction).

**Noise floor.** Not established — single 150-cycle sample.

**Screenshots.** None — probe.

**Verdict.** At the time this looked like a clean confirmation of 038's
rejection: reroll costs more than it saves. But Hay has no free-type
companion shortcut (unlike carrots_single/wood_single's free-Grass),
so a memory-matched reroll's hit rate depends entirely on how many of
the ~24 candidate positions *this specific drone* has personally
walked to before — and 150 cycles is a small sample of that space. 057
reran the identical logic as a real, full target-gated run (≈871
cycles/drone) and got a real, positive result (02:42.421 vs the
champion's 02:47.682) — the opposite direction from this probe. The
lesson: for a mechanism whose payoff depends on state accumulated over
the *whole* run, a short bounded probe can be actively misleading, not
just noisy — worth remembering for future reroll/memory-based designs.
