# exp-064 — does RNG-seed luck alone explain #1's implied budget?

**Hypothesis.** 063 confirmed `leaderboard_run()` hardcodes `seed = -1`
and sketched (without attempting) a seed-timing exploit — but never
checked whether such an exploit could work *even in principle*. If growth
time at water≈1 is effectively fixed regardless of seed (as 056's three
identical 415-tick trials suggested), then no amount of RNG luck can
produce a budget below our measured 815-tick floor (400 fixed +
415 growth), and the sketch is moot on top of being impractical.

**Variable.** `simulate()`'s documented seed parameter, swept 0-23, all
inside the sandbox — never touches the real farm or the live leaderboard.

**Metric.** `GROWTH_TICKS` (plant→ripe, isolated single tile, water
forced to 0.999) at each seed, read via `quick_print` from
`output.txt`. Compares the spread across seeds to 056's single-seed
value (415, steady state).

**Baseline.** 056: 415 ticks growth at water≈1 (real farm, single
uncontrolled seed, 3 consecutive identical trials after ramp-up).

**Procedure.**
1. `saves/hay/main.py`: driver, loops 24 explicit seeds through
   `simulate("GrowthProbe", Unlocks, {Items.Water: 1000}, {"trial_seed":
   seed}, seed, 2000)`.
2. `saves/hay/GrowthProbe.py`: the simulated target — plant one Grass
   tile at water≈1, measure ticks to `can_harvest()`, print.
3. No `zzRunner.py` in this deploy — nothing in this save can trigger a
   real `leaderboard_run()`.
4. `tools/tfwr.sh run`, read `output.txt` for the 24 `SIM_SEED
   ... GROWTH_TICKS ...` lines.

**Falsifier.** If growth ticks vary meaningfully across seeds (not just
noise around 415), RNG luck could move the real floor and the sketch in
`docs/RNG-Seed-Mechanism.md` deserves a second look, not dismissal on
the grounds already given.
