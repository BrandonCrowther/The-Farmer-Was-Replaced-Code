import Common

# Leaderboards.Hay succeeds when num_items(Items.Hay) >= TARGET is true *at the
# moment the program ends*. The simulation never stops on its own, so every drone
# has to notice the target and return, and the main drone has to outlive them all.
TARGET = 2000000000

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
		while get_water() < 0.75:
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

clear()
# Free measurement, two ticks, once: the spawn grid below is a hard-coded 6x6
# inherited from the achievement code. If the farm allows more drones than that,
# parallelism is being left unused and no amount of tick-shaving competes with it.
quick_print("FARM", "world", get_world_size(), "max_drones", max_drones())
drones = []
for i in range(6):
	for j in range(6):
		if i + j != 0:
			d = spawn_drone(driver, 3 + i*5, 3 + j*5)
			# None means the drone cap was hit; there is no handle to wait on.
			if d:
				drones.append(d)
driver(3, 3)
# The run is not over until the program is, and the program is not over while a
# spawned drone is still farming. Reap them before falling off the end.
for d in drones:
	wait_for(d)
