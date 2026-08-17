# exp-057 — full memory-matched reroll-before-walk, real full run

**Hypothesis.** 049's 150-cycle bounded probe showed reroll-before-walk
(memory-matched, `REROLL_LIMIT=5`) regressing (1,471 vs 1,390) — but
Hay has no free-type shortcut (Grass excludes itself as a companion,
unlike carrots_single/wood_single's free-Grass trick), so the memory
dict's hit rate depends entirely on how many of the ~24 candidate
positions this drone has *personally* walked to before. A 150-cycle
probe barely samples that space; the real run gives each drone ≈871
cycles (27,879 harvests ÷ 32 drones, at the champion's real weighted
yield) to mature its memory — steady-state hit rate should approach
~1/3 per draw (matching the physical baseline 37% skip rate already
observed without any reroll), and rerolling toward *any* memory match
(not just escaping Carrot) compounds that via `1-(2/3)^(rerolls+1)`,
reaching a high effective hit rate well before `REROLL_LIMIT=5` is
exhausted. Combined with 056's clean ground-truth growth floor (415
ticks at water≈1) and a higher water threshold (0.999, not 0.75 — the
champion's "10x short" comment was measured wrong per 046/047's fresh
data), this should land closer to the cluster's ~750-856 ticks/harvest
band than the champion's real ~1,300-1,390.

**Variable.** Champion's Carrot-only escape reroll (`REROLL_LIMIT=2`,
`water<0.75`) → full memory-matched reroll (any type, `REROLL_LIMIT=5`,
`water<0.999`), real target-gated run (not a bounded probe).

**Metric.** The completion modal's displayed time and global rank,
compared to the champion's real 02:47.682-02:52.376 / #130-131.

**Baseline.** Champion (real, this session): 02:47.682 PB / 02:52.376
fresh, #130-131. 056: clean growth floor 415 ticks at water≈1
(unwatered 952). 047: real walk-rate 63% without reroll.

**Procedure.**
1. `saves/hay/main.py`: full reroll-before-walk (memory dict, any
   type), `REROLL_LIMIT=5`, water threshold 0.999, same 32-drone
   spacing-5 layout (champion's proven safe grid).
2. `tools/cycle.sh hay exp-hay-057-r1 --from <worktree>` — real,
   full target-gated run.
3. Read `SHOT=` with vision for time/rank; compare to the champion.

**Falsifier.** If this is also worse over the full real horizon, the
memory-maturity theory is wrong too, and reroll-before-walk is closed
for Hay regardless of time horizon — not just a short-probe artifact.
