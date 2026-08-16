import Common

# Leaderboards.Hay succeeds when num_items(Items.Hay) >= TARGET is true *at the
# moment the program ends*. The simulation never stops on its own, so every drone
# has to notice the target and return, and the main drone has to outlive them all.
TARGET = 2000000000

entity = Entities.Grass
instructions = Common.get_planting_instructions(entity)

# Diagnostic run, not an optimisation. Several conclusions rest on an unverified
# assumption: that our own tile still holds a plant at the top of each iteration.
# The driver plants grass once before the loop and harvests at the end of every
# pass, and nothing obviously replants it. If it is empty then get_companion()
# returns None, polyculture() returns immediately, and both 004 and 006 exercised
# far less than they appear to.
#
# quick_print costs 0 ticks, so this does not perturb the thing being measured —
# but it is bounded to the first few passes of one drone anyway, because the
# sensor calls around it are not free.
SAMPLES = 25

def driver(x, y):
	Common.move_to(x,y)
	instructions()
	passes = 0
	while num_items(Items.Hay) < TARGET:
		while get_water() < 0.75:
			use_item(Items.Water)
		if x == 3 and y == 3 and passes < SAMPLES:
			companion = get_companion()
			if companion == None:
				quick_print("STATE", passes, get_entity_type(), get_ground_type(), can_harvest(), "companion=None")
			else:
				quick_print("STATE", passes, get_entity_type(), get_ground_type(), can_harvest(), companion[0])
		passes = passes + 1
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
