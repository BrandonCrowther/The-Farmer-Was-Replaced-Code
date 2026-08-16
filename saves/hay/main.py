import Common

# Leaderboards.Hay succeeds when num_items(Items.Hay) >= TARGET is true *at the
# moment the program ends*. The simulation never stops on its own, so every drone
# has to notice the target and return, and the main drone has to outlive them all.
TARGET = 2000000000

# How many times to replant looking for a companion we can actually satisfy.
# Each reroll costs a plant (200 ticks) and restarts the growth clock, so this is
# not free; 019 puts P(carrot) at about a third, so most passes reroll zero times
# and few reroll more than once.
REROLL_LIMIT = 2

entity = Entities.Grass
instructions = Common.get_planting_instructions(entity)

def driver(x, y):
	Common.move_to(x,y)
	instructions()
	# What this drone believes it has planted, keyed by position.
	#
	# 010 already skips the harvest-and-replant when the companion tile is
	# already correct — but it only learns that *after* walking there, and a move
	# costs 200 ticks. Remembering it turns a ~800 tick round trip into a couple
	# of ticks of dictionary lookup on the passes where the tile has not changed.
	#
	# Only this drone's own plantings go in, and the map is never trusted for
	# anything except skipping a trip. The asymmetry matters: believing a
	# companion is present when it is not costs the 67x multiplier on that
	# harvest, while a needless walk costs 800 ticks. Wrong-and-skip is far worse
	# than wrong-and-walk, so nothing speculative belongs in here.
	planted = {}
	while num_items(Items.Hay) < TARGET:
		# Water while there is water to use, not until an unreachable level.
		#
		# `while get_water() < 0.75` targets a level the farm cannot supply. The
		# ground loses 1% of its water per second, so holding 32 tiles at 0.75
		# drains roughly 0.24/s, against a supply of one 0.25 tank per 10 seconds
		# — about 0.025/s. Ten times short. The condition therefore stays true
		# essentially forever and the loop spins on failed use_item calls at a
		# tick each, which is the ~1000 warnings a run and roughly 200 ticks a
		# pass by 009's accounting.
		#
		# Watering is still worth doing — growth scales linearly from 1x at water
		# 0 to 5x at 1 — so pour in whatever tanks exist and move on. num_items
		# costs 1 tick and, unlike the water level, it is a condition that can
		# actually become false.
		while num_items(Items.Water) > 0 and get_water() < 0.75:
			use_item(Items.Water)
		Common.polyculture_mapped(planted)
		# Not Common.await_harvest(): that spins forever on a plant that will
		# never ripen, and once the target is hit nothing else is going to move.
		# Checking the target here too is what stops a straggler from hanging
		# the whole run.
		h = can_harvest()
		while not h and num_items(Items.Hay) < TARGET:
			h = can_harvest()
		harvest()

		# Reroll a Carrot companion — but only now, after the harvest.
		#
		# 019 measured what 011 only inferred: a satisfied companion yields 81920
		# hay against a bare 512, a **160x** multiplier. It also measured which
		# companions actually get satisfied — Bush 5/5, Tree 7/7, Carrot 1/8.
		# Carrot needs Soil and `till()` will not convert ground a plant stands
		# on, so it fails whenever the tile holds anything unharvestable. Carrot
		# is a third of requests, so roughly a third of passes take 512 instead of
		# 81920.
		#
		# Replanting rerolls the preference, and grass is free. 006 tried this and
		# lost — because it rerolled at the *top* of the pass, harvesting the
		# mature grass while its companion was still unsatisfied and collecting
		# 512 for it. It paid for the reroll by destroying the thing it was
		# buying.
		#
		# Here the harvest has already happened at full multiplier and the tile is
		# empty, so a reroll costs one plant (200 ticks) rather than a harvest plus
		# a plant, and throws away nothing. Capped, because each reroll also resets
		# the growth clock.
		rerolls = 0
		instructions()
		companion = get_companion()
		while rerolls < REROLL_LIMIT and companion != None and companion[0] == Entities.Carrot:
			harvest()
			instructions()
			companion = get_companion()
			rerolls = rerolls + 1

clear()
# Lattice placement, retried with the wrap bug fixed.
#
# 021 tried this and came back 15.9% slower, and the write-up blamed contention.
# 023 then measured the arrival outcomes directly: a neighbour had pre-stocked the
# requested tile on 44 arrivals out of 32,727 — 0.13%. There was no cooperation to
# lose, and the explanation was invented.
#
# The real cause was almost certainly a broken assumption. "Companion requests
# never cross the seam" was verified for the *champion* layout, whose drones sit
# at 3..28. This lattice puts drones on x=0 and y=0, whose companions land at 31 —
# across the wrap — and Common.move_to is not wrap-aware, so it walks 31 moves
# east instead of 1 west. At 200 ticks a move that is 6200 ticks instead of 200,
# on roughly 7 of 32 drones. 022 put ~11 of 32 on a zero edge and lost 36.6%,
# which is the same story at a larger dose.
#
# So: same lattice, but polyculture now moves with move_to_wrapped.
ROWS = 8
COLS = 4
quick_print("FARM", "world", get_world_size(), "max_drones", max_drones())
drones = []
for j in range(ROWS):
	for i in range(COLS):
		x = 8 * i
		if j % 2 == 1:
			x = x + 4
		y = 4 * j
		if x + y != 0:
			d = spawn_drone(driver, x, y)
			if d:
				drones.append(d)
quick_print("SPAWNED", len(drones) + 1, "of", max_drones())
driver(0, 0)
# The run is not over until the program is, and the program is not over while a
# spawned drone is still farming. Reap them before falling off the end.
for d in drones:
	wait_for(d)
