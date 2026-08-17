# exp-carrots_single-005 -- finish-and-score
#
# carrots_single's first real driver. Design settled by 001-004
# (experiments/carrots_single/queue.md has the full trail): 3 Carrot
# tiles round-robin at pairwise wrapped distance 4 (self-collision
# structurally impossible, since companion range is <=3), free-Grass
# companion skip (untouched grassland already has standing Grass -- 002),
# full walk-service for Bush/Tree with a revert back to Grass afterward so
# the free rate doesn't erode. This category is growth-bound (~71% idle on
# a single tile, 003), and 3 tiles nearly eliminate that idle time,
# measuring 2.44x the single-tile throughput (004). Projects ~11.5
# minutes to the real 100,000,000 target.

TARGET = 100000000
TILES = [(0, 0), (0, 4), (2, 2)]
TILE_SET = set(TILES)

def move_wrapped(x, y):
	N = get_world_size()
	while get_pos_x() != x:
		if (x - get_pos_x()) % N <= N // 2:
			move(East)
		else:
			move(West)
	while get_pos_y() != y:
		if (y - get_pos_y()) % N <= N // 2:
			move(North)
		else:
			move(South)

def own_tile_ready():
	if get_ground_type() != Grounds.Soil:
		till()
	if get_entity_type() != Entities.Carrot:
		plant(Entities.Carrot)

def water_here():
	while num_items(Items.Water) > 0 and get_water() < 0.999:
		use_item(Items.Water)

for t in TILES:
	move_wrapped(t[0], t[1])
	own_tile_ready()
	water_here()

i = 0
while num_items(Items.Carrot) < TARGET:
	tx, ty = TILES[i % len(TILES)]
	i = i + 1
	move_wrapped(tx, ty)
	water_here()

	companion = get_companion()
	serviced_pos = None
	if companion != None:
		ctype, pos = companion
		if ctype != Entities.Grass and pos not in TILE_SET:
			move_wrapped(pos[0], pos[1])
			if get_ground_type() != Grounds.Grassland:
				till()
			if get_entity_type() != ctype:
				harvest()
				plant(ctype)
			serviced_pos = pos
			move_wrapped(tx, ty)

	h = can_harvest()
	while not h and num_items(Items.Carrot) < TARGET:
		h = can_harvest()
	if num_items(Items.Carrot) >= TARGET:
		break
	harvest()

	if serviced_pos != None:
		move_wrapped(serviced_pos[0], serviced_pos[1])
		harvest()
		plant(Entities.Grass)
		move_wrapped(tx, ty)
	own_tile_ready()

quick_print("DONE", "CARROT", num_items(Items.Carrot), "TICK_FINAL", get_tick_count(),
	"TIME_FINAL", get_time())
