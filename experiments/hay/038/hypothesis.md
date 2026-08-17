# exp-038 — reroll-before-walk-general

**Hypothesis.** Generalising 020's Carrot-only reroll to "reroll toward any
companion this drone already has stocked" (the same mechanism hay_single's
009-012 measured and 011 proved optimal for that category) reduces average
ticks/harvest here too — 031 already showed Carrot succeeds 99.6% of the
time when attempted, so avoiding it specifically no longer targets the real
cost, which is any real ~800-tick walk on a memory miss of any type.

**Variable.** The reroll condition in `driver()`: `companion[0] ==
Entities.Carrot` (020, avoid one type) → `pos in planted and planted[pos]
== ctype` (reroll toward a known hit, any type). `REROLL_LIMIT` unchanged
at 2 for this first test — isolate the criterion change before also
sweeping the limit.

**Metric.** The completion modal's time and rank, same protocol as every
scored Hay experiment. Read `output.txt` warnings too (unchanged code
shape, so warning counts should track 020's for anything that isn't this
specific change).

**Baseline.** 020 (current champion): PB 02:47.682/#130, but that specific
number is flagged as run-condition-dependent (record.json) — the *clean*
baseline is 02:52.323 (mean of 4). Relaunched fresh and running 020
unmodified once (exp-038-baseline) immediately before this variant, so both
are measured under matching (freshly relaunched) conditions rather than
compared across sessions.

**Procedure.**
1. Relaunch (clean conditions).
2. `tools/cycle.sh hay exp-hay-038-baseline --from <autofarmer checkout>`
   (020 unmodified) — establishes today's clean-condition reference point.
3. `saves/hay/main.py`: the reroll-toward-known-hit change.
4. `tools/cycle.sh hay exp-hay-038-r1 --from <worktree>`.
5. Compare both times, run close together under matching conditions.

**Falsifier.** If this variant doesn't beat the fresh baseline from step 2,
Hay's already-higher hit rate (44-66%, from neighbour cooperation — 021)
means there isn't much of the same headroom hay_single had, and the
generalised reroll isn't worth keeping here even though it proved decisive
there.
