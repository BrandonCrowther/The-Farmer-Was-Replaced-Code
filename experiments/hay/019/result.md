# exp-019 — mechanics-probe — result

**Outcome.** diagnostic — two standing numbers were wrong

**1. The polyculture multiplier is 160x, not 67x.**

| | hay per harvest |
| --- | --- |
| companion not satisfied | **512** |
| companion satisfied | **81,920** |

81920 / 512 = **160**. The 67x in 011 was a whole-run rate ratio and was off by
2.4x. It was recorded as though measured; it was not.

**2. Carrot almost never gets satisfied, and that is where the remaining gap is.**

| companion | requests | satisfied yield |
| --- | --- | --- |
| Bush | 14 | 81,920 (5/5 attempted) |
| Tree | 11 | 81,920 (7/7 attempted) |
| **Carrot** | **15** | **512 on 7 of 8 attempts** |

Bush and Tree always succeed. Carrot fails 7 times in 8 — it needs Soil and
`till()` will not convert ground a plant stands on. Carrot is a third of
requests, so roughly a third of passes collect 512 instead of 81,920.

Over the 40 sampled passes the farm produced 1,160,192 hay. Had every pass been
satisfied it would have produced 40 x 81,920 = 3,276,800. **That is 2.8x, and the
leader is 3x ahead.** The gap is almost entirely unsatisfied carrots.

**3. Growth is 2819 ticks at water 0**, and 691–1958 on passes where the
companion walk had already absorbed part of it. 016's "walk time ~= growth time"
was the right shape; this is the number. It also reconciles with 009's 3-tick
wait: that farm waters its tiles, and growth scales 1x to 5x with water, so a
watered plant ripens inside the walk.

**4. Companion distances are exactly 1, 2 or 3** (7, 14 and 19 of 40) and never
wrap. The "within 3 moves" claim and the diamond-territory premise both hold.

**Harness note.** `tfwr.sh run` verifies the run started by checking state 2
seconds after F5. This probe finished in under that, so `run` saw `result` and
reported "F5 did not start a run" — twice. The run had in fact completed both
times. Short runs need the check to distinguish "never started" from "already
finished"; the telemetry was recovered by hand from the game's `output.txt`.
