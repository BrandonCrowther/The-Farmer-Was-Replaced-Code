# How leaderboard RNG is seeded — and why manipulating it isn't worth pursuing

Written 2026-08-17 during the Hay (multi) investigation, exp-063. Applies
to every leaderboard category, not just Hay — the seeding code is shared.

## What the game actually does (confirmed by decompiling `Core.dll`)

`Core.dll` is Mono-managed IL (not IL2CPP), so its metadata and method
bodies are readable directly — no debugger or running process needed,
just static inspection of the installed `.dll` file. Two facts were
confirmed this way:

1. **`Simulation`'s constructor** takes a `seed` argument. If `seed < 0`
   it constructs `random = new System.Random()` (parameterless); if
   `seed >= 0` it constructs `random = new System.Random((int)seed)`.
   Every other named generator on the object — `randomVarious`,
   `randomMaze`, `randomSnake`, `randomCactus`, `randomSunflower`,
   `randomPumpkin`, `randomPoly`, `randomRandom` — is then constructed as
   `new System.Random(random.Next())`, drawn from that one master
   `random` in a fixed order at construction time. So the entire run's
   randomness — plant growth timing, maze layout, water decay, companion
   draws, everything the wiki's `Simulation.md` page lists — is a
   deterministic function of exactly one root value.

2. **`BuiltinFunctions.LeaderboardRun`** builds a `LeaderboardStartArgs`
   object and hardcodes the seed argument to the literal constant `-1`
   — visible directly in the compiled IL as `ldc.i4.m1` immediately
   before the `newobj LeaderboardStartArgs..ctor` call, in the same
   argument position `Simulation`'s constructor treats as seed. This
   matches `Leaderboard.md`'s documented "Equivalent Simulation"
   snippets (`seed = -1` for every category), now confirmed from the
   actual call site rather than just the wiki text.

**Consequence:** every `leaderboard_run()` always takes the parameterless
`new System.Random()` branch. Under Mono/.NET Framework semantics, that
constructor seeds from `Environment.TickCount` — a monotonic millisecond
counter (roughly, time since process/system start) — **not** a
wall-clock `DateTime`. The specific lever the user proposed (manipulating
the date/time) doesn't apply here; the theoretical lever would be
*system uptime in milliseconds at the instant the constructor runs*, a
different and much less convenient thing to control than the calendar
clock.

## Sketch: how a determined user could attempt to exploit this

This was **not attempted** — no seed search was run, no timing attack was
built, nothing was submitted to the live leaderboard. This section exists
only to record the reasoning for why it wasn't worth pursuing, in enough
detail that the question doesn't need reopening later.

1. **Offline seed search using the intended sandbox tool.** `simulate()`
   legitimately exposes an explicit seed parameter and is deterministic
   given fixed starting conditions + seed (`Simulation.md`). A user could
   brute-force many candidate seeds locally, using a cheap partial-run
   proxy (e.g. the first N companion draws) instead of a full run, to
   find a seed whose early RNG sequence is unusually favorable.

2. **Mapping seed → `TickCount`.** Mono's `System.Random()` derives its
   internal state from `Environment.TickCount` via a known, public,
   deterministic algorithm. In principle a target seed from step 1 could
   be inverted to the `TickCount` value(s) that would produce it — though
   the mapping may not be cleanly invertible depending on how bits get
   mixed/discarded; this step was not actually attempted.

3. **Timing the trigger.** To land the real `leaderboard_run()` call at
   that exact millisecond of system uptime would require sub-millisecond
   precision through our own keypress-injection harness, the X11/Wayland
   compositor, the Proton/Wine translation layer, and Mono's own
   scheduling — several independent sources of jitter, any one of which
   is plausibly worse than 1 ms. There's also no builtin to read back
   which seed a run actually used, so confirming a hit would itself need
   a separate mechanism. Realistically unreliable even before considering
   whether it should be attempted at all.

4. **The scoring rule caps the benefit regardless.** `Leaderboard.md`:
   *"To reduce variance, all runs are required to run for at least 2
   hours... If a run is completed earlier, it will be repeated until a
   total time of 2 hours is reached. The average of all runs is then
   uploaded as your score."* Each repeat almost certainly reseeds
   independently (a fresh `Simulation` per repeat, hitting the `-1`
   branch again, reading `TickCount` at whichever real-world instant that
   repeat happens to start — a moment fully internal to the running
   session, not observable or triggerable from outside). A perfect
   single-shot timing attack could at best control the *first* repeat's
   seed; for a run that resolves in low tens of seconds at 5000x speedup,
   a 2-hour session is plausibly 100+ repeats, capping the realistic
   benefit of the entire technique at roughly 1% or less of the final
   averaged score — even in the best case, before any of steps 2-3's
   reliability problems are counted.

## Verdict

Mechanism fully identified: one root `System.Random`, hardcoded `seed =
-1` at every `leaderboard_run()` call site, seeded from system uptime
rather than wall-clock time. The attack sketched above is both
impractical (multi-layer sub-millisecond timing, an unverified seed
inversion step, no way to confirm a hit) and low-value even if it worked
perfectly (the 2-hour repeat-averaging rule dilutes a single controlled
seed to a small fraction of the final score). Combined with the standing
concern that deliberately forcing a favorable outcome on a shared public
Steam leaderboard is a fairness problem regardless of technical
feasibility, this closes the "residual RNG predictability" candidate from
`experiments/hay/queue.md`'s 063 entry. Not pursued further.
