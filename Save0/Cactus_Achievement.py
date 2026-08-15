import Common
import Cactus

entity = Entities.Cactus
def driver(x, y, dir):
	Common.move_to(x,y)
	# Delegate spawning additional drones recursively
	if num_drones() < max_drones():
		if dir == North or dir == South:
			spawn_drone(driver, x + 1, 0, dir)
		else:
			spawn_drone(driver, 0, y + 1, dir)
	instructions = Common.get_planting_instructions(entity)
	sizes = Cactus.prep_field(entity, dir, instructions)
	sorted = Cactus.sort_asc(sizes)
	Cactus.perform_sort(sorted, dir)
		

clear()
# Drone 0 acts as the control plane
# It delegates jobs to short lived slave drones
while True:
	driver(0, 0, East)
	
	count = num_drones()
	while count > 1:
		count = num_drones()
	driver(0, 0, North)
	
	count = num_drones()
	while count > 1:
		count = num_drones()

	harvest()
	Common.move_to(0,0)