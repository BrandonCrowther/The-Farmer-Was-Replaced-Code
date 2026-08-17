# exp-065 — does the drone-concurrency race ever duplicate a harvest?

**Hypothesis.** 046/047 found the known race only ever *fails* cheaply
(a "Cannot plant Carrot on Grassland" 1-tick failure) — but that was
observed incidentally, on the plant side, never deliberately provoked on
the harvest side. If two drones can race to `harvest()` the exact same
ripe tile and both successfully collect yield, that would be a real
duplication exploit — a plausible mechanism for a suspiciously fast
score. If only one ever actually gets the yield, the race is confirmed
harmless and this closes the last open exploit-adjacent lead.

**Variable.** Two drones spawned on the *same* tile (`spawn_drone`
places the new drone at the caller's own position), running identical
code, both racing to `harvest()` the same plant the instant it ripens.

**Metric.** `num_items(Items.Hay)` before/after each drone's own
`harvest()` call, plus the true final total after both have finished —
compared to see whether the total reflects one harvest's yield or two.

**Baseline.** A single drone harvesting the same isolated setup gains
exactly one harvest's yield (512, per 056's isolated single-tile
design) — no ambiguity about what "one harvest's worth" is here.

**Procedure.**
1. `saves/hay/main.py`: `racer(tag)` — till/water/plant/wait for ripe/
   harvest, printing before/after around its own `harvest()` call.
   Spawn one via `spawn_drone`, run the other directly, `wait_for` the
   spawned one, then print the true final total.
2. Smoke test only — no `zzRunner.py` in this deploy, nothing here can
   trigger a real `leaderboard_run()`.
3. `tools/tfwr.sh run`, read `output.txt`.

**Falsifier.** If the final total equals `before + 2×512` (both
harvests landed), that's a real duplication bug worth taking seriously
as a lead. If it equals `before + 512` (only one landed) regardless of
what each drone individually observed, the race is confirmed lossless
at best, and the exploit-hunt is fully closed.
