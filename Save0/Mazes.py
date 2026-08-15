import Common

opposite_directions = {
	North: South,
	South: North,
	East: West,
	West: East
}

coordinate_adjustments = {
	North: [0, 1],
	South: [0, -1],
	East: [1, 0],
	West: [-1, 0]
}

is_slave = False
dead_ends = []
treasure_location = None

def reset_memory():
	global dead_ends
	dead_ends = []
	global treasure_location
	treasure_location = measure()

def harvest_treasure(maze_size):
	substance = maze_size * 2**(num_unlocked(Unlocks.Mazes) - 1)
	success = use_item(Items.Weird_Substance, substance)

def initialize_maze(maze_size, x, y):
	harvest()
	Common.move_to(x,y)
	plant(Entities.Bush)
	harvest_treasure(maze_size)

def random_elem(list):
	index = random() * len(list) // 1
	return list[index]
	

def valid_moves(previous_move = None):
	ret = []
	moves = set((North, East, South, West))
	
	if get_entity_type() == Entities.Grass:
		return ret
	
	if previous_move != None:
		moves.remove(opposite_directions[previous_move])
	
	for m in set(moves):
		adj = coordinate_adjustments[m]
		px, py = get_pos_x(), get_pos_y() 
		x, y = px + adj[0], py + adj[1]
		
		if not can_move(m) or is_dead_end(x, y):
			moves.remove(m)
		else:
			meas = measure()
			if meas == None:
				return []
			tx, ty = meas[0], meas[1]
			distx = abs(tx - px)
			disty = abs(ty - py)
			cdistx = abs(tx - x)
			cdisty = abs(ty - y)
			if cdistx + cdisty < distx + disty:
				ret.insert(0, m)
			else:
				ret.append(m)
		
	# slave works backwards
	if is_slave:
		rev = []
		for i in range(len(ret)):
			rev.insert(0, ret.pop())
		return rev

	return ret

def is_dead_end(x = get_pos_x(), y = get_pos_y()):
	for i in dead_ends:
		if i[0] == x and i[1] == y:
			return True
	return False


def backtrack(backstack):
	while(len(backstack) > 0):
		if get_entity_type() == Entities.Treasure:
			global dead_ends
			dead_ends = []
			return True
		move(backstack.pop())
	return False
		
def recurse(direction, backstack):	
	move(direction)
	backstack.append(opposite_directions[direction])
	
	meas = measure()
	if meas != treasure_location:
		reset_memory()
		return False

	entity = get_entity_type()
	if entity != Entities.Hedge and entity != Entities.Treasure:
		return False
	
	if entity == Entities.Treasure:
		return True
	
	moves = valid_moves(direction)
	move_len = len(moves)
	if move_len > 1:
		global dead_ends
		dead_ends.append([get_pos_x(), get_pos_y()])
	for m in moves:
		if m == opposite_directions[direction]:
			continue
		ret = recurse(m, [])
		if ret == True:
			return True
	
	bt = backtrack(backstack)
	backstack = []
	return bt
		

def start_solving(set_slave = False):
	global is_slave
	is_slave = set_slave
	reset_memory()
	moves = valid_moves()
	for m in moves:
		ret = recurse(m, [])	
		if ret:
			return True
	return False