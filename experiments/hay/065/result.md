# exp-065 — does the drone-concurrency race ever duplicate a harvest? — result

**Outcome.** No duplication. The race is confirmed lossless-at-best,
never a gain. This closes the last open exploit-adjacent lead.

**Numbers.**

```
START pos 0 0
DRONE_A BEFORE 53049977263 AFTER 53049977775 GAIN 512
DRONE_B BEFORE 53049977263 AFTER 53049977775 GAIN 512
FINAL_HAY 53049977775
```

Both drones read the *same* `BEFORE` and the *same* `AFTER` around their
own `harvest()` call, each showing an apparent gain of 512 — but the
true final total (`FINAL_HAY`, read after both finished) equals that
single `AFTER` value, not `BEFORE + 2×512`. Only one harvest's worth of
yield (512, matching 056's isolated single-tile baseline) was actually
granted across the whole two-drone race. Both drones *executed*
`harvest()`, but only one had any effect on the shared counter — the
other's call was a silent no-op against an already-emptied tile.

**Baseline.** Single-drone harvest of the same isolated setup: +512,
per 056.

**Verdict.** The identical before/after values both drones observed are
themselves informative: it means the concurrent scheduling model
resolves both drones' `harvest()` attempts (whichever succeeds, whichever
no-ops) *before* either one reaches its own `quick_print`, not truly
interleaved at arbitrary granularity — consistent with 046/047's
plant-side finding (a race is a clean win/lose resolution, not a
corruption). No duplication mechanism exists here to exploit, on the
harvest side any more than the plant side. Combined with 062 (no Hay
tradeability, no module-call cost gap), 063 (RNG-seed timing sketched
but impractical and low-value even if perfect), and 064 (seed luck
provably can't beat the growth floor, only worsen it), this closes every
concrete direction raised in the exploit brainstorm. #1's implied
budget remains unexplained by anything found in this investigation —
consistent with the standing read that it reflects a residual or
historical mechanic closed by the Dec 2025 patch, not something
reachable from the current game version. No champion change. Back to
the #2-10 cluster as the honest target.
