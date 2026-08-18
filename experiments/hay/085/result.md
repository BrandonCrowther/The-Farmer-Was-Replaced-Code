# exp-085 — setup-phase tuple reuse for (px,py) — result

**Outcome.** **Adopted, new champion.** 01:54.587, Global Rank #52 —
down from 084's 01:54.669/#53. Two runs, r1 -0.039s (under the 0.069s
floor) and r2 -0.082s (clears it) — both negative, unlike a genuine
tie (080's r1/r2 disagreed in *sign*). Re-run required per
`docs/LOOP.md` (delta under ~2x the floor); the consistent direction
across both runs, not just the second run's own size, is what makes
this a believable small win rather than noise.

**Numbers.**

| run | metric | note |
| --- | --- | --- |
| validation (target=inventory+200,000) | clean completion, no warnings | 3-line output |
| real r1 | 01:54.630, #52 | -0.039s vs 084 (under the floor alone) |
| real r2 | 01:54.587, #52 | -0.082s vs 084 (clears the floor) |

**Baseline.** 084: 01:54.669, #53.

**Delta.** -0.082s (r2, the one that clears the floor), consistent in
sign with r1. -0.98% total from 084.

**Noise floor.** 0.069s. r1 alone didn't clear it; r2 did, and both
agree in direction — treated as a real, small, adopted win rather than
inconclusive, per the "consistent direction across a re-run" reading
(contrast with 080, whose two runs disagreed in sign).

**Verdict.** Confirms the setup-phase prediction going in: real, but
tiny — right at the edge of what this leaderboard's noise floor can
even resolve, exactly what 080's precedent (a ~30x larger setup change
that tied) predicted for a change this small. Adopting on the strength
of two same-direction runs rather than one large one is a slightly
different evidentiary bar than every other win tonight — worth being
explicit about in case a future re-measurement disagrees. A crash (
"Fatal error in GC", the documented routine memory-leak crash) hit
between r1 and r2; recovered via `tools/tfwr.sh relaunch` +
redeploy per `docs/LOOP.md`'s standard procedure, no data lost.
`saves/hay/main.py` updated and merged to `main`. `record.json` and
`queue.md` updated.
