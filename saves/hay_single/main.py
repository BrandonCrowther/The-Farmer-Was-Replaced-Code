import Common

# exp-hay_single-013 -- reroll-sequence-pattern
#
# 011 proved the reroll-only asymptote (REROLL_LIMIT -> infinity, full
# coverage) is exactly 1,200 ticks/harvest (~68.27 hay/tick) -- and 012
# already measures ~68.7 real, meaning REROLL_LIMIT tuning is at its
# ceiling. That ceiling assumes each (type, position) draw is IID uniform.
# If it isn't -- if replanting draws from a *predictable* sequence rather
# than a fresh independent roll -- the 1/3 structural cap doesn't actually
# hold and there is real headroom left. This is cheap to check directly
# rather than assumed: log a long raw sequence of companion draws with no
# servicing at all (pure plant -> read -> destroy -> repeat) and look for
# structure (repeats, alternation, position clustering) that the reactive
# design isn't exploiting.
#
# Not a driver: this never satisfies anything and never reaches the target.
# Expect "Run Failed"; the duration is not a score.

instructions = Common.get_planting_instructions(Entities.Grass)
instructions()

SAMPLES = 300
for i in range(SAMPLES):
	companion = get_companion()
	if companion != None:
		ctype, (cx, cy) = companion
		quick_print("DRAW", i, ctype, cx, cy)
	else:
		quick_print("DRAW", i, "None")
	harvest()
	instructions()

quick_print("DONE", "TICK_FINAL", get_tick_count(), "TIME_FINAL", get_time())
