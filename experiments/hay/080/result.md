# exp-080 — precompute NEAR_OFFSETS once at module level — result

**Outcome.** **Tied, not adopted.** Real runs landed on both sides of
the baseline, both inside the noise floor.

**Numbers.**

| run | metric | note |
| --- | --- | --- |
| offline correctness check (Python, 6 base positions incl. seam-crossing corners) | 32/32 offsets identical to old per-drone scan | exact match every time |
| validation (target=200,000) | 32/32 drones, 30 tiles each, clean, no warnings | matches expected count exactly |
| real r1 (target=2,000,000,000) | 01:56.077, #58 | -0.015s vs 079's baseline |
| real r2 (target=2,000,000,000) | 01:56.149, #58 | +0.057s vs 079's baseline |

**Baseline.** 079: 01:56.092, #58.

**Delta.** r1: -0.015s. r2: +0.057s. Both under the 0.069s noise floor,
and in opposite directions — a tie, not a signal either way.

**Verdict.** Per `docs/LOOP.md`: "A delta smaller than [the noise
floor] is not a result, whatever it looks like," and two runs landing
on opposite sides of the baseline is the textbook noise pattern, not a
real effect waiting to be confirmed by a third run. Matches exp-060's
precedent (a near-exact tie, not adopted, even though the reasoning
behind the change was sound) — the leaderboard result is the arbiter
here, not the reasoning, however solid the reasoning is. **Not
adopted**: `saves/hay/main.py` stays on 079's champion; this branch's
code does not merge to `main`, only this journal does, per
`docs/LOOP.md` step 8's loss/inconclusive path.

This does not mean the change was wrong — the offline equivalence proof
and live validation both hold regardless of the real-run outcome, and
the change remains provably non-regressive. It means one of two things:
either 077's "module state is shared across drones" reading was too
strong (each drone may still redo comparable work, making this
relocation genuinely tick-neutral), or the real saving is real but too
small a fraction of the ~2-hour-simulated averaged score to clear this
noise floor at the champion's current, already-tight tick budget. Either
way, the setup phase's remaining stray-tick budget (as opposed to the
hot loop's, where 079's reroll fix *did* clear the floor) may simply be
running out of room to matter at this leaderboard's resolution — worth
keeping in mind before spending more cycles on setup-phase-only
micro-optimizations specifically.
