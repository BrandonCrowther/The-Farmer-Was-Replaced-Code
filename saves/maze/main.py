import Common
import Mazes

# Responsible 
def master(x, y, max_len):
	start_time = get_time()
	Common.move_to(x,y)
	
	while get_time() - start_time < 5:
		get_time()
	
	while True:
		if get_entity_type() != Entities.Hedge:
			Mazes.initialize_maze(max_len, x, y)
		result = Mazes.start_solving(True)
		if result:
			Mazes.harvest_treasure(max_len)

def slave(x, y, max_len):
	start_time = get_time()
	Common.move_to(x + 2, y + 2)
		
	while get_time() - start_time < 6:
		get_time()

	while True:
		result = Mazes.start_solving()
		if result:
			Mazes.harvest_treasure(max_len)

clear()
max_len = 8
for i in range(get_world_size() / max_len):
	for j in range(get_world_size() / max_len):
		if i + j != 0:
			start_coord_x = i * max_len + 4
			start_coord_y = j * max_len + 4
			spawn_drone(master, start_coord_x, start_coord_y, max_len)
			spawn_drone(slave, start_coord_x, start_coord_y, max_len)
	
spawn_drone(slave, 0, 0, max_len)
master(0,0, max_len)