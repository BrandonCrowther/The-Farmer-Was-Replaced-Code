import Common

# Leaderboards.Hay succeeds when num_items(Items.Hay) >= TARGET is true *at the
# moment the program ends*. The simulation never stops on its own, so every drone
# has to notice the target and return, and the main drone has to outlive them all.
TARGET = 2000000000

entity = Entities.Grass
instructions = Common.get_planting_instructions(entity)

# exp-007 measured the thing this run is built around: a drone found its plant
# unripe on 94.1% of passes, and busy-waited for it. Meanwhile 36 drones were
# working 36 of the farm's 1024 tiles and the other ~96% sat empty.
#
# So stop waiting. Give every drone a square plot and walk it in a fixed circuit,
# harvesting whatever is ripe as it comes round. A tile now gets the entire
# circuit to grow instead of one drone standing over it — the growth that used to
# be dead time happens while the drone is somewhere else, and the whole field is
# planted rather than a scattering of it.
#
# Polyculture is deliberately left out here. It is worth a 5x multiplier and it
# will come back in 012, but it also doubles the walking, and this run exists to
# test one thing: that idle waiting, not tick count, is what costs the time.
PLOTS = 6

def driver(ox, oy, size):
	# Plant the plot out once, then circuit it forever.
	for dx in range(size):
		for dy in range(size):
			Common.move_to(ox + dx, oy + dy)
			instructions()

	while num_items(Items.Hay) < TARGET:
		for dx in range(size):
			for dy in range(size):
				if num_items(Items.Hay) >= TARGET:
					return
				Common.move_to(ox + dx, oy + dy)
				# No busy-wait: an unripe tile is simply skipped and picked up on
				# the next circuit. That is the whole point.
				if can_harvest():
					harvest()
					instructions()
				if get_water() < 0.75:
					use_item(Items.Water)

clear()
size = get_world_size() // PLOTS
drones = []
for i in range(PLOTS):
	for j in range(PLOTS):
		if i + j != 0:
			d = spawn_drone(driver, i * size, j * size, size)
			# None means the drone cap was hit; there is no handle to wait on.
			if d:
				drones.append(d)
driver(0, 0, size)
# The run is not over until the program is, and the program is not over while a
# spawned drone is still farming. Reap them before falling off the end.
for d in drones:
	wait_for(d)
