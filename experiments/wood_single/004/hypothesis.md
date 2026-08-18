# exp-004 — measure Tree's real growth time, then apply Hay's playbook

**Hypothesis.** 003 found Tree's own mechanics (no auto-regrow
exception, ~400-tick reroll cost) but left one question open: 001's
34,718-tick isolated growth figure predicted a per-harvest cost far
above the real measured 9,551 for the current single-tile champion, a
~3.9x gap best explained by 001 having measured growth unwatered
(water≈0) — the same mistake Hay's own 019 made before 037 corrected
it 6.7x. If that's right, Tree's real growth time at water≈1 should be
dramatically smaller, and once it's the same order of magnitude as one
tile's own servicing cost (not ~8x it), a multi-tile round-robin —
Hay's own 070 insight — should be able to fully hide it, the same way
it did for Hay/Grass.

**Measurement.** `simulate()` sandbox (clean, isolated — see 003 for
why this matters over the contaminated live world), water sustained at
0.999 throughout via the same top-off loop the design will use.
**Result: 4,412 ticks — a 7.87x reduction from 001's figure.** Confirms
the water-measurement-condition hypothesis directly.

**Design, built on that number.** Applied Hay's full 069 (upfront
pre-seed every reachable position as one free type, accept on a
memory-matched draw, reroll otherwise) + 070 (round-robin multiple
tiles so growth-wait hides behind sibling servicing) playbook to
Tree/Wood for the first time:

- **4 tiles**, not Hay's 2: per-visit servicing (harvest 200 + replant
  200 + reroll chase avg ~3×400=1200 + move 200 ≈ 1800) needs
  `(N-1)×1800 ≥ 4412` to fully hide growth → `N≥3.45` → 4 tiles gives
  ~5,400 ticks of away-time per tile, comfortably above 4,412.
- **Diagonal placement**, not Hay's adjacent offset: `(0,0), (1,1),
  (2,2), (3,3)` relative to spawn — Tree's real, confirmed constraint
  (001) is growth doubling for every tree directly N/E/S/W of another
  (2.44x for one neighbor), *cardinal only*, diagonal is free. Verified
  pairwise non-cardinal offline before writing any code.
- Pre-seed union (42 positions) and reroll logic otherwise reuse Hay's
  exact proven pattern (`hay_single`'s exp-017 tonight), including
  `REROLL_LIMIT=30` (exhaustion `(2/3)^30≈5e-6`, negligible) and the
  constant-comparison reroll check (`planted` is Bush-only by
  construction, same as Hay).
- Water kept at 0.999 (matching the exact condition the growth figure
  was measured under) — not re-tuned down the way Hay's 072 later did,
  to avoid stacking an unverified assumption onto an already large
  change.

**Two real parser bugs hit and fixed during validation** (this
category's own scripting language rejects constructs the codebase
never happened to use before): a list comprehension
(`[expr for i in range(n)]` — not supported, rewritten as an explicit
loop with `.append()`) and a tuple literal passed directly as a
function argument with the tuple's own first element also parenthesized
(`.append(((ax+i)%size, ...))` — "Expected a comma or closing bracket";
fixed by building the tuple in an intermediate variable first). Both
caught by the live validation pass before any real run, exactly the
point of validating.

**Validation.** Live (target = current inventory + 100,000): setup
produced `BASES [(0,0),(1,1),(2,2),(3,3)] PLANTED_COUNT 42` — exact
match to an offline Python re-implementation of the same coverage logic
— then completed cleanly, no warnings. Smoke test (200 cycles, bounded,
not target-based): **2,682.46 ticks/harvest** (windows 2,486–3,039),
vs. the current champion's real 9,551 — a predicted ~3.56x
improvement.

**Baseline.** 002 (current champion): 31:59.849, #232.
