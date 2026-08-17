# Hay_Single — experiment queue

Target: **100_000_000 hay** on an 8x8 farm with a single drone
Leader: **02:17.995** (confirmed on the in-game leaderboard, rank #1)
Entry point: `main` · Runner: `leaderboard_run(Leaderboards.Hay_Single, "main", 5000)`

Branches: `auto_experiment/hay_single/NNN` · Results: `experiments/hay_single/NNN/result.md`

## The floor — answered by 001, not guessed

001 measured this category directly instead of reusing Hay's numbers (which
were taken under a different drone-count/world-size water economy). Full
arithmetic and caveats are in `experiments/hay_single/001/result.md`; the
conclusion:

- **Tick rate ≈6,070 ticks/s** (~15.2x the unpowered 400/s) → leader's
  02:17.995 buys **≈837,600 ticks**.
- **Harvests needed at full multiplier** (81,920/harvest, 512 base x 160,
  carried over from Hay and *not yet independently confirmed here* — 002 must
  check it): `ceil(100,000,000 / 81,920) = 1,221`.
- **Budget: ≈686 ticks/harvest, averaged over the whole run.**
- **Growth (≈404 ticks mean) is *not* the bottleneck.** Own-tile handling
  (harvest + replant, ~400-404 ticks) already exceeds growth time, so a single
  tile is never idle-blocked. **The schedulability floor is 1 hay tile.** A
  second tile cannot buy back idle time that doesn't exist — it can only add
  cross-board movement, which is exactly what lost Hay's 027 (+47s) and 029
  (+28s) multi-plot attempts. Do not reopen multi-tile without a *new* reason;
  the reason it failed in Hay applies here at least as strongly (no neighbour
  drones to pre-stock companion tiles for you, unlike Hay's 021 "contention is
  cooperation" finding).
- **The real constraint is the ~282-ticks-a-harvest companion-servicing
  budget.** A real companion walk (move + till + plant) costs 800-1,600 ticks
  — several times the slack. Hitting 686 average requires a **skip rate
  ≥~75%**, higher than Hay's own champion ever reached (45-66%, reactive
  reroll-until-hit). That rules out porting Hay's `polyculture_mapped` +
  reroll approach as-is and points at Hay's never-tried **038
  monocrop-stock** idea: pre-plant Grass/Bush/Tree once on the (few) positions
  within wrapped-distance 3, so nearly every pass is a dictionary lookup
  rather than a walk.

**So: one hay tile, ringed by a small pre-planted companion stock, is the
design — not a search over plot counts.** 002 builds and instruments exactly
that, and checks the ≥75% skip rate and the 81,920 yield assumption for real
before trusting the projection above.

## Queued

- [ ] 002 write-driver — build the single-tile + pre-stocked-companion design
      002's own falsifiers, before writing more than the first variant:
        * confirm a real satisfied harvest actually yields 81,920 here (001
          never walked to a companion tile to check);
        * instrument achieved skip rate and average ticks/harvest — if it
          lands well under the ~75%/~686 targets, that's the number to report,
          not a guess;
        * if the farm still can't clear 100,000,000 in reasonable time even
          at a high skip rate, say so and treat 038's idea as bounded rather
          than silently re-deriving a new floor after the fact.
- [ ] 003 (placeholder) — whatever 002 leaves open. Do not leave this queue
      empty without checking for a fundamental-fork question first (see
      docs/LOOP.md, "Empty queue").

## Done

- [x] 001 mechanics-probe — growth ticks (404 mean), tick rate (~6,070/s),
      wrapped companion distance (confirmed ≤3), op costs (confirmed 200),
      bare yield (confirmed 512). Computed the floor above.
      `experiments/hay_single/001/result.md`
