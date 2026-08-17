# exp-hay-045 -- unlock-level-check
#
# docs/wiki/Unlocks.md: "Grass -- Increases the yield of grass." This is a
# SEPARATE unlock from Polyculture, never checked tonight (or apparently
# ever, in this project's history -- grep found no prior mention). If
# leaderboard runs don't actually start with it maxed, despite the general
# "starts with all unlocks fully upgraded" claim, that would be a real,
# previously entirely unexamined yield lever -- independent of every
# companion-servicing question chased tonight.
#
# 0-tick reads only (num_unlocked, get_cost are getters). Terminates
# immediately after printing; expect "Run Failed", not a score.

quick_print("GRASS_LEVEL", num_unlocked(Unlocks.Grass))
quick_print("POLYCULTURE_LEVEL", num_unlocked(Unlocks.Polyculture))
quick_print("WATERING_LEVEL", num_unlocked(Unlocks.Watering))
quick_print("GRASS_NEXT_COST", get_cost(Unlocks.Grass))
quick_print("POLYCULTURE_NEXT_COST", get_cost(Unlocks.Polyculture))
