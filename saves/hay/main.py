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

# GROWTH CEILING PROBE. Establishes the theoretical floor on ticks per harvest.
#
# The chain: grass takes a fixed time to ripen; water scales growth 1x to 5x
# linearly; so the fastest any tile can produce is its unwatered growth time
# divided by five. With 32 tiles and 763 harvests each to reach 2e9, that sets a
# hard floor no amount of routing cleverness can beat.
#
# Two things are missing before that sum can be done, and both are free to
# measure:
#
#   1. The water/growth relationship, measured here rather than taken from the
#      wiki. Alternate passes: water to the maximum available, or not at all.
#   2. The tick/second conversion. The wiki prices water per *second* (a 0.25
#      tank each 10 s, 1% of current lost per second) while everything we measure
#      is in ticks, and nobody has established the rate. get_time() and
#      get_tick_count() both cost 0.
#
# Runs on the full 32-drone farm deliberately. 031's lesson: a single-drone probe
# is a different farm, because wood and water economics depend on the others.
SAMPLES = 300

def driver(x, y, report):
	Common.move_to(x,y)
	instructions()
	planted = {}
	passes = 0
	while num_items(Items.Hay) < TARGET:
		wet = passes % 2 == 0
		if wet:
			while num_items(Items.Water) > 0 and get_water() < 0.99:
				use_item(Items.Water)

		# Growth starts now: the tile was replanted at the end of the last pass.
		t_plant = get_tick_count()
		w_plant = get_water()

		Common.polyculture_mapped(planted)
		h = can_harvest()
		while not h and num_items(Items.Hay) < TARGET:
			h = can_harvest()
		t_ripe = get_tick_count()
		harvest()

		if report:
			if passes < SAMPLES:
				quick_print("GROW", passes, "wet", wet,
					"growticks", t_ripe - t_plant,
					"w_start", w_plant, "w_end", get_water(),
					"tanks", num_items(Items.Water),
					"tick", get_tick_count(), "time", get_time())
		passes = passes + 1
		instructions()

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
