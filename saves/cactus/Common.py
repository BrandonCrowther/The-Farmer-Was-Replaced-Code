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

def affordable(entity):
	# Whether we hold everything planting `entity` costs. Grass, Bush and Tree
	# are free; Carrot is 512 hay + 512 wood.
	cost = get_cost(entity)
	for item in cost:
		if num_items(item) < cost[item]:
			return False
	return True

def polyculture_mapped(planted):
	# polyculture(), but the caller carries a memory of what it planted where, so
	# a companion tile that is already correct costs a dictionary lookup rather
	# than a round trip. A move is 200 ticks; the lookup is a handful.
	#
	# `planted` must only ever hold this drone's own plantings. A stale entry
	# causes a *skip*, and a wrong skip forfeits the 67x polyculture multiplier on
	# that harvest — far more expensive than the walk it saved. So entries are
	# written only straight after this drone plants, and the tile is still
	# verified with get_entity_type() on any pass where we do walk.
	x, y = get_pos_x(), get_pos_y()
	companion = get_companion()
	if companion == None:
		return
	plant_type, (px, py) = companion
	if not affordable(plant_type):
		return
	key = (px, py)
	if key in planted:
		if planted[key] == plant_type:
			return
	move_to(px, py)
	if get_entity_type() != plant_type:
		harvest()
		plant_companion(plant_type)
	planted[key] = plant_type
	move_to(x, y)

def polyculture():
	x, y = get_pos_x(), get_pos_y()
	companion = get_companion()
	# get_companion() returns None when the plant underfoot has no preference.
	if companion == None:
		return
	plant_type, (px, py) = companion
	# Do not walk somewhere to fail. A companion we cannot afford — in practice
	# Carrot, at 512 hay and 512 wood — will not be planted when we arrive, so
	# the trip earns no multiplier and costs the full round trip: ~800 ticks of
	# movement at 200 a move. Checking costs one tick for get_cost and one per
	# item, and it is worth it on roughly a third of passes.
	#
	# The harvest back home still happens, unmultiplied. That is strictly better
	# than paying for the walk and getting the same unmultiplied harvest, and it
	# is *not* what 006 did: 006 rerolled by harvesting the mature grass while
	# the companion was still unsatisfied, collecting the crop at 1x and throwing
	# away the very multiplier it was trying to win.
	if not affordable(plant_type):
		return
	move_to(px, py)
	# Only disturb the companion tile if it is not already what it needs to be.
	#
	# A successful operating function costs 200 ticks and a failed one costs 1
	# (see docs/wiki/Operation-Costs.md), so the harvest-and-replant pair here is
	# 400 ticks of a ~1400 tick pass. It buys a companion that was already
	# standing there, and its yield is wood or fruit rather than the crop being
	# farmed — nothing that counts towards a resource leaderboard's target.
	#
	# get_entity_type() costs 1 tick, so checking is close to free.
	if get_entity_type() != plant_type:
		harvest()
		plant_companion(plant_type)
	move_to(x, y)

