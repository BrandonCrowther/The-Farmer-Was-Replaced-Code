import Common

# Leaderboards.Hay succeeds when num_items(Items.Hay) >= TARGET is true *at the
# moment the program ends*. The simulation never stops on its own, so every drone
# has to notice the target and return, and the main drone has to outlive them all.
TARGET = 2000000000

entity = Entities.Grass
instructions = Common.get_planting_instructions(entity)

# A plant's companion is always a *different* species, so grass rolls over Bush,
# Tree and Carrot. get_cost says Bush and Tree are free and only Carrot costs
# anything (512 hay + 512 wood) — yet Common.p_planting_table maps Entities.Tree
# to a callback that plants **Grass**. A Tree request is therefore satisfied with
# the wrong plant: no warning, no error, and no polyculture multiplier on roughly
# a third of every drone's companion visits. Plant the tree it asked for.
p_tree = Common.p_make_callback(Entities.Tree, Grounds.Grassland)

def companion_instructions(t):
	if t == Entities.Tree:
		return p_tree
	return Common.get_planting_instructions(t)

def polyculture():
	# Otherwise identical to Common.polyculture(): walk to the companion tile,
	# harvest it, plant the companion, walk back. Only the Tree case differs.
	x, y = get_pos_x(), get_pos_y()
	companion = get_companion()
	if companion == None:
		return
	plant_type, (px, py) = companion
	Common.move_to(px, py)
	harvest()
	companion_instructions(plant_type)()
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
