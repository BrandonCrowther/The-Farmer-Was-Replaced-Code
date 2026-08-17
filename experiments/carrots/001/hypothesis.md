# exp-001 — terminate the seeded achievement driver

**Hypothesis.** `saves/carrots/main.py` is structurally identical to
`saves/wood/main.py` (same 32-drone interleaved-Grass-companion
pattern, just `Entities.Carrot`/`Items.Carrot` instead of
`Entities.Tree`/`Items.Wood`), which just scored 06:07.889/#111 for a
10-billion target after only target-gating + a water-guard, no other
changes. This should transfer directly at high confidence — target
here is 2,000,000,000, 5x smaller than Wood's.

**Variable.** Seeded `while True:` per-drone loop → target-gated on
`Items.Carrot`; water-topup guarded (same fix as wood/sunflowers
multi-drone 001s).

**Metric.** The completion modal's verdict and displayed time — this
category's first-ever leaderboard entry.

**Baseline.** wood (multi) 001: 06:07.889 for 10B at this exact driver
shape. Given a 5x smaller target and the same design, projecting
well under that, real time uncertain but low-risk given the proven
pattern.

**Procedure.**
1. `saves/carrots/main.py`: target-gate both per-drone and main loops,
   water-guard.
2. `tools/cycle.sh carrots exp-carrots-001-r1 --from <worktree>` directly
   (skipping a separate smoke test given the just-proven identical
   pattern on wood (multi)).
3. Read `SHOT=` with vision for the time and rank; read `OUTPUT=` for
   the diagnostic line.

**Falsifier.** If this doesn't transfer as cleanly as expected (a hang,
or a wildly different throughput), check whether Carrot's companion/
growth mechanics genuinely differ from Tree's before assuming the
driver itself has a new bug.
