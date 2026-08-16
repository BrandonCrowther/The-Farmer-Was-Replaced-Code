import Common

# Leaderboards.Hay succeeds when num_items(Items.Hay) >= TARGET is true *at the
# moment the program ends*. The simulation never stops on its own, so every drone
# has to notice the target and return, and the main drone has to outlive them all.
TARGET = 2000000000

entity = Entities.Grass
instructions = Common.get_planting_instructions(entity)

# Grass rolls its companion over Bush, Tree and Carrot. 004 made Bush and Tree
# pay out, leaving Carrot as the one face that costs anything (512 hay + 512
# wood) — so reroll that one. Two of the three faces are free, so a reroll clears
# in about 1.5 tries and only ~1/3 of iterations need one at all.
#
# The cap matters: every reroll is a harvest plus a plant, and an uncapped loop
# would keep paying that through a run of bad luck chasing a multiplier worth
# less than the ticks spent on it.
REROLL_LIMIT = 3

def driver(x, y):
	Common.move_to(x,y)
	instructions()
	while num_items(Items.Hay) < TARGET:
		while get_water() < 0.75:
			use_item(Items.Water)
		# Reroll before the walk, while this plant is still worthless to discard.
		Common.reroll_companion(entity, REROLL_LIMIT)
		Common.polyculture()
		# Not Common.await_harvest(): that spins forever on a plant that will
		# never ripen, and once the target is hit nothing else is going to move.
		# Checking the target here too is what stops a straggler from hanging
		# the whole run.
		h = can_harvest()
		while not h and num_items(Items.Hay) < TARGET:
			h = can_harvest()
		harvest()

clear()
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
