# exp-003 — reactive-single-tile — result

**Outcome.** adopted as the design baseline, after fixing a real bug found
mid-experiment.

**r1 (buggy — no watering).** Confirmed the free-Grass and full-Bush/Tree-
service logic works (40/40 multiplied), but growth ran at the unwatered
1x rate (~35-42k ticks/cycle, matching Plant-growth.md's 6.0s mean ×
~6,070 ticks/s ≈ 36,420) because the probe never called `use_item(Water)`.
`TICKS_PER_HARVEST` 37,424.65 — not representative, fixed below.

**r2 (watered, un-harvested revisit bug).** With watering added, growth
dropped to the expected range, but **2/40 harvests came back bare (512,
not 81,920)** — both were revisits to a position this drone had already
serviced-then-reverted-to-Grass earlier in the run. `plant()` does not
overwrite an existing entity (even Grass) — a revisited position needs
`harvest()` first, exactly like `Common.py`'s `polyculture_mapped` already
does and this probe's hand-written version omitted. Fixed by adding
`harvest()` before both the companion-service `plant(ctype)` and the
revert-to-Grass `plant(Entities.Grass)`.

**r3 (fixed) — numbers.** **40/40 harvests multiplied (81,920), 100%.**
`HITS_GRASS` 11/40 (27.5%, close to 1/3), `HITS_SERVICED` 29/40. Mean idle
time (16-sample subset) ≈5,940 ticks — **≈71% of the ≈8,362-tick average
cycle is idle wait**, confirming this category is growth-bound, not
servicing-bound, the opposite of hay_single (001: ~0% idle) and much more
pronounced than Hay (041: idle only on ~32% of passes, and only ≈492
ticks there).

**Baseline.** 001: growth ≈7,196 ticks mean, isolated.

**Delta / projection.** `TICKS_PER_HARVEST` 8,361.55 → **9.80 carrots/tick**.
At 1,221 harvests needed (100,000,000 / 81,920), projected total
≈10,209,453 ticks → **≈1,682s ≈ 28.0 minutes** at the ~6,070 ticks/s rate.
No leader time known yet for this category (never checked) — this is a
floor to beat, not a comparison.

**Noise floor.** Not established (single 40-cycle run per variant, and two
of the three runs had real bugs) — worth a longer/second run before
trusting the exact number, though the 100% multiplier rate and the
idle-time magnitude are unambiguous.

**Screenshots.** None — probe.

**Verdict.** Single-tile design works cleanly now, but spends ~71% of its
time idle. Handling cost per cycle (own-tile + companion + revert) ≈
8,362 − 5,940 ≈ **2,422 ticks**, against growth ≈7,196 — a ratio of
**≈2.97**, suggesting **3 tiles could nearly perfectly pipeline** (each
tile revisited roughly every 3×2,422 ≈ 7,266 ticks, matching growth
almost exactly) with idle time driven close to zero. Unlike Hay (044:
idle window too small even for one extra tile) and hay_single (001: no
idle at all), **this is the first category tonight where multi-tile looks
genuinely promising on the numbers, not just plausible.** 004 should build
and test it for real.
