import Common

# Leaderboards.Hay succeeds when num_items(Items.Hay) >= TARGET is true *at the
# moment the program ends*. The simulation never stops on its own, so every drone
# has to notice the target and return, and the main drone has to outlive them all.
TARGET = 2000000000

entity = Entities.Grass
instructions = Common.get_planting_instructions(entity)

def affordable(e):
	cost = get_cost(e)
	for item in cost:
		if num_items(item) < cost[item]:
			return False
	return True

def polyculture():
	# Common.polyculture() walks to the companion tile, harvests it and plants
	# the companion back. On this leaderboard the companion is usually Carrot
	# and the run starts with no carrot seeds, so the planting callback tills
	# the tile to Soil and *then* fails to plant — leaving bare soil that grows
	# nothing, on a tile that was productive grassland a moment earlier.
	#
	# So keep the walk and the harvest, which are real yield, and only change
	# what gets planted: the companion when we can afford it, grass when we
	# cannot. The tile is never left empty either way.
	x, y = get_pos_x(), get_pos_y()
	companion = get_companion()
	if companion == None:
		return
	plant_type, (px, py) = companion
	Common.move_to(px, py)
	harvest()
	if affordable(plant_type):
		Common.get_planting_instructions(plant_type)()
	else:
		instructions()
	Common.move_to(x, y)

def driver(x, y):
	Common.move_to(x,y)
	instructions()
	while num_items(Items.Hay) < TARGET:
		while get_water() < 0.75:
			use_item(Items.Water)
		polyculture()
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
