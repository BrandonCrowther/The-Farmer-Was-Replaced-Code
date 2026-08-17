# exp-009 — reroll-before-walk — result

**Outcome.** **adopted — a large, real win.** Nearly doubles throughput
over the champion.

**Numbers.** 200 cycles, 15,410,688 hay, 264,326 ticks, 43.51s.
`HITS_INITIAL` 50, `HITS_REROLL` 69, `WALKS` 70, `UNAFFORD` 11 (all early,
before wood accumulated), `REROLLS_TOTAL` 260. `WOOD` reached 1,483,776 —
coverage still grows fine; rerolling did not starve it.

**Tail window (cycles 175-199, fully warmed up — every `GAINED` is 81,920,
100% multiplied):** `(264326-244419)/24 ≈ 829.5` ticks/harvest — barely
half the champion's implied ~1,468. Steady-state throughput
`81,920/829.5 ≈ 98.75` hay/tick.

**Overall (all 200 cycles, warm-up included):** `15,410,688/264,326 ≈
58.31` hay/tick — already beats 008's real 55.8 hay/tick average even
before steady state is reached.

**Baseline.** 008: real scored champion, ≈55.8 hay/tick, ≈1,468
ticks/harvest.

**Delta.** Steady-state throughput is **≈77% higher** than the champion
(98.75 vs 55.8 hay/tick) — close to the ~2x the arithmetic predicted (918
vs 1,600 predicted miss cost; 830 measured against ~1,468 measured, both
directionally and quantitatively in line).

**Noise floor.** Not established — single probe run. Should hold up (the
mechanism — reroll cost vs. walk cost — is structural, not tuned to this
particular random seed), but 010 should watch for it.

**Screenshots.** None — probe.

**Verdict.** The champion's flat "walk on every miss" policy was leaving a
real amount on the table: with a genuine 1/3 structural hit rate (004), most
misses are cheaper to resolve by cheaply re-rolling our own tile (destroy
unripe + replant, ~400 ticks, no travel) than by paying a full ~1,600-tick
round trip — capped at 2 rerolls so the memory still gets new stock often
enough to keep growing. **010 should build this into the real terminating
driver and run it as a scored cycle**, the same way 007→008 did. Rough
projection at steady-state throughput: `100,000,000 / 98.75 ≈ 1,012,700`
ticks → `≈167s ≈ 02:47` — call it an estimate, not a prediction; 008 already
showed the real run can beat its own probe's projection.
