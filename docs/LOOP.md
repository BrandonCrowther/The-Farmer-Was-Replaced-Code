# The Phase 3 loop — tick protocol

One tick = one experiment, start to finish. `tools/cycle.sh` does the mechanical
part; this document covers the judgement, which is why the loop is a model and
not a systemd timer. Read this at the start of every tick — it is the contract,
and it is cheaper to re-read than to carry in the prompt.

The category is whatever the invocation names. Everything below says `<cat>`.

## A tick

1. **Check the clock against the stop conditions** (below). Stop before starting
   work you cannot finish.
2. **Pick the work.** The first unchecked item in `experiments/<cat>/queue.md`.
   If the queue is empty, see *Empty queue* below — do not just stop.
3. **Set up.** `tools/new_experiment.sh <cat> <slug>` for a new worktree and
   branch, then write the variant into `<worktree>/saves/<cat>/` and fill in
   `experiments/<cat>/<NNN>/hypothesis.md`. State the metric and what would
   falsify it *before* running, not after.
4. **Run.** `tools/cycle.sh <cat> exp-<cat>-<NNN>-r1 --from <worktree>`.
   It verifies the deploy by hash, reloads, runs, waits, captures, archives
   `output.txt` and dismisses. It prints `STATUS=ok` or fails non-zero.
5. **Read the result.** The time, PB and rank exist *only* on screen. Crop the
   modal out of `SHOT=` and read it with vision — a full-frame read costs ~4x a
   crop and tells you nothing extra. Only pull the full frame when a number
   looks wrong or the cycle failed.
6. **Compare against the floor.** `noise_floor` in `experiments/<cat>/record.json`.
   A delta smaller than that is not a result, whatever it looks like. If a
   variant appears to win by less than ~2x the floor, re-run once before
   believing it.
7. **Journal.** Write `result.md` — the number, the warning histogram delta, and
   what it implies for the next variant. Update `record.json` and move the queue
   item to Done with its number. Commit on the experiment branch.
8. **Merge if it won, journal either way.**

   *Won* — beat the baseline by more than the floor: merge the branch into
   `autofarmer`, `python3 tools/render_leaderboards.py`, commit, push
   `autofarmer` and the branch.

   *Lost or inconclusive* — the code stays on its branch, but the **journal
   still has to reach `autofarmer`**, or the next tick reads a stale queue and
   redoes the experiment. Merging the branch would drag the rejected code along
   with it, so take only the journal paths:

   ```sh
   git checkout auto_experiment/<cat>/<NNN> -- experiments/<cat>/
   git diff --cached --stat -- saves/    # must be empty: journal only, no code
   git commit && git push origin autofarmer auto_experiment/<cat>/<NNN>
   ```

   A loss is data and gets written up exactly as carefully as a win — 003 is the
   example: it cost a run, changed the queue completely, and was worth it.
9. **Queue what you learned.** Every result should either add a queue item or
   explain why that line of attack is exhausted.
10. **Schedule the next tick** and report one line: experiment, number, verdict.

## Stop conditions

- **Wall clock.** Ask the user for the stop time at setup; never assume one.
  Stop cleanly — finish journalling the current experiment, do not abandon it
  mid-cycle.
- **Five consecutive failures — switch category, do not stop.** A failure is a
  cycle that produced no time. Reset the count on any successful cycle. At five
  in a row, move to **`fastest_reset`** and carry on there; it already scores
  (15:11:42.399, rank #833), so it starts from a working baseline rather than
  from nothing.

  Read its queue before trusting it: item 001 is "terminate", written when every
  category was assumed to be an endless farmer, but this one already completes
  and posts a time, so 001 is probably moot and 002 (baseline) is the real
  starting point. Note also that its noise floor is **~10.7 minutes**, so unlike
  Hay a single run proves nothing — budget three runs per variant.

  If five *more* consecutive failures follow on `fastest_reset`, the harness
  itself is wedged rather than the category — switching again will not help.
  Stop then, and report what the last screenshot showed.
- **Empty queue.** Do not stop on an empty queue without first asking whether a
  *fundamental fork* exists — a different strategy rather than another tweak.
  For a farming category that means things like: a different plot geometry or
  drone count, a different crop rotation, trading rather than growing, using
  fertiliser, restructuring who waits on whom. Queue the fork and keep going.
  Only stop when you have genuinely run out of ideas, and then say what you
  tried and what you would try next.

## Rules that do not bend

- **Never read or write `live/save.json` or `live/__builtins__.py`.** Telemetry
  comes from the screen and from `output.txt`.
- **`main` is never touched.**
- **No `Co-Authored-By:` trailers.**
- An experiment branch writes only `saves/<cat>/**` and `experiments/<cat>/**`.
  Tooling and docs changes belong on `autofarmer`.

## Extending `Common.py`

Adding a genuinely reusable function to `Common.py` needs no permission. All
nine copies are byte-identical and must stay that way — edit one, then copy it
to the rest and check with `md5sum saves/*/Common.py`.

The bar is *reusable*, not merely *shared*: something a second category would
plausibly call. Category-specific tuning stays in that category's `main.py`.

Do not repurpose an existing helper to answer a new question — that is exactly
how the polyculture bug happened. `p_planting_table` answered "what do I plant
while farming X" and was reused for "what satisfies a companion request for X".
Both answers were right for their own question and wrong for the other, and
because planting the wrong plant is a legal action it produced no warning
anywhere. When a new caller needs a different question answered, give it its own
function — see `p_companion_table` and `plant_companion()`.

## Failure modes seen, and what they look like

| symptom | cause | what to do |
| --- | --- | --- |
| `F5 did not start a run (state=idle)` | a dialog or an undismissed modal swallowed the click | `cycle.sh` already retries after `dismiss`; if it still fails, capture and look |
| a time that barely differs from the last one | you may have run the *previous* code | check `DEPLOYED=` and the harness window text in the screenshot |
| `wait-result` times out | a drone is stuck in a busy-wait that the target check does not bound | `tfwr.sh stop`, then fix the wait, not the timeout |
| resource bar shows real save values mid-run | the run never started | reload and retry |
| `the game has crashed — Proton dialog: "..."` | the game died and left a Wine dialog carrying the same window class | `tools/tfwr.sh relaunch`, then re-run the cycle. See *Recovering from a crash* |
| a modal with an orange "Run Failed" line | the run was stopped, never terminated, or ended short of its target | `cycle.sh` already exits 2 on this. **Never record the duration** — it looks exactly like a score |


## A conclusion needs a test that is not a full run

A leaderboard run yields **one number**. That number can establish *whether* a
change is faster. It can never establish *why*, and every wrong conclusion in this
project came from using it that way — fitting a plausible mechanism to a single
delta and writing it up as explanation.

The record from one session:

| claim, fitted to a run time | how it died |
| --- | --- |
| "contention is cooperation" (021) | 023 measured neighbour pre-stocking at **0.13%** |
| "wrapped walks explain the lattice" (023) | 024 changed the walk and moved the time by **2 ms** |
| "carrot fails 7 times in 8" (019) | 031 traced 1,114 plantings: **99.6% succeed** |
| "the reroll rerolls nothing" (032) | 033 measured **66.4%** of attempts changing the preference |
| "the noise floor is 2.41 s" (027) | 028 ran four clean runs: **sd 0.069 s** |
| "`get_companion()` rerolls per call" (033) | 036 bracketed **7,958** query pairs: **zero** changed |

Five of those were written into result files as fact and three were built on by
later experiments before being caught.

**A probe can be wrong in its prose while right in its numbers.** 033 measured
the reroll correctly and then explained it with an untested side-claim — that
`mid_entity == Grass` proved no replant had happened. 035 was built on that
side-claim and lost 12.5 s. When a probe's *headline* is an interpretation rather
than a count, mark it as one.

**Prefer a number that is over-determined.** What settled 036 was not the
cleaner probe but a distribution that could be computed two ways: Carrot appeared
at 4.1% of preferences where a fresh roll gives 33%, and (1/3)³ = 3.7% is exactly
what two successful replants leave. A quantity you can predict independently and
then check will expose a wrong story on its own; a single count will not.

**The rule.** Any claim about mechanism must come with a test that observes the
mechanism *directly*, and that test must not be a full run:

- `quick_print` and `get_tick_count()` cost **0 ticks**. A probe can classify
  every arrival, count every reroll, trace every planting, and time every growth
  cycle without perturbing anything.
- **A probe can be short.** 019 ran 20 seconds and settled four questions. A
  probe that never scores is still a good cycle.
- **Write the falsifier before the run.** If you cannot say what observation
  would prove the explanation wrong, it is not an explanation yet.
- **State inferences as inferences.** "X is worth 67x" reads as measured and gets
  built upon. "The run is 67x slower without X, which we attribute to the
  multiplier but have not measured" does not.

**But keep the system intact while probing.** Isolation is not free: a
single-drone probe is a *different farm*, because wood and water economics depend
on the other drones — that is exactly how 019 produced a false carrot result, and
how 008 lost 59x by dropping polyculture "to isolate the variable". Instrument the
real configuration; do not shrink it.

## Measure the mechanic before designing around it

`quick_print` costs **0 ticks** and `get_tick_count()` costs 0. There is no
budget reason to infer a game mechanic from a run time when it can simply be
read. Several experiments here were designed around numbers that were never
measured:

| claim | where it came from | status |
| --- | --- | --- |
| polyculture is worth 67x | a whole-run rate ratio in 011, which conflates the multiplier with everything else that changed | inferred |
| walk time ~= growth time | a story fitted to 016's regression | inferred |
| companion range is 3 moves | the wiki | unverified in-game |
| the farm is ~10x water-starved | arithmetic on wiki constants | never sampled |
| contention is unavoidable | Euclidean area reasoning in a Manhattan world | **wrong**, corrected in 014 |
| movement has no diagonals | assumed, then used to justify a layout | **verifiable for free** — the API defines exactly four `Direction` constants |

Three rejections rest on the first two rows. The rule that follows:

1. **Before designing around a mechanic, measure it**, with a single-purpose
   probe run if needed. A probe that does not score is still a good cycle.
2. **Isolate the measurement.** `num_items` is global, so a per-drone yield
   measurement needs a single-drone run — with 32 drones the delta across your
   own harvest is contaminated by everyone else's.
3. **Check the API and the wiki first.** They are free. The no-diagonals question
   was answerable by grepping the API surface at any point.
4. **Write inferences as inferences.** A result that says "X is worth 67x" reads
   as measured and later experiments will build on it. Say what was measured and
   what was concluded from it, separately.

## The game leaks memory — relaunch on a schedule

Measured on 2026-08-16: after ~14 hours of continuous cycling the Steam scope hit
a **56 GB memory peak** and systemd OOM-killed it, taking the game with it. The
`Fatal error in GC` crash earlier the same day was almost certainly the same
pressure surfacing inside Mono first, rather than the run-abort it was blamed on.

The leak is not recoverable from inside the game. Only a relaunch reclaims it.

- `cycle.sh` prints `MEM_AVAIL_MB=` every run and refuses to start below 4 GB
  available, because a cycle begun under pressure will not finish and will take
  the game down with it.
- **Relaunch proactively every ~8 cycles**, not only after a crash. A relaunch
  costs about a minute; an OOM costs the cycle, the game, and possibly Steam.
- **Crashes are not a stop condition.** They are a known, understood, recoverable
  consequence of the leak. Recover and carry on, however many times it happens —
  there is no crash budget. What *is* a stop condition is recovery itself
  failing: see below.
- If Steam itself is gone — `tfwr.sh relaunch` reports "Steam is not running" —
  it was probably OOM-killed too. Start it with `setsid steam &`, wait for the
  process, then relaunch.


## The score depends on run conditions, not only on code

Four clean champion runs measure sd **0.069 s** — the game is extremely
repeatable when conditions match. But identical code run ~20 cycles into the
memory leak scored 67 and 15 standard deviations *faster* (exp-023 at 02:47.682,
exp-026 at 02:51.263, against a clean mean of 02:52.323). Instrumentation cannot
explain it: 026 carries more of it than 023 and is slower.

Whatever the cause, the consequence for method is firm:

- **Only compare runs made under similar game conditions** — similar time since
  the last relaunch, similar cycle count. A variant measured on a fresh game
  against a champion measured on a leaked one is not a comparison.
- **Re-baseline after every relaunch** if the comparison matters. A relaunch is
  cheap; a false result costs a whole line of experiments, as 021 and 022 did.
- **A floor is only valid for the conditions it was measured in.** The 0.15 s
  floor from 002 happened to survive, but it was applied for 25 experiments
  without anyone checking whether it still held.

## Recovering from a crash

`tools/tfwr.sh relaunch` kills the game, restarts it through Steam, waits for the
window, and reloads to the canonical state. It is the hand-walked recovery from
2026-08-16 written down, and it leaves the game exactly where a `reload` does.

A crash is **not** an ordinary cycle failure. Handle it like this:

1. Any `tfwr.sh` command failing with *"the game has crashed"* means relaunch,
   then re-run the cycle that died. That cycle counts as one failure.
2. **Verify the deployed code afterwards.** A restart is when Steam Cloud has
   restored the original save over a deployed category before. `cycle.sh` hashes
   `live/*.py` against the category every run and will redeploy, so this is
   covered — but do not skip a cycle's hash check to save time.
3. **No cap on relaunches.** The original rule stopped after three, written when
   crashes looked random and possibly unfixable. They are not: they are the
   memory leak above, and a relaunch reclaims it completely. Recovering ten times
   in a session is maintenance, not failure.

   **Stop when recovery stops working**, which is a different signal: two
   consecutive relaunch attempts that do not end with the game idle and
   responding. That means something the loop genuinely cannot fix — a broken
   install, a Steam that will not start, a full disk — and further attempts only
   burn the window. Hand off with the last screenshot and the exact error.

## Speedup is not a lever

`leaderboard_run(..., speedup)` sets a *starting* speedup and the docs are clear
that it "does not affect the result of the simulation in any way" and that the
sim "may not reach the stated value if it cannot properly speedup computation …
common causes include use of multiple drones".

Measured here: a score accumulates 2 hours (7200 s) of sim time, and cycles take
210 s of wall clock, so the effective speedup is **~34x** against the 5000
requested — with the no-polyculture variant down at ~6x. Raising the number is
free and harmless and will do nothing. The only real lever on wall-clock cycle
time is cheaper per-tick code, which is what the experiments are chasing anyway.

## Aborting a run is dangerous

`Shift+F5` does not stop a leaderboard run, focused or not. The control that
works is the red stop button that appears in a code window's title bar while it
executes — and using it killed the game outright on 2026-08-16 with
`Fatal error in GC` / `SuspendThread loop failed`, a Mono GC fault under Proton,
which ended the night's loop.

So treat aborting as a last resort with a real chance of taking the game with it.
If a variant is running long, prefer letting it finish, or read the answer off
the resource bar and the in-game clock while it runs — that is how 011 was priced
at 67x without needing its final number.
