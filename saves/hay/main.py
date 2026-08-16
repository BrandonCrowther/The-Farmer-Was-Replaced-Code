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

def driver(x, y, report):
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
	passes = 0
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
		# PROBE. 032 argued the reroll cannot work: harvest() fails on an unripe
		# plant, so the tile still holds the grass planted an instant earlier,
		# instructions() sees Grass and plants nothing, and get_companion()
		# returns the same preference forever. If so, 020's REROLL_LIMIT has
		# never done anything and its 12.4 s win came from the single replant.
		#
		# Print what actually happens: the preference before and after each
		# attempt, and the entity in between.
		rerolls = 0
		instructions()
		companion = get_companion()
		if report:
			if passes < 300:
				quick_print("ROLL0", passes, companion[0])
		while rerolls < REROLL_LIMIT and companion != None and companion[0] == Entities.Carrot:
			before_type = companion[0]
			harvest()
			mid_entity = get_entity_type()
			instructions()
			companion = get_companion()
			if report:
				if passes < 300:
					quick_print("ROLLN", passes, "attempt", rerolls,
						"before", before_type, "mid_entity", mid_entity,
						"after", companion[0],
						"changed", companion[0] != before_type)
			rerolls = rerolls + 1
		if report:
			if passes < 300:
				quick_print("ROLLEND", passes, "rerolls", rerolls, "final", companion[0])
			passes = passes + 1

clear()
# max_drones() is 32 (measured in 013) and this grid has 36 positions, so four
# spawns have always returned None. The loop runs column-major, so the four that
# failed were never random: (5,2) through (5,5), a contiguous unfarmed strip down
# one edge, silently absorbed by the `if d:` guard ever since 001.
#
# Position only matters for contention. A drone farms its own tile, so where it
# stands changes nothing about its own yield — but neighbouring drones overlap in
# the band their companion requests reach (spacing 5 against a range of 3), and
# every overlap is a chance to invalidate another drone's map entry.
#
# So spend the four missing drones deliberately: keep the spacing-5 grid and put
# four holes through the middle instead of losing a whole edge. Same 32 drones,
# spread more evenly, fewer neighbours each.
HOLES = [(1, 1), (1, 4), (4, 1), (4, 4)]
quick_print("FARM", "world", get_world_size(), "max_drones", max_drones())
drones = []
for i in range(6):
	for j in range(6):
		if i + j != 0:
			if (i, j) not in HOLES:
				d = spawn_drone(driver, 3 + i*5, 3 + j*5, False)
				# None would mean the cap was hit anyway, and there is no handle
				# to wait on. Requesting 32 against a cap of 32 it should not
				# happen — the count below is how we find out if it does.
				if d:
					drones.append(d)
quick_print("SPAWNED", len(drones) + 1, "of", max_drones())
driver(3, 3, True)
# The run is not over until the program is, and the program is not over while a
# spawned drone is still farming. Reap them before falling off the end.
for d in drones:
	wait_for(d)
