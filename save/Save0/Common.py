# No-op function, placeholder
def p_noop(x=-1, y=-1, dir=None):
	return
	
def await_harvest():
	h = can_harvest()
	while not h:
		h = can_harvest()

def move_to(x, y, protocol = p_noop):
	def p_can(dir):
		return num_unlocked(Unlocks.Mazes) == 0 or can_move(dir)
	
	while get_pos_x() < x and p_can(East):
		protocol(x, y, East)
		move(East)
	while get_pos_x() > x and p_can(West):
		protocol(x, y, West)
		move(West)
	while get_pos_y() < y and p_can(North):
		protocol(x, y, North)
		move(North)
	while get_pos_y() > y and p_can(South):
		protocol(x, y, South)
		move(South)

def p_make_callback(entity, ground_type):
	def callback():
		if get_ground_type() != ground_type:
			till()
		if get_entity_type() != entity:
			plant(entity)
	return callback	

p_planting_table = {
	Entities.Grass: p_make_callback(Entities.Grass, Grounds.Grassland), 
	Entities.Bush: p_make_callback(Entities.Bush, Grounds.Grassland),
	Entities.Carrot: p_make_callback(Entities.Carrot, Grounds.Soil),
	Entities.Tree: p_make_callback(Entities.Grass, Grounds.Grassland),
	Entities.Cactus: p_make_callback(Entities.Cactus, Grounds.Soil),
	Entities.Pumpkin: p_make_callback(Entities.Pumpkin, Grounds.Soil),
	Entities.Sunflower: p_make_callback(Entities.Sunflower, Grounds.Soil)
}
def get_planting_instructions(entity):
	return p_planting_table[entity]

def polyculture():
	x, y = get_pos_x(), get_pos_y()
	plant_type, (px, py) = get_companion()
	instructions = get_planting_instructions(plant_type)
	move_to(px, py)
	harvest()
	instructions()
	move_to(x, y)

