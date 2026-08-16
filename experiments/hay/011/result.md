# exp-011 — no-polyculture — result

**Outcome.** rejected, decisively — polyculture is worth ~67x, not 5x

**Numbers.** Aborted after 25 minutes of wall clock rather than run to
completion; the answer was already unambiguous and the night is finite.

| | hay | in-game time | rate |
| --- | --- | --- | --- |
| no polyculture (partial) | 1.26e9 of 2e9 | 2:24:43 | 145k hay/s |
| champion (010) | 2e9 | 03:24.552 | 9.78M hay/s |

**Ratio: 67.4x.** Extrapolated, the full run would have taken ~3.8 hours in-game
against the champion's 3.4 minutes.

**Verdict.** The trade is not close. Polyculture costs ~800 ticks of movement per
pass and returns roughly 67x the yield, so the ~5x break-even is met about
thirteen times over. The multiplier is clearly upgraded well past its base of 5x
— it doubles per upgrade and a resource leaderboard starts fully unlocked, so
5 x 2^4 = 80 is the right order.

**This retires a whole line of attack.** Anything that trades companion yield for
fewer ticks is dead on arrival, and that includes the shape of 008. It also
reframes 010's win correctly: 010 was worth having *because* it removed work
while keeping every bit of the multiplier, which is the only kind of saving this
category rewards.

**What it cost, and what it bought.** Two harness faults surfaced here:

1. **`stop` never worked.** It called `need_game` rather than `focus_game`, so
   Shift+F5 went to an unfocused window and was dropped. Even once focused,
   Shift+F5 does not stop a leaderboard run — the control that does is the red
   stop button in the code window's title bar, which the running window grows.
2. **A failed run was reported as a success.** The completion modal is identical
   for a scored and a failed run apart from an orange "Run Failed" line, and
   `cycle.sh` treated the modal's presence as a result. This run returned
   `STATUS=ok` with a duration of 2:36:54 for a run that never met its target.
   Left alone it would have journalled that as a score — the single most
   dangerous failure mode an unattended loop has, because the number looks
   entirely reasonable.

Both are fixed: `tfwr.sh verdict` probes the failure line, and `cycle.sh` exits
2 unless the verdict is `scored`.
