# exp-000 — end-to-end loop validation — result

**Outcome.** adopted — the full loop runs unattended-capable, with one caveat below.

## What ran

`Leaderboard_run` unchanged: `leaderboard_run(Leaderboards.Fastest_Reset, "Full_Reset_Driver", 5000)`.

## Result read off the screen

| field | value |
| --- | --- |
| leaderboard | Fastest_Reset |
| this run | **15:23:55.099** |
| personal best | 15:11:42.399 |
| global rank | #833 |
| wall-clock duration | ~2 min (F5 at 20:23:23, result dialog by ~20:25) |

This run was ~12 min of in-game time slower than the existing PB, so the PB stood.

## The loop, step by step

1. `tools/tfwr.sh select` — click the harness window. **Required**: F5 into an
   unselected window is a silent no-op.
2. F5 via `hyprctl dispatch sendshortcut`.
3. `tools/tfwr.sh state` → `running`, from the title-bar buttons flipping from
   green ▶/▷ to orange ■/⏸.
4. Poll; the result arrives as a modal with the time, PB, and global rank.
5. Dismiss with a click on OK, at logical (461, 938).
6. Farm state restored intact afterwards — resource bar back to 53B / 75B /
   11.1B, gold 75.6k → 75.7k. A leaderboard run does not disturb the main save.

## Caveat found: `state` is fooled by the result modal

`tfwr.sh state` still reported `running` while the completion dialog was up,
because the modal covers the title bar the check samples. It reads `idle`
correctly once dismissed. So `state` answers "did the run start", not "is the run
still going" — for completion, watch for the modal itself. Worth fixing before the
loop depends on it.

**Screenshots.** `logs/captures/` (gitignored) — result dialog captured at
20:25:34.
