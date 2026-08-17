import Common

# Leaderboards.Hay succeeds when num_items(Items.Hay) >= TARGET is true *at the
# moment the program ends*. The simulation never stops on its own, so every drone
# has to notice the target and return, and the main drone has to outlive them all.
TARGET = 2000000000

# How many times to replant looking for a companion this drone already has
# stocked (see the reroll block in driver() below — exp-hay-038). Each reroll
# costs a plant (200 ticks) and restarts the growth clock, so this is not
# free; hay_single's 011 measured the exact tradeoff for the equivalent
# single-drone mechanism and found diminishing returns past ~5.
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

		# Reroll for a companion we already have standing — generalised from
		# 020's Carrot-only reroll (exp-hay_single-009/010/011/012 measured
		# this directly on the single-drone category, then proved it exactly:
		# the reroll-only asymptote against remembered stock is a hard
		# ceiling, not an estimate, at ~1,200 ticks/harvest for that category
		# — see experiments/hay_single/011/result.md).
		#
		# 020's version only avoided Carrot, on the theory that Carrot mostly
		# fails (019's "1/8" figure). 031 later measured Carrot actually
		# *succeeds* 99.6% of the time when attempted here — this drone has
		# 31 neighbours constantly planting Bush/Tree/Carrot, so wood is
		# abundant and `affordable()` rarely blocks it. So avoiding Carrot
		# specifically no longer targets the real cost, which is the walk
		# itself: `polyculture_mapped` still pays a ~800-tick round trip on
		# every miss, of any type, that this drone hasn't already stocked.
		#
		# The fix: reroll toward *any* companion this drone already has in
		# `planted`, not away from one specific type. A hit skips the whole
		# next pass's walk (a few ticks of dictionary lookup instead of an
		# ~800-tick round trip); a reroll here costs one plant (200 ticks,
		# same as 020's), and resets the growth clock exactly as before.
		rerolls = 0
		instructions()
		companion = get_companion()
		while rerolls < REROLL_LIMIT and companion != None:
			ctype, pos = companion
			if pos in planted and planted[pos] == ctype:
				break
			harvest()
			instructions()
			companion = get_companion()
			rerolls = rerolls + 1

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
				d = spawn_drone(driver, 3 + i*5, 3 + j*5)
				# None would mean the cap was hit anyway, and there is no handle
				# to wait on. Requesting 32 against a cap of 32 it should not
				# happen — the count below is how we find out if it does.
				if d:
					drones.append(d)
quick_print("SPAWNED", len(drones) + 1, "of", max_drones())
driver(3, 3)
# The run is not over until the program is, and the program is not over while a
# spawned drone is still farming. Reap them before falling off the end.
for d in drones:
	wait_for(d)
