# exp-075 — drop instructions() from the hot loop entirely

**Hypothesis.** 066/067 already proved Grass auto-regrows and
`harvest()` alone — no ripeness check needed — correctly destroys and
regrows it every time (200 ticks, 0 yield, still Grass after). 073's
champion still calls `instructions()` (a guarded `plant(Grass)`) once
after every real harvest *and* once per reroll attempt, on the belief
that a replant is needed — but the guard (`if entity_type != Grass:
plant()`) never fires, since entity_type is never anything but Grass.
At ~2.1 rerolls/cycle that's ~3.1 wasted calls/harvest, 7 ticks each —
~22 ticks/harvest of pure overhead that was simply never removed when
073 was built, even though the underlying fact (066/067) was already
known.

**Variable.** Remove every `instructions()` call from the hot loop
(both the post-harvest call and the ones inside the reroll chase).
Keep only the two initial calls that plant Grass on previously-empty
ground for the first time.

**Metric.** Single-drone smoke test: windowed ticks/harvest, same
methodology as 068-074. Then the real completion modal's time and
rank, compared to 073's 02:00.734/#65.

**Baseline.** 073/074: real champion measures 889.78 ticks/harvest.

**Procedure.**
1. Single-drone smoke test (900 cycles) confirming the saving before
   touching the real champion.
2. Validation pass (reduced target, no `zzRunner.py`, explicit crop-
   tile collision check across all 64 tiles) before the real attempt —
   this is a code change, not just a parameter, so the same rigor as
   073 applies even though the underlying safety (auto-regrow) was
   already validated in isolation.
3. Real scored run via `tools/cycle.sh`.

**Falsifier.** If the smoke test doesn't show a reduction close to the
predicted ~17-22 ticks/harvest, or if removing `instructions()` breaks
something the isolated 066/067 probes didn't cover (e.g. an interaction
with the reroll chase's `planted` dict lookups), don't adopt.
