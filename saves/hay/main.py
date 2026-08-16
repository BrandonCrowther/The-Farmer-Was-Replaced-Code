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

# Each drone tends a 2x2 block of grass instead of standing over one tile.
#
# 026 measured where the time goes, split by what the pass did:
#
#   walk + replant a companion   52% of passes   1455 ticks work,   3 ticks wait
#   map says tile is already ok  45% of passes     26 ticks work, 437 ticks wait
#
# The map-skip passes do almost no work and then sit still for 437 ticks, because
# skipping the walk means the grass has not finished growing. That is ~21% of all
# drone time spent waiting. The walk was never overhead — it was covering growth —
# so removing it just converts walking into waiting.
#
# A second plot fixes that: while one tile ripens the drone harvests the other.
#
# 027 tried four plots and lost by 47 s. A lap of a 2x2 block is four moves — 800
# ticks — and only some plots are ripe on any lap, so the drone often paid a full
# circuit for a single harvest. Two adjacent plots make the lap one move: 200
# ticks against the 437 ticks of idling it replaces. That is the version of this
# idea whose arithmetic works.
#
# Deliberately *not* combined with anything else. 021 and 022 were unreadable
# because layout moved together with other things; this changes the plot count and
# nothing else, on the champion's spacing-5 grid.
PLOTS = [(0, 0), (1, 0)]

def driver(hx, hy, report):
	planted = {}
	passes = 0
	# Establish all four plots first.
	for offset in PLOTS:
		Common.move_to(hx + offset[0], hy + offset[1])
		instructions()

	while num_items(Items.Hay) < TARGET:
		for offset in PLOTS:
			if num_items(Items.Hay) >= TARGET:
				return
			Common.move_to(hx + offset[0], hy + offset[1])
			# No waiting. An unripe plot is skipped and picked up next circuit —
			# by which time three other plots have been visited.
			t0 = get_tick_count()
			ripe = can_harvest()
			if not ripe:
				if report:
					if passes < 400:
						quick_print("PASS", passes, "work", get_tick_count() - t0, "wait", 0, "ripe", 0)
					passes = passes + 1
			if ripe:
				while num_items(Items.Water) > 0 and get_water() < 0.75:
					use_item(Items.Water)
				Common.polyculture_mapped(planted, report)
				t1 = get_tick_count()
				harvest()
				if report:
					if passes < 400:
						quick_print("PASS", passes, "work", t1 - t0, "wait", 0, "ripe", 1)
					passes = passes + 1
				# Reroll a Carrot request now, on the empty tile, exactly as 020
				# established: after the multiplied harvest, never before it.
				rerolls = 0
				instructions()
				companion = get_companion()
				while rerolls < REROLL_LIMIT and companion != None and companion[0] == Entities.Carrot:
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
