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
