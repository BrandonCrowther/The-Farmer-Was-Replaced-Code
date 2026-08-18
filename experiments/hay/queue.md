# Hay — experiment queue

Target: **2_000_000_000 hay**
Entry point: `main` · Runner: `leaderboard_run(Leaderboards.Hay, "main", 5000)`

Branches: `auto_experiment/hay/NNN` · Results: `experiments/hay/NNN/result.md`

## Queued

- [x] 062 exploit-candidate-probe — **both candidates closed, no
      champion change.** User pushback: since boards were reset, #1's
      post-patch time should be replicable if it rests on a residual
      version of a patched exploit — worth checking before assuming
      it's out of reach. (a) Direct Hay tradeability: not a real
      mechanism — `get_cost()` only accepts `Entity`/`Unlock`, never a
      bare `Item` (confirmed live, errors on `Items.Hay`), and there is
      no `trade()`/`sell()`/`buy()` in the builtin API at all. (b)
      Module-function-call cost gap (checking for a residual version of
      the patched "free function calls in dynamic modules" exploit):
      none found. `Common.move_to()` costs exactly its real body work
      (228 ticks = 200 move + 28 getter/comparison overhead), and
      indirect-via-variable costs exactly +1 tick over direct-by-name —
      identically for a local function (200→201) and an imported-module
      function (228→229) — matching Operation-Costs.md's documented
      rule precisely, no discount or gap. `experiments/hay/062/result.md`

- [x] 063 rng-seed-mechanism — **mechanism identified, not pursued.**
      Decompiled `Core.dll` (Mono IL, static inspection only): every
      `leaderboard_run()` hardcodes `seed = -1` at the call site
      (confirmed in the compiled IL itself, not just the wiki), which
      forces Mono's parameterless `System.Random()` — seeded from
      `Environment.TickCount` (system uptime), not wall-clock date/time
      as originally guessed. All other RNG streams (growth, maze,
      companion draws, everything) cascade from that one root value via
      `.Next()` calls in a fixed order. A theoretical exploit sketch
      (offline seed search via `simulate()`, invert seed→TickCount, time
      the `leaderboard_run()` trigger to land on a chosen tick) was
      **not attempted** — it needs unverified sub-millisecond timing
      through several jittery layers, and even a perfect hit would only
      control one of a 2-hour session's 100+ averaged repeats (the
      "average of all runs over 2 hours" scoring rule dilutes it to
      ~1% or less of the final score). Closed on both practical grounds
      and the standing concern about manipulating a shared public
      leaderboard. Full writeup: `docs/RNG-Seed-Mechanism.md`.

- [x] 064 seed-luck-vs-growth-floor — **RNG-luck theory falsified,
      closes the exploit-hunt for real.** User's follow-up: if #1's
      budget only makes sense as an exploit, and RNG is the mechanism,
      could a seed be forced favorable enough to explain it (e.g. by
      controlling system uptime, "freezing the clock")? Tested directly:
      swept `simulate()`'s legitimate seed parameter across 24 values,
      measuring 056's isolated single-tile growth-time floor at each one
      (sandboxed — never touched the real farm or live leaderboard).
      Result: 20/24 seeds landed on the same floor value, 4/24 landed on
      *exactly double* it (one whole extra growth-cycle) — **no seed
      went below the floor.** RNG luck only ever costs a full cycle, it
      never saves one. That, plus 063's own practicality problems
      (unverified sub-ms timing, and the 2-hour repeat-averaging rule
      capping any one controlled seed to ~1% of the final score), means
      the seed-timing exploit has nothing to exploit even in the most
      generous reading. `experiments/hay/064/result.md`

- [x] 065 harvest-race-duplication-check — **no duplication, exploit-
      hunt fully closed.** Last open brainstorm direction: could the
      known drone-concurrency race (050) be provoked deliberately to
      duplicate a harvest, rather than just tolerated as a rare loss?
      Tested directly: two drones spawned on the *same* tile, racing to
      `harvest()` the same ripe plant. Both executed `harvest()` and
      each *locally* observed a 512 gain around their own call — but the
      true final total after both finished was `before + 512`, not
      `before + 1024`. Only one harvest ever actually lands; the loser's
      call is a silent no-op against an already-emptied tile. Confirms
      046/047's plant-side finding generalizes to harvest: the race
      resolves cleanly (win/lose), never corrupts or duplicates.
      `experiments/hay/065/result.md`

- [x] 066 grass-auto-regrow — **CORRECTION: the "400-tick own-handling
      floor" claimed throughout 046-065 is wrong. Real cost is ~207.**
      User pushback, tested directly: `Grass.md` says "Grass grows
      automatically on grassland" — `harvest()` never leaves the tile
      empty, `get_companion()` rerolls fresh every cycle with no
      `plant()` call, and the champion's `instructions()` call after
      `harvest()` is a guarded `plant()` whose guard *always* skips
      (entity_type never leaves Grass) — measured at **7 ticks, not
      200**, in 6/6 cycles. True own-handling: harvest (200) +
      instructions (7) ≈ **207**, not 400. This halves the reroll cost R
      used in every servicing-cost estimate since 046: `S = R(1-p)/p`
      drops from ≈800 to ≈414, and the zero-servicing floor (own-
      handling + 415 growth) drops from ~815 to **~622** *in the
      idealized case*. Does **not** overturn 051/053-055/058-061's
      specific results (real measured game runs, unaffected by a wrong
      model) — see 068 below for why the "real headroom" conclusion
      drawn here at the time did not survive direct measurement.
      `experiments/hay/066/result.md`

- [x] 067 reroll-pattern-validation — confirms 066's 207-tick number in
      the champion's *exact* reroll usage (harvest with no ripeness
      check, on a just-regrown tile): still 200 ticks, 0 yield, still
      auto-regrows after. No correction needed to 066.
      `experiments/hay/067/result.md`

- [x] 068 real-ticks-per-harvest — **corrects 066's "real headroom"
      claim: it was premature.** Directly measured the unmodified
      champion's real ticks/harvest, single drone, 900 cycles (matching
      a full run's ~871/drone), windowed every 150. Memory saturates by
      cycle 300 (~23-24 of ~25 reachable positions) and never grows
      further, so cycles 300-900 *are* steady state — and steady-state
      ticks/harvest plateaus at **~1070-1220**, nowhere near the
      corrected 622 floor, or even the old 815 one. Cause: **17.2% of
      cycles exhaust all 5 rerolls with no memory hit** even at full
      maturity (vs. ~8.8% a naive independent-draw model at p=1/3
      predicts) and fall through to a real walk (200-1200 ticks) next
      cycle — a structural tax the operation-cost floor treated as
      avoidable. 066/067's *operation* costs (207, not 400) are still
      correct and stand; the *conclusion* drawn from them ("real room,
      not a wall") does not, and is retracted. `experiments/hay/068/result.md`

- [x] 069 bush-wall-spatial-preseed — **user's design, tested in two
      variants, closes the accept-policy family for real.** Proposal:
      pre-seed every n=2/n=3 reachable position (20 of 24) with
      permanent Bush before the loop starts, leaving only the 4 n=1
      tiles genuinely dynamic — accept a draw the instant it's either a
      memory-matched Bush at n=2/3 (free) or any type at n=1 (cheap to
      walk); reroll everything else. Predicted accept probability
      32/72≈0.444 vs 068's measured ~0.288 — confirmed almost exactly
      (avg rerolls/cycle dropped from 1.93 to 1.19, exhaustion rate
      0%). But total ticks/harvest barely moved (1069.57 vs 068's
      ~1070-1220): 230/900 cycles needed a real ~800-tick walk to
      service the n=1 tile (its type changes almost every draw), which
      ate the reroll savings almost exactly. Follow-up v2 (all 24
      positions static, zero walk ever): reroll rate rose back to
      ~2.07/cycle (matches the p=1/3 prediction with the n=1 shortcut
      removed, `(1-1/3)/(1/3)=2.0`) and total landed at 1068.35 —
      predicted 1043.72 from the corrected model, within 2.4%. Three
      independently structured designs (natural accumulation, hybrid,
      fully static) now converge on the same ~1000-1200 band, for three
      different, well-understood reasons — a real conservation trade
      between reroll cost and walk cost, not a coincidence. Combined
      with the eight earlier real-measured rejections (051, 053-055,
      058-061), this is convergent evidence of a genuine structural
      ceiling on accept/reroll policy design given the current
      24-position/3-type/207-reroll/~800-walk mechanics — not fixable
      by policy alone. No champion change. `experiments/hay/069/result.md`

- [x] 070 two-tile-interleaving — **first real gain in this whole
      family: ~10% below 069v2's ceiling.** 069 closed accept/reroll
      *policy* — this changes the macro-layout instead. Ticks are a
      single global clock; growth is passive and doesn't care where the
      drone is. A single-tile drone wastes its 415-tick growth wait
      doing nothing; a drone alternating between two adjacent tiles
      (distance 1, shared all-static-bush wall, 30 tiles covering the
      union of both radius-3 diamonds) can spend that wait servicing the
      sibling tile instead — a single sibling visit (~628 ticks, no
      walk) already exceeds 415, so growth is fully hidden. Predicted
      ~815-828 ticks/harvest; measured **959.57**, avg rerolls/cycle
      2.003 (matches p=1/3 almost exactly, confirming the reroll math is
      unaffected by adding a tile). The 145-tick gap from prediction is
      most likely water decaying further over the longer inter-visit
      interval, requiring more top-up per visit — plausible, not yet
      directly instrumented. Still a genuine, reproducible win over
      069v2's 1068.35 — the first one since 057 in this entire
      investigation. Doesn't yet reach the #2-10 cluster's 750-856 band.
      `experiments/hay/070/result.md`

- [x] 071 breakdown-instrumentation — **070's water-decay theory was
      wrong; the real gap is simpler and now fully attributed.** Direct
      category breakdown (water/wait/harvest/reroll/move, each timed
      separately) instead of another guess. `wait≈1` confirmed growth is
      fully hidden as predicted. But `water=62.76`/harvest (0.276
      `use_item()` calls/harvest) was real and simply never modeled at
      all — not a two-tile-specific effect, just an unmeasured cost that
      exists in the single-tile design too. `move=226` vs the 200 a bare
      distance-1 hop should cost — `Common.move_to()`'s wrapper carries
      ~26 ticks of avoidable overhead. `reroll=482.63` (avg 2.14
      rerolls/cycle) is within normal variance of 069/070's numbers, not
      a new finding. Sum of real gaps (~155) closely matches the
      observed 145-tick shortfall. `experiments/hay/071/result.md`

- [x] 072 water-and-move-optimization — **both fixes confirmed almost
      exactly as predicted — real ~7.6% improvement.** Water threshold
      0.999→0.75 (safe: growth still finishes in ~518 ticks, comfortably
      inside the ~900-tick away-window `071` confirmed is idle) and
      `Common.move_to()`→direct `move()` for the known single-hop
      direction. Result: water 62.76→9.66 (`WATER_CALLS` 248→16, a
      15.5x drop), move 226→201 (essentially the 200 floor), `wait`
      unchanged at 1 (the lower threshold didn't push growth past the
      away-window). **Total: 999.41→923.53 (-75.88, -7.6%)** — now only
      67.5 ticks above the #2-10 cluster's upper bound (856).
      `reroll` (484.85, ~52% of total) is now clearly dominant and
      already at 069's p=1/3 structural floor. `experiments/hay/072/result.md`

- [x] 073 first-real-run — **ADOPTED, new champion. 02:00.734, #65 (was
      02:42.421, #111) — -41.687s (-25.7%), +46 ranks.** Built the full
      32-drone two-tile version, reusing the champion's existing
      spacing-5/6x6/HOLES grid with each drone's second tile at
      base+(1,0). The macro-layout collision risk flagged at the end of
      070 (a drone's bush-wall reaching within 1 tile of a same-row
      neighbor's own crop at 5-spacing) was fixed with a global
      `ALL_CROPS` exclusion set every drone's setup checks against, not
      just its own two tiles — geometry alone (1-tile margin) was
      judged too tight to trust. Validated live before the real attempt:
      a target-reduced, `zzRunner`-removed run confirmed zero crop-tile
      collisions across all 64 tiles. The real run then confirmed the
      entire chain from 066-072 (207-tick reroll cost, 615-tick floor,
      growth-hiding, water/move optimizations) generalizes from
      single-drone smoke tests to the real macro-layout on the first
      attempt. `experiments/hay/073/result.md`

- [x] 074 real-champion-measurement — **confirmed and better than
      predicted.** The exact deployed `main.py` logic (no measurement-
      harness overhead), single drone, 900 cycles: **889.78
      ticks/harvest**, beating 072's instrumented 923.53 by 33.75 —
      close to the ~27-tick bookkeeping cost 071 identified, within
      normal variance. Now only **33.78 ticks above the cluster's upper
      bound (856)**. Cluster reference was already re-confirmed fresh:
      exp-073's own completion screenshot (captured live, moments
      before this entry) showed #2-10 unchanged at 01:27.694-01:48.665
      — no re-check needed, the board hadn't moved. No further concrete
      lever identified: `reroll` is the dominant, structurally-floored
      cost (069's p=1/3 analysis), REROLL_LIMIT retuning doesn't change
      the average (only an already-negligible `(2/3)^30≈5×10⁻⁶`
      exhaustion tail), and 3+ tile round-robins were already reasoned
      (070) to give no further gain since one sibling's service time
      already exceeds the growth floor. Treated as the practical
      ceiling for the two-tile-interleaving paradigm absent a new
      structural idea. `experiments/hay/074/result.md`

- [x] 075 drop-instructions-noop — **ADOPTED, new champion. 01:58.059,
      #63 (was 02:00.734, #65) — -2.675s, +2 ranks.** "No further
      concrete lever identified" in 074 was wrong — 066/067 already
      proved Grass auto-regrows and a bare `harvest()` (no ripeness
      check) correctly destroys/regrows it every time, but the champion
      still called `instructions()` (a guarded, always-false `plant()`
      check) once after every harvest *and* once per reroll attempt —
      ~3.1 calls/harvest × 7 ticks ≈ 22 ticks of pure overhead that was
      simply never removed when 073 was built, despite the underlying
      fact being known since 066. Removed every `instructions()` call
      except the two that plant Grass on empty ground for the first
      time. Single-drone smoke test: 873.02 ticks/harvest (down from
      074's 889.78, -16.76) — now only **17.02 ticks above the
      cluster's upper bound (856)**. Validated live (zero crop
      collisions) before the real attempt, same as 073.
      `experiments/hay/075/result.md`

- [x] 076 setup-phase-movement — **ADOPTED, new champion. 01:57.195,
      #60 (was 01:58.059, #63) — -0.864s, +3 ranks.** User review of the
      setup/spawn phase (not the hot loop) found two real issues: (a)
      the initial long walk from each drone's spawn point to its base
      tile used `Common.move_to()` — unwrapped, always the direct path
      — instead of `Common.move_to_wrapped()`, paying a much longer
      walk than necessary for far-corner assignments on the 32-wide
      farm; (b) `move_to()` also carries a leftover `protocol()`
      indirect-call parameter and a `num_unlocked(Unlocks.Mazes)` check
      on every move, for a maze-avoidance feature this category never
      uses — `move_to_wrapped()` has neither. Every `Common.move_to()`
      in `driver()` switched to `Common.move_to_wrapped()`. Picked back
      up after the prior session's crash-interrupted attempt: validated
      first (target=200,000, `zzRunner.py` swapped for a bare `import
      main`, an arrival check after every `move_to_wrapped` call) —
      64/64 checks clean, 0 mismatches, `SPAWNED 32 of 32`, no warnings
      — then run for real. Small win, exactly as expected for a
      setup-phase-only fix on top of an already-tuned hot loop.
      `experiments/hay/076/result.md`

- [x] 077 spawn-tree-parallelization — **ADOPTED, new champion. 01:56.890,
      #59 (was 01:57.195, #60) — -0.305s, +1 rank.** "Summoning" half of
      the two-part 077 idea. 073's one drone sequentially spawned all 31
      others (measured live: `spawn_drone()` costs a flat 200 ticks
      isolated, matching Operation-Costs.md's generic function-cost row;
      the real 31-call loop cost 6745 ticks total, close to 076's ~6200
      estimate). Replaced with a binary spawn tree — each drone keeps one
      position for itself and spawns ≤2 children with the rest, so depth
      is `ceil(log2(32))=5` instead of 31 sequential calls on one drone.
      Validated live first (32/32 unique positions matching the expected
      grid, no dupes/gaps, max child latency 443 ticks vs 6745 old)
      before the real run. Smaller than 076 (-0.864s) because this
      removes one shared one-time critical-path constant, not a
      per-drone cost ×32. `experiments/hay/077/result.md`

- [x] 078 shared-bush-wall-territory-partitioning — **REJECTED,
      analytical closure, no live run.** "Spacing" half of the 077
      review. A genuine walk-skipping partition needs a non-owning drone
      to trust a shared tile is already planted without visiting it —
      the API has no remote tile read (`get_entity_type()` only reads
      the current position), so the only way to skip the walk is to
      trust an ownership rule blind. That's a real correctness bug, not
      a perf trade: 077's own spawn tree made drone setup order provably
      unordered (043's tick-rate-parallelism finding + 050's confirmed
      no-shared-state + no cross-drone sync primitive beyond `wait_for`
      on a direct child), so a drone could draw a companion request for
      a neighbor-owned tile before the neighbor has planted it, silently
      `break` out of its reroll-chase believing it's satisfied, and lose
      the multiplier on that harvest with zero warning — the same shape
      as the polyculture bug `docs/LOOP.md` already warns about. Even
      race-free, the trade looks like a loser anyway: 069 already
      measured that *reducing* proactive tile coverage (its 20/24
      partial pre-seed) barely beat no coverage, because uncovered
      positions' real walk cost ate the savings — full coverage won.
      Closed without spending a real run to re-derive a conclusion
      three separate already-measured results already implied.
      `experiments/hay/078/result.md`

- [x] 079 stray-tick-scour — **ADOPTED, new champion. 01:56.092, #58
      (was 01:56.890, #59) — -0.798s, +1 rank.** Three fixes, all
      provable behavior-preserving by reading the code (no new game-
      mechanic assumption, unlike 078's rejected idea): (1) reroll
      chase's `planted[key] == ctype` was a second tuple-keyed dict
      lookup re-deriving a value that has exactly one write site in the
      file (always `Entities.Bush`) — replaced with a direct constant
      comparison; the one change here that touches the hot loop.
      (2) bush-wall setup computed both `wdist()` calls (~11 ticks each)
      unconditionally even though `or` already short-circuits — skip
      the second once the first already qualifies. (3) bush-wall setup
      cached a doubled `get_entity_type()` call. Single-drone smoke test
      (884.06 ticks/harvest, window range 849-910) was too noisy to
      detect the ~1.3-tick/harvest predicted hot-loop effect and blind
      to the setup-only fixes by construction, but validated live for
      correctness (32/32 unique positions, unchanged) before the real
      run confirmed a clear win. `experiments/hay/079/result.md`

- [x] 080 precompute-near-offsets — **TIED, not adopted.** Moved the
      bush-wall setup's per-drone `wdist()`-based window scan (56 cells,
      up to 2 calls each) to a module-level `NEAR_OFFSETS` precompute,
      the same pattern `ALL_BASES`/`ALL_CROPS` already use — motivated
      by 077's own validation showing spawned children don't re-pay for
      `ALL_BASES`/`ALL_CROPS`'s build cost, implying module-level state
      is shared, not recomputed per drone. Proven byte-identical to the
      old scan offline (Python, 6 base positions incl. seam-crossing
      corners) and live-validated (32/32 drones, 30 tiles each, clean).
      Real runs: r1 01:56.077/#58 (-0.015s), r2 01:56.149/#58 (+0.057s)
      — both under the 0.069s noise floor, opposite directions, the
      textbook noise pattern. Not adopted (exp-060's precedent: a tie
      doesn't merge even when the reasoning behind it is sound) — but
      not wrong either; either 077's "shared module state" reading was
      too strong, or the real saving is genuine but too small a share of
      the ~2h-averaged score to clear this floor. Suggests the
      *setup*-phase's remaining stray-tick budget specifically may be
      near exhausted, separate from the hot loop's (where 079's fix
      *did* clear the floor). `experiments/hay/080/result.md`

- [x] 081 drop-redundant-target-check — **ADOPTED, new champion.
      01:55.779, #57 (was 01:56.092, #58) — -0.313s, +1 rank.** Of the
      hot loop's three `num_items(Items.Hay)</>=TARGET` checks per
      iteration, removed the one guarding only the cheap final `move()`
      call, keeping the one guarding the much more expensive
      harvest+reroll chase — the asymmetric, lower-risk half of the
      idea flagged in 080's entry. ~2600 ticks/drone recurring over
      ~871 harvests, real hot-loop cost unlike 080's one-time setup
      relocation. Not a pure equivalence proof like 079/080 — validated
      live instead (couldn't use the real 2B target: persistent save
      inventory is already ~53.8B, so the loop would never even enter):
      single-drone and 32-drone runs at inventory+3M/+30M targets both
      completed cleanly with small bounded overshoot (45,376 and 94,848
      respectively, both under two satisfied-harvest yields), no hang.
      Real run cleared the noise floor, closer in size to 079's win than
      080's tie. `experiments/hay/081/result.md`

- [x] 082 water-check-reorder — **ADOPTED, new champion. 01:55.590,
      #56 (was 01:55.779, #57) — -0.189s, +1 rank.** The water top-off
      guard, `num_items(Items.Water) > 0 and get_water() <
      WATER_THRESHOLD`, paid both getters every iteration because the
      almost-always-True operand (water is genuinely fine, 046/047) was
      checked first, never triggering `and`'s short-circuit; the
      almost-always-False operand (072: only 16/871 cycles actually
      need a top-up) was checked second. Swapped order — pure boolean
      commutativity, same truth value, same safety, but the common
      no-op path now skips `num_items()` entirely. Same proof class as
      079/081 (short-circuit is a documented, already-confirmed
      language rule), validated live for a sanity check regardless.
      `experiments/hay/082/result.md`

- [x] 083 water-threshold-retune — **CLOSED, no code change.** One live
      probe plus three analytical checks, none found anything safe and
      worth a real run: (1) `WATER_THRESHOLD` — measured `WATER_CALLS
      16/900`, `WAIT_TICKS 0`, but `MIN_WATER 0` — the tile's own water
      already touches its floor at the current 0.75, no slack to lower
      it without risking real idle wait; (2) 3+ tiles per drone —
      re-derived against current numbers, still closed (070's reasoning
      holds: servicing cost, not growth-wait, is the bottleneck, and a
      3rd tile doesn't touch that); (3) beating the 1/3 reroll floor by
      pre-seeding a mix of companion types instead of all-Bush — ruled
      out algebraically (`P(drawn type == a fixed-in-advance preset) =
      1/3` for any single-type-per-position assignment, so all-Bush is
      already optimal among this whole strategy class); (4) dropping
      the `key in planted` check now that `NEAR_OFFSETS` covers the
      full draw window — unsafe, `ALL_CROPS` exclusions mean coverage
      isn't actually total, and skipping the check risks silently
      claiming an unearned multiplier (the polyculture-bug shape).
      `experiments/hay/083/result.md`

- [x] 084 reroll-check-reorder-and-tuple-reuse — **ADOPTED, new
      champion. 01:54.669, #53 (was 01:55.590, #56) — -0.921s, +3
      ranks — the largest single stray-tick fix since 079 itself.**
      Prompted by the user asking to re-derive the reroll floor from
      scratch rather than take 083's closure as final — re-reading the
      accept-check's own three lines with fresh eyes (not a new area
      of the code, the *same* lines 079 already touched) found two
      more instances of 079's exact class: `key = (cx, cy)` rebuilt a
      tuple identical to one already inside `companion` (bind `pos`
      directly instead); and `key in planted and ctype ==
      Entities.Bush` had the AND ordered against the actual
      probability distribution (`ctype==Bush` is False 2/3 of the
      time, 069) instead of with it, so it almost never short-
      circuited — same trick as 082's water-check reorder. Smoke test
      was inconclusive (865.09 vs 082's 873.02, inside window noise)
      but the real run cleared the floor decisively.
      `experiments/hay/084/result.md`

- [x] 086 shared-territory-two-phase-spawn — **REJECTED, +0.966s
      regression.** User-proposed: partition the bush-wall so each of
      the 32 drones only plants its own ~2/3-3/4 share (a hand-rolled,
      offline-verified `OWNED_OFFSETS` literal table — zero runtime
      computation, per the user's explicit correction against building
      it live), with a genuine two-phase spawn-tree barrier (setup tree
      fully joins before a fresh hot-loop tree starts) closing the
      exact race 078 rejected the same underlying idea over. Offline
      verification and live validation (target=200,000) both passed
      clean — 32/32 unique setup/hotloop markers, barrier holds exactly
      as designed, zero correctness issue found. Lost anyway: the real
      walk-count reduction (960→756 candidate visits, 21.3%) was real
      but small and local, while the second, independent spawn tree
      Phase 2 needs plausibly pays a farm-diameter-scaled "walk back
      out to my own base" cost 085's single-tree design never pays
      twice — validation trace shows 2x+ variance in per-drone
      hot-loop-start ticks (3294-7880), consistent with that story
      though not isolated to confirm it precisely. Confirms 078's race
      concern was real and *can* be engineered around safely, but not
      that shared planting is worth its structural cost in this
      design's shape. `experiments/hay/086/result.md`

- [x] 085 setup-tuple-reuse — **ADOPTED, new champion. 01:54.587, #52
      (was 01:54.669, #53) — -0.082s, +1 rank.** Applied 084's exact
      lesson one loop up: the bush-wall setup built `(px, py)` as a
      fresh tuple twice (the `ALL_CROPS` check, then the `planted`
      write) — built once, reused. Setup-phase only, so expected likely
      unmeasurable per 080's precedent (a ~30x larger setup change that
      tied) — tried anyway, free and safe, per the user's "micro
      optimizations still count" instruction. Real runs disagreed with
      the floor but agreed with each other: r1 -0.039s (under the
      0.069s floor alone), r2 -0.082s (clears it) — both negative,
      unlike a genuine tie (080's r1/r2 disagreed in *sign*). Adopted
      on the strength of consistent direction across the required
      re-run. A routine "Fatal error in GC" crash hit between r1 and
      r2 — recovered via `relaunch` + redeploy per `docs/LOOP.md`, no
      data lost. `experiments/hay/085/result.md`

- [x] 087 same-tree territory partition — **REJECTED, analytical
      closure with live-probe numbers, no scored cycle spent.** Every
      buildable same-tree coordination mechanism (shared flag: dead on
      arrival per 050; adjacency-following tree redesign: +490 ticks
      of live-probed spawn latency alone; same idea on today's
      unchanged tree: 44/204 free tiles but ~139,000 ticks of
      subtree-ripple cost against ~37,000 saved, a ~4x net loss;
      dedicated signal-drone + `has_finished()` poll: needs a spare
      drone slot the existing 32-of-32 `max_drones()` budget has no
      room for without going fully phased, i.e. 086's shape again) is
      closed. **This closes the whole 078/086/087 shared-territory-
      planting family** — not "same size class," a structural dead
      end, now backed by measured constants (~850 ticks/candidate-
      visit, ~200-210 ticks/spawn, the 32-drone hard cap, real
      subtree-size data). Also directly closes the same-session
      proposal to compact the plot into tighter 2D blocks to increase
      shareable boundary — that's a geometry change and doesn't touch
      the mechanism problem, which is what actually blocks every
      variant regardless of layout. `experiments/hay/087/result.md`.
      **Next line of attack for Hay needs to change shape entirely**,
      per `docs/LOOP.md`'s "three same-family rejections" rule (078,
      086, 087 all reject this one family) — not another sharing
      topology.

## Closing state, 2026-08-18 (076-085, overnight session)

Champion: **01:54.587, #52** (was 01:58.059/#63 at session start —
-3.472s, +11 ranks across 076/077/079/081/082/084/085; 078/080/083
rejected/tied/closed with no champion change but real information
gained). Eight real adopted wins in one night. Progress did NOT
monotonically shrink the way it first looked — 084 (-0.921s) came
*after* 083's own "closing scour" and was bigger than 081 or 082
individually, found by re-deriving the reroll floor from scratch
rather than trusting the earlier closure; 085 then found one more
instance of 084's own pattern one loop up, small but real (needed two
same-direction runs to trust, given the floor). **The lesson: "closed"
means "nothing found in this pass," not "nothing left" — re-reading the
same few hot-loop lines with fresh eyes is still worth doing before
concluding the well is dry, and the yield can genuinely still surprise
(084 was the biggest win of the whole scour, not the smallest).** Now
only **5.922s** above the cluster's slow end (01:48.665) — genuinely
close.

**What's been checked, and how thoroughly:** every safe, code-provable
stray-tick fix findable by close reading of `driver()` and its
bush-wall setup — guard checks that never vary, missed short-circuits,
doubled getters, redundant target checks, unfavorable AND-operand
ordering, unnecessary tuple rebuilds (now checked in both the hot loop
and setup). 083 also closed the three most plausible *macro*-level
ideas still sitting in this design's neighborhood (more tiles, mixed
companion pre-seeding, dropping the position check) analytically,
without needing a real run for any of them. Two consecutive re-scours
(084, 085) both found something — **the next tick should scour once
more** (the water-check block hasn't been re-read since 082 wrote it;
the setup loop's `move_to_wrapped`/`plant_companion`/`instructions`
call sites haven't been re-read since 076) before trusting a third
closure.

**What would actually move the needle beyond stray-tick scouring:**
nothing left inside the two-tile-interleaving + full-Bush-pre-seed +
reroll-based-servicing paradigm's *macro shape* — 069's 1/3 reroll
floor is a proven mathematical minimum for this approach, not a tuning
target. Closing the remaining ~6s gap to the cluster needs either more
stray-tick material (increasingly plausible, given 084/085) or a
genuinely different macro-design — e.g. a servicing strategy that
doesn't pay a per-visit reroll/harvest/move cost at all, or some
mechanism not yet identified. No macro-design idea has enough evidence
behind it yet to attempt blind; per `docs/LOOP.md`'s empty-queue rule,
this is recorded as the fork rather than forced. #1's implied budget
remains unexplained by anything found in 062-065 and is out of scope
(likely a pre-patch residual exploit, see record.json's note).

**#1 (`const arch *`, 00:58.549) is very likely not honestly
achievable under current mechanics** — web research (2026-08-17, user's
suggestion) found the game's Dec 4 2025 "Leaderboard Rebalance" patch
reset all boards specifically because old times used three mechanics
since patched: a shared-memory bug between drones (independently
confirmed structurally closed tonight, 050), an RNG made "harder to
break" (not "unbreakable"), and a zero-tick computation exploit via
dynamic-module function calls. This cleanly explains why #1's implied
~409-466 ticks/harvest budget sits *below* even our zero-servicing
floor (815) — not a design gap on our end. The #2-10 cluster
(01:27-01:48, ≈750-856 ticks/harvest) is the honest target and remains
the goal; #1 is out of scope going forward.

**Standing summary after 038-057, continued past the "leader-gap-
unexplained" checkpoint at the user's explicit request** (a persistent
3x gap on a bounded, fully-discoverable mechanic set implies a missed
mechanism, not an unknowable one). Real findings from this pass:
water is genuinely fine (0.8-1.0, not "10x short" as the old
championcode comment claimed — 046/047), tick rate and every unlock
level (including `Speed` and `Fertilizer`, never checked before) are
confirmed maxed/constant (043, 048, 052), a real concurrent-drone race
causes ~9-47 "Cannot plant Carrot on Grassland" failures per run (real
but small, <0.2% of harvests), tighter drone packing and distance-
aware reroll (alone or combined) all measured *worse* (051, 053, 054,
055 — thrashing/reroll-cost effects dominate), and — the one real
positive result — memory-matched reroll-before-walk, retested with the
correct full-run time horizon after a short bounded probe
under-measured it (049 vs 057), is a genuine **-3.1% wall time, #130→
#111** win. `experiments/hay/046` through `057/result.md` have the
full trail. Growth floor is now clean-measured (056): 415 ticks at
water≈1 (not ~608-724 as derived from the wiki's raw seconds table),
putting the *cluster* target within reach of a servicing-cost-focused
push (058), while the #1 gap remains genuinely unresolved by anything
found so far and is being set aside per the user's guidance.

- [x] 044 multi-tile-scheduled — **rejected, with a precise reason.**
      Tested the actual scheduled-second-tile design 041's idle-time
      finding motivated: only visit tile B (distance 1) during A's
      measured ~492-tick idle window, never on A's expensive cycles.
      Real result: **1,342.73 ticks/harvest — worse than the 1,300
      baseline.** The idle window (492) is smaller than even the
      *cheapest possible* B-visit cost (own-handling 400 + minimum
      commute 400 = 800) — a 308-tick shortfall that no scheduling
      refinement fixes. Closes multi-tile-per-drone for Hay for a sharper
      reason than hay_single's (which had zero idle time; Hay has real
      idle time, just not enough of it). Casts doubt on 039's
      ~2.2-tiles-per-drone reading of the leader-implied ~441 figure — the
      leader's edge is not "champion + a scheduled second tile."
      `experiments/hay/044/result.md`.
- [x] 043 tick-rate-check — **rejected the shared-compute-budget
      hypothesis, decisively: tick rate is identical (6,074.97/s to 6 sig
      figs) solo vs. with all 31 other drones actively farming**, and
      matches hay_single's own directly-measured rate. 041's ~3x
      growth-time gap vs hay_single is real but not caused by this; the
      leader-implied ~441-ticks/harvest estimate (039) is unaffected since
      it never depended on cross-category tick-rate comparability.
      `experiments/hay/043/result.md`. (Hit and recovered from a genuine
      infinite-loop bug — unbounded spawned-drone loop meant the run never
      ended on its own, and Shift+F5 doesn't stop a leaderboard run,
      confirming docs/LOOP.md; recovered with `relaunch`, no data lost.)
- [x] 041 growth-schedulability — **the old, never-run 037, finally
      answered: unlike hay_single, real idle time exists here.** On the
      ~68% of passes that miss (real walk), idle ≈3 ticks, matching
      hay_single. But on the ~32% of passes that hit (memory skip), idle ≈
      **492 ticks average** — the drone finishes servicing almost
      instantly and then genuinely waits for the plant to ripen. This is
      the slack hay_single structurally never had (001), and it's why
      hay_single's four-way multi-tile closure does not automatically
      transfer here. `experiments/hay/041/result.md`.
- [ ] 042 multi-tile-per-drone — design a layout that adds a second tile
      *scheduled to fill the ~492-tick idle window on hit-cycles only*,
      not a blind second plot the way 027/029 were (030's postmortem: they
      failed because idle time was assumed, not measured — now it's
      measured). Converges with two independent estimates: 039's
      leader-implied ~441 ticks/harvest and the old queue's own "leader
      implies ~2.2 tiles per drone at 466 ticks."
      Falsifier: if a scheduled second tile still doesn't beat the
      champion, the ~492-tick window may be real but too unpredictable
      (which pass will hit, decided by the same 1/3 RNG confirmed twice
      tonight — 013, 040) to reliably schedule around without adding
      commute cost on misses too.
- [x] 039 drone-tick-profile — measured the main drone's real steady-state
      cost: **≈1,300 ticks/harvest**. Cross-checked against the real
      leader time (00:58.549, confirmed on-screen, never previously
      recorded here): implies **≈441 ticks/harvest for the leader**, only
      ~41 above the bare own-tile floor. `experiments/hay/039/result.md`.
- [x] 040 draw-pattern-check — **rejected the "multi-drone breaks the
      draw" hypothesis, decisively.** 12,600 pooled samples (300 x 42
      internal repeats) on the main drone with all 31 neighbours active:
      type freq within 0.7% of 1/3, 24 positions, no autocorrelation —
      cleaner than 013's own solo confirmation. The draw is IID-uniform
      regardless of drone count. **039's ~441-tick leader estimate is not
      explained by "beating the draw"** — its same-drone-count /
      same-harvest-share assumption is the more likely weak point, or the
      leader's edge is something structurally different from anything
      tested tonight. `experiments/hay/040/result.md`.
- [ ] 041 (open) — re-examine 039's harvest-count assumption (does the
      leader necessarily use 32 drones with an even ~763-harvest share
      each?), or look for a genuinely different mechanism (yield beyond
      81,920/harvest, a layout that changes per-drone harvest count, or
      something not yet considered) before spending more cycles on
      companion-servicing tuning — that line is now closed twice over
      (038's rejection, 040's IID confirmation).
- [x] 038 reroll-before-walk-general — **rejected**, 02:52.510 vs a fresh
      02:52.338 baseline (+0.172s, ≈2.5 noise-floor sd, small and
      negative). Ported hay_single's decisive reroll-before-walk win
      (009-012: solo hit rate ~25-33% baseline, ~77-90% throughput gain)
      by generalising 020's Carrot-only reroll to "reroll toward any
      companion already in `planted`". Didn't help here: Hay's baseline
      hit rate is already 44-66% via 021's neighbour-cooperation effect,
      leaving little slack for a cheap reroll to capture, and the extra
      reroll attempts on passes that were never going to hit cost more
      than they saved. `experiments/hay/038/result.md`. Not merged.
- [x] 035 query-until-hit — **the unlock.** 033 found `get_companion()` rerolls
      on every call, and a call costs **1 tick**; every reroll so far has
      replanted at 200 ticks to get a fresh request. Call it repeatedly until it
      names a tile the map already satisfies, cap the attempts, and the pass
      becomes a 26-tick skip instead of a 1,455-tick walk. 034 shows the skip rate
      must reach ~66% (from 45%) before a second plot can pay.
- [x] 036 preference-stability — **`get_companion()` is deterministic for a
      standing plant** (7,958 bracketed pairs, zero changes). 013 is safe, 035 is
      explained, and 033's "non-deterministic per call" is withdrawn: the replant
      is what rerolls the preference, confirmed independently by Carrot sitting at
      4.1% against (1/3)³ = 3.7%. **A reroll costs a 200-tick plant, never a
      1-tick query.** `experiments/hay/036/result.md`

**Reopened 2026-08-16, high priority.** 039's independent estimate tonight
(leader ≈441 ticks/harvest) converges strikingly with this item's own old
"2.2 tiles per drone at 466 ticks" hypothesis — two separate lines of
reasoning landing near the same number. hay_single proved four separate
ways that multi-tile can't help a *solo* drone (no idle time to hide, no
sharing benefit past 1/3, any commute is pure loss) — but Hay's neighbour
cooperation (021, and 040's context) is a mechanism hay_single structurally
doesn't have, and it might change the calculus for a drone tending 2+ tiles
here specifically. Run this probe for real before assuming the hay_single
conclusion transfers. (Note: the "038" below is stale numbering from before
tonight's exp-038/039/040 — use whatever `new_experiment.sh` assigns next.)

- [ ] 037 growth-schedulability — **the gate on every multi-plot design, and it
      answers the standing question about the theoretical ceiling directly.**
      Multi-plot died in 027/029 because a drone walks to a plot and finds it
      unripe (30% of visits, 030). That is only unavoidable if ripening time is
      unpredictable. Now that the companion request is known to be fixed at plant
      time, the remaining unknown is growth.
      Probe, all 0-tick prints, on the champion unmodified: record
      `get_tick_count()` at replant, again when `polyculture_mapped` returns, and
      again the moment `can_harvest()` first turns true, plus `get_water()`.
      That yields three things at once:
        * **the growth-time distribution** — if it is tight, a drone can compute
          when to come back and multi-plot stops paying the 200-tick blind check;
        * **idle vs walk split** — how much of each pass is spent waiting rather
          than working, which is the true headroom for a second plot;
        * **the ceiling** — harvests per tile per second at this water level, so
          the leader's implied ~2.2 tiles per drone can be checked against what a
          tile can physically produce, rather than inferred from a run time.
      Write the falsifier first: if idle time is near zero, the farm is
      tick-limited, multi-plot is dead for good, and the gap has to be elsewhere.

- [ ] 038 skip-then-two-plots — retry two plots, but only if 037 shows real idle
      time *and* a tight growth distribution. 034's arithmetic: a second tile pays
      only when work per harvest is under ~509 ticks, and the leader implies 2.2
      tiles per drone at 466 ticks. 029 failed because it added the plot before
      cutting the work; scheduling is the way to cut it.

Cleaned 2026-08-16 13:05: the merge-conflict resolution in 020 resurrected
entries that were already finished (017, 018, 019, 023, 013, 008). Those are in
Done. What follows is genuinely open.

- [x] 031 why-carrot-fails — **the largest measurable prize.** 019 measured Bush
      5/5 and Tree 7/7 satisfied against Carrot 1/8, and a satisfied companion is
      worth **160x**. A third of requests are Carrot, so a third of passes collect
      512 instead of 81,920 — satisfying them all would be ~2.8x, against a 2.9x
      gap to the leader.
      The cause is assumed to be `till()` refusing ground a plant stands on, but
      that has never been checked. A probe that prints `get_ground_type()`,
      `get_entity_type()` and `can_harvest()` at the moment a carrot planting
      fails settles whether the blocker is the ground, the occupancy, or both —
      and therefore whether it is fixable at all.
- [x] 032 reroll-for-map-hit — **replaces empty-companion-tiles, which 031
      voided.** The farm is already ~97% multiplied, so the gap is ticks per
      harvest: 967 against the ~330 the leader implies. The dominant term is the
      companion round trip on the 52% of passes that need one, and the skip path
      costs 462 ticks against 1,459.
      020 already rerolls on an empty tile for 200 ticks a throw. Reroll instead
      until the request names a tile the map says is *already correct*: at a 45%
      hit rate that is ~1.2 throws, ~240 ticks, to turn a 1,459-tick pass into a
      462-tick one. Cap it, and measure the resulting skip rate.
- [x] 033 probe-the-reroll — done, and its write-up was later corrected by 036.
      The reroll changes the preference 66.4% of the time; the claim that it does
      so *without replanting* was wrong and cost 035 a run.
- [ ] 022 reroll-limit — 020 caps rerolls at 2. 036 confirms the residue exactly:
      Carrot sits at **4.1%** of preferences, matching (1/3)³. Limit 3 would take
      it to 1.2%, so this can move at most ~3% of passes and each reroll costs a
      200-tick plant. Small by construction.
      **And its premise is now in doubt.** 020's reroll was justified by 019's
      "carrot fails 7 in 8", which 031 falsified — carrot plantings succeed
      **99.6%** of the time. 020's −12.4 s is real, so the reroll buys something,
      but not what its comment claims. Worth one probe of *why* (affordability
      skips? longer walks to carrot tiles?) before spending a run on the cap.
- [ ] 033 monocrop-checkerboard — the user's design: permanent Bush/Tree stock on
      alternating tiles so a companion stops being work at all. Deprioritised
      against 031 because a permanent stock makes carrot requests *harder* to
      satisfy, not easier, and carrot is where the gap is.

### Closed lines — do not reopen without new information

- **Layout/spacing.** Disjoint diamonds +15.9% (021, 024), dense packing +36.6%
  (022). Per-pass profiles are identical to within 1% (025 vs 026), so layout is
  not a lever.
- **Multi-plot.** Four plots +47 s (027), two plots +28 s (029). 030 found why:
  29% of visits reach an unripe plot and pay a 200-tick move for nothing.
  **Waiting in place beats walking to check** while growth is the constraint.
- **Trading companion yield for ticks.** Polyculture is worth 160x (019); no
  variant that gives up the multiplier can win (011 at 67x apparent, 016 +11.5 s).

## Done

- [x] 057 memory-matched-reroll-real-run — **adopted, new champion.**
      Full memory-matched reroll (any type, `REROLL_LIMIT=5`, water
      threshold 0.999), run for real over the full ~871-cycle/drone
      horizon (not a bounded probe): **02:42.421, Global Rank #111**
      (was 02:47.682, #130/131). Confirms 049's short-probe regression
      was a time-horizon artifact — memory has to mature and a 150-cycle
      sample can't see that. `experiments/hay/057/result.md`
- [x] 058 higher-reroll-limit — **rejected.** `REROLL_LIMIT=10`:
      02:55.859, worse than 057's 5. `experiments/hay/058/result.md`
- [x] 059 lower-reroll-limit — **rejected.** `REROLL_LIMIT=3`:
      02:44.211, worse than 057's 5 (smaller regression than 058) —
      brackets 5 as the true local optimum.
      `experiments/hay/059/result.md`
- [x] 060 hybrid-accept-every-attempt — **tied, not adopted.** Accept
      on (memory-hit OR distance==1) checked every attempt, plus
      wrapped setup movement: 02:42.439, a dead tie with 057
      (+0.018s). Modeled a real improvement (S≈737 vs ≈800-816) that
      didn't materialize — an unmodeled opportunity cost (accepting a
      paid walk early forfeits later free-hit chances).
      `experiments/hay/060/result.md`
- [x] 061 hybrid-accept-late-only — **rejected.** Accept on (memory-hit
      always OR (`rerolls>=REROLL_LIMIT-2` AND distance<=2)): 02:49.099,
      worse than 057 and worse than 060's tie — widening the accept
      distance to catch something before the budget runs out still
      gives up real free-hit chances for a sometimes-more-expensive
      guaranteed payment. Closes the accept-policy-tuning family for
      real: four variants (058-061) plus four earlier ones (051,
      053-055) all tied or lost to 057's simple design.
      `experiments/hay/061/result.md`
- [x] 056 clean-growth-floor — isolated, single-tile, water
      deliberately maintained at 0.999: **415 ticks** growth at
      water≈1 (952 unwatered) — smaller than the ~608-724 estimated
      from Plant-growth.md's raw seconds, meaningfully changing the
      floor math. `experiments/hay/056/result.md`
- [x] 055 tight-packing-plus-distance-reroll — **rejected.** Combining
      051's spacing-4 layout with 054's distance>=2 reroll trigger:
      2,605.73 ticks/harvest, worse than either alone, skip rate also
      fell. Closes the combined family. `experiments/hay/055/result.md`
- [x] 054 distance-reroll-wider-trigger — **rejected.** (Carrot OR
      distance>=2) trigger, `REROLL_LIMIT=5`: 2,087.08 ticks/harvest,
      worse than 053's narrower trigger. `experiments/hay/054/result.md`
- [x] 053 distance-aware-reroll — **rejected.** Reroll on (Carrot OR
      distance==3), `REROLL_LIMIT=2`: 1,482.65 ticks/harvest vs 1,390
      baseline — a small regression. `experiments/hay/053/result.md`
- [x] 052 unlock-sweep-full — **confirmed maxed, closes this line for
      real.** `Unlocks.Speed` (5, never checked before — could plausibly
      have affected the ticks-per-real-second conversion) and
      `Unlocks.Fertilizer` (4) both confirmed genuinely maxed via a
      live `unlock()` attempt (returned `False`, level unchanged), not
      just an empty `get_cost()`. Direct `TICKS_PER_SEC` measurement
      (trivial loop): 6,074.97 — matches every prior measurement
      exactly. `experiments/hay/052/result.md`
- [x] 051 tighter-packing — **rejected, real and in the wrong
      direction.** Spacing 4 (vs champion's 5), still self-collision-
      safe: skip rate *fell* (32% vs 36.7%), ticks/harvest rose to
      2,347.27 — overlap increases thrashing (neighbors overwriting
      each other's conflicting needs), not cooperation.
      `experiments/hay/051/result.md`
- [x] 050 shared-memory-check — **confirmed drones are fully isolated.**
      A top-level dict written by one spawned drone is invisible to
      another (and to the main drone) — no shared mutable state is
      possible between drones, only the physical game world connects
      them. Rules out any "shared companion memory" design.
      `experiments/hay/050/result.md`
- [x] 049 reroll-before-walk-retimed — **looked like a rejection in a
      150-cycle probe** (1,471.41 vs 1,390 baseline) but see 057: this
      was a time-horizon artifact, not a real rejection.
      `experiments/hay/049/result.md`
- [x] 048 megafarm-check — **confirmed maxed.** `Unlocks.Megafarm`
      level 5, `unlock()` attempt returns `False`, `max_drones()` stays
      32. No drone-count lever. `experiments/hay/048/result.md`
- [x] 047 walk-servicing-breakdown — **found and fixed a self-inflicted
      diagnostic bug** (r1 measured from the drone's un-moved starting
      position, not the champion's real (3,3) home, producing bogus
      huge unwrapped distances — a false alarm about `Common.move_to`
      not wrapping). r2, corrected: real servicing costs are all
      reasonable (225-641 ticks for the move legs, matching distance
      1-3 exactly), no blowup. `experiments/hay/047/result.md`
- [x] 046 full-diagnostic-reprobe — real per-cycle breakdown under 32-
      drone contention: real water 0.8-1.0 (the champion's "10x short"
      comment is wrong), walk-rate 63%/skip-rate 37% in this sample.
      `experiments/hay/046/result.md`

- [x] 030 instrument-two-plots — **found the missing ticks.** 29% of visits reach
      an unripe plot and pay a 200-tick move for nothing; with movement in the
      accounting it is 1,160 ticks a harvest against the champion's 967, matching
      the measured +16%. A two-plot cycle revisits every ~2,320 ticks against
      ~2,819 of growth. **Waiting in place beats walking to check** — multi-plot
      is closed. `experiments/hay/030/result.md`

- [x] 029 two-plots — **rejected**, 03:20.637 (+28.3 s). Multi-plot loses at two
      plots as well as four, and the tick model predicted a wash, so ~150 ticks a
      harvest are unexplained. Recorded as an open question rather than a third
      invented mechanism. `experiments/hay/029/result.md`
- [x] 028 renoise — **the floor is 0.069 s (4 clean runs)**, so the original
      0.15 s stands and the 2.41 s correction was withdrawn. The real finding:
      identical code scores 67 sd faster when run deep into the memory leak, so
      comparisons are only valid under matching game conditions.

- [x] 027 multi-plot — **rejected**, 03:37.380 (+47 s, 19 sd). Four plots cost
      more in movement than the idling they remove. Surfaced the real finding of
      the day: the noise floor is **2.41 s, not 0.15 s**, and 012/014/017 are
      noise. `experiments/hay/027/result.md`

- [x] 024 lattice-wrapaware — **rejected**, 03:19.655 against 021's 03:19.653.
      Two milliseconds apart, so the wrap fix changed nothing and that
      explanation is dead as well. The lattice penalty is structural and
      deterministic; 025 instruments it instead of guessing a third time.
      `experiments/hay/024/result.md`

- [x] 022 denser-spacing — **rejected, +63.1 s (+36.6%).** With 021 this brackets
      an optimum: disjoint (L1 8) +15.9%, champion (L1 5) best, dense (L1 4)
      +36.6%. Layout tuning is not where the remaining gap lives.
      `experiments/hay/022/result.md`

- [x] 021 diamond-lattice — **rejected, +27.4 s (+15.9%).** Disjoint territories
      work exactly as designed and make the farm 16% slower: **contention was
      cooperation.** Neighbours pre-plant each other's companion tiles, so 010's
      skip fires far more often when territories overlap. Casts doubt on 014 and
      re-explains 015. `experiments/hay/021/result.md`

- [x] 020 reroll-after-harvest — **adopted, new champion.** 02:52.271, −12.4 s
      (−6.7%), rank #177 -> #149. 006's idea with its placement fixed: reroll
      after the multiplied harvest, not before it. `experiments/hay/020/result.md`

- [x] 017 water-threshold — **adopted**, 03:04.715, −0.608 s. Gate the watering
      loop on `num_items(Items.Water) > 0` so it stops spinning on an unreachable
      level; water warnings 1042 -> 120. Smaller than predicted, and this run
      cannot say why. `experiments/hay/017/result.md`
- [x] 019 mechanics-probe — **the multiplier is 160x, not 67x**, and carrot is
      satisfied only 1 time in 8 while Bush and Tree never fail. A third of
      passes therefore yield 512 instead of 81,920; satisfying all of them would
      be 2.8x, against a 3x gap to the leader. Growth is 2819 ticks at water 0.
      Companion distances are 1–3 and never wrap. `experiments/hay/019/result.md`

- [x] 016 no-carrot — **rejected**, 03:16.787 (+11.5 s). Skipping a doomed
      planting should have been free and was not: **the companion walk is how
      grass growth time gets hidden.** Walk time ~= growth time, which is why
      008, 011 and 016 all failed. The remaining gap needs faster growth, not
      shorter walks — and growth is water-limited.
      `experiments/hay/016/result.md`

- [x] 015 self-correcting-map — **rejected**, 03:09.234 (+3.9 s). Marking
      contested tiles permanently untrusted degrades the map to "always walk".
      **Optimism pays**: the asymmetry argument was right about single events and
      wrong about their frequency. `move_to_wrapped` kept in Common regardless.
      `experiments/hay/015/result.md`

- [x] 014 thirty-two-drones — **adopted**, 03:05.323, −0.466 s, rank #177.
      Confirms `SPAWNED 32 of 32`: thirteen experiments ran with four positions
      silently empty. Small win, because position only affects contention — and
      contention cannot be fixed by geometry at this drone count.
      `experiments/hay/014/result.md`

- [x] 013 companion-map — **adopted, new champion.** 03:05.789, −18.5 s (−9.1%),
      rank #230 -> #178. Each drone remembers what it planted where and skips the
      ~800 tick round trip when the tile is unchanged. Also measured
      `max_drones() = 32` against a spawn grid of 36 — we have been at the drone
      cap all along. `experiments/hay/013/result.md`

- [x] 012 skip-unaffordable — **adopted**, 03:24.347 (mean of 2), −0.205 s.
      Do not walk to a companion we cannot plant. Confirmed with a second run
      because the first cleared the floor by only 1.5x. Carrot is still never
      *successfully* planted, so a third of requests earn no multiplier — the
      biggest remaining prize. `experiments/hay/012/result.md`

- [x] 011 no-polyculture — **rejected decisively.** Polyculture is worth **67x**,
      not the ~5x it needs to break even against its ~800 ticks of movement per
      pass. Aborted at 1.26e9 hay / 2:24:43 in-game (145k hay/s vs the champion's
      9.78M hay/s). Retires every "trade yield for ticks" idea, 008's shape
      included. Surfaced two harness faults: `stop` never worked, and a failed
      run was being reported as a score. `experiments/hay/011/result.md`

- [x] 008 plot-rotation — **rejected, ~59x slower** (3:38:11 vs 03:40.911). The
      premise was a misreading of 007: 94% of passes *beginning* unripe is a
      frequency, not a duration. Dropping polyculture "to isolate the variable"
      threw away the 5x multiplier that was most of the yield, and a 25-tile
      circuit cost more movement than the waiting it removed.
      `experiments/hay/008/result.md`

- [x] 007 farm-state-diagnostic — **the bottleneck is growth, not ticks.** 825
      samples: the tile always holds grass (so 004/006 stand), companion faces
      are uniform thirds (confirming 004's premise), and `can_harvest()` is
      False on 94.1% of passes. Drones idle-wait while 96% of the field is
      unused. Invalidates the *rationale* for 006/008/009 and opens 011.
      `experiments/hay/007/result.md`

- [x] 006 reroll-companion — **rejected**, 03:41.013 (+0.102 s, inside the
      floor, so: no effect). The mechanic works — unaffordable carrot requests
      fell 73% — but a harvest plus a plant per reroll costs exactly what the
      multiplier wins. Prices the mechanic, and cleared the 005 tripwire.
      `experiments/hay/006/result.md`

- [x] 005 use-shared-helper — **adopted**, 03:40.911, delta 0.000 s. Confirms
      `Common.plant_companion()` matches 004's local override exactly; hay's
      private polyculture() is gone. Also serves as 004's confirming run.
      Tripwire noted: an identical time to the millisecond twice would mean the
      score has stopped tracking the code. `experiments/hay/005/result.md`

- [x] 004 true-companion — **adopted, new champion.** 03:40.911, −74.4 s
      (−25.2%) vs baseline; rank #422 -> #278. `p_planting_table` mapped Tree to
      a callback that plants Grass, silently forfeiting the polyculture
      multiplier on ~1/3 of companion visits. `experiments/hay/004/result.md`

- [x] 003 guarded-polyculture — **rejected**, 04:56.552 (+1.23 s). Planting
      grass on an unaffordable companion tile is not the repair: `till()` will
      not convert ground a plant stands on, so it traded 760 rare failures for
      259 common ones. Taught two things that reshaped the queue — carrot
      becomes affordable mid-run, and the Tree mapping is a silent miss.
      `experiments/hay/003/result.md`

- [x] 002 baseline — **04:55.320** (mean of 3), noise floor ±0.15 s. The score
      the game reports is already averaged over 2 h of repeats, so Hay barely
      varies and one run per variant is enough to rank candidates.
      `experiments/hay/002/result.md`
- [x] 001 terminate — bounded every drone's loop on `num_items(Items.Hay)` and
      reaped the spawns with `wait_for`. **04:55.393**, global rank #422 — the
      category scores at all for the first time. `experiments/hay/001/result.md`
