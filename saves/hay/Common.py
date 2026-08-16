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

# p_planting_table answers "what do I put on a tile while farming X". A companion
# request asks a different question: "what actually satisfies a plant that wants
# an X next to it". The Tree entry is where the two diverge and why they must not
# share a lookup — a tree farm deliberately puts *grass* on the tile between its
# trees (see the wood driver, which depends on that), but a plant asking for a
# Tree companion is satisfied by nothing except a real tree.
#
# Answering the companion question from the farming table planted grass for every
# Tree request: legal, silent, no warning in output.txt, and no multiplier. It
# cost roughly a third of all companion visits. Fixing it took 25% off the Hay
# leaderboard time in one run — see experiments/hay/004/result.md.
#
# Companion preference is only ever Grass, Bush, Tree or Carrot, and never the
# plant's own species.
p_companion_table = {
	Entities.Grass: p_make_callback(Entities.Grass, Grounds.Grassland),
	Entities.Bush: p_make_callback(Entities.Bush, Grounds.Grassland),
	Entities.Tree: p_make_callback(Entities.Tree, Grounds.Grassland),
	Entities.Carrot: p_make_callback(Entities.Carrot, Grounds.Soil)
}

def plant_companion(entity):
	p_companion_table[entity]()

def polyculture():
	x, y = get_pos_x(), get_pos_y()
	companion = get_companion()
	# get_companion() returns None when the plant underfoot has no preference.
	if companion == None:
		return
	plant_type, (px, py) = companion
	move_to(px, py)
	harvest()
	plant_companion(plant_type)
	move_to(x, y)

