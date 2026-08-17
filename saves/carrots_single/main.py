# exp-carrots_single-004 -- multi-tile-pipeline probe
#
# 003 measured single-tile carrots_single as ~71% idle (growth ~7,196
# ticks vs ~2,422 ticks of handling per cycle) -- the first category
# tonight where multi-tile looks genuinely promising, not just plausible.
# Model: with N tiles round-robin, once N * (handling + commute) exceeds
# growth, idle drops to ~0 and throughput plateaus at yield/handling_per_
# tile, independent of further N -- the crossover here is N ~= 7,196 /
# 3,222 (handling ~2,422 + ~800 average commute at distance 4) ~= 2.23,
# so N=3 should already be at or past the plateau. Predicted: ~25.4
# carrots/tick, ~2.6x over 003's single-tile 9.80.
#
# Tiles at (0,0), (0,4), (2,2) -- computed to be pairwise wrapped distance
# exactly 4, safely outside every tile's own companion range (<=3), so no
# tile's companion request can ever name another of our own tiles (the
# self-collision hazard hay_single's 005 and Hay's 044 had to guard
# against) -- avoided by construction here, with a defensive check kept
# anyway since it's nearly free.
#
# Not chasing the target -- terminates after a bounded number of cycles.
# Expect "Run Failed"; the duration is not a score.

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

CYCLES = 60
harvests = 0
hits_grass = 0
hits_serviced = 0
hits_guard = 0
t_start = get_tick_count()
for i in range(CYCLES):
	tx, ty = TILES[i % len(TILES)]
	move_wrapped(tx, ty)
	water_here()

	companion = get_companion()
	serviced_pos = None
	if companion != None:
		ctype, pos = companion
		if ctype == Entities.Grass:
			hits_grass = hits_grass + 1
		elif pos in TILE_SET:
			# Defensive only -- distance-4 spacing should make this
			# unreachable, since companion range is <=3.
			hits_guard = hits_guard + 1
		else:
			move_wrapped(pos[0], pos[1])
			if get_ground_type() != Grounds.Grassland:
				till()
			if get_entity_type() != ctype:
				harvest()
				plant(ctype)
			serviced_pos = pos
			move_wrapped(tx, ty)
			hits_serviced = hits_serviced + 1

	h = can_harvest()
	while not h:
		h = can_harvest()
	harvest()
	harvests = harvests + 1
	if serviced_pos != None:
		move_wrapped(serviced_pos[0], serviced_pos[1])
		harvest()
		plant(Entities.Grass)
		move_wrapped(tx, ty)
	own_tile_ready()

t_total = get_tick_count() - t_start
quick_print("SUMMARY", "CYCLES", CYCLES, "HARVESTS", harvests, "HITS_GRASS", hits_grass,
	"HITS_SERVICED", hits_serviced, "HITS_GUARD", hits_guard, "TICKS", t_total,
	"TICKS_PER_HARVEST", t_total / harvests, "CARROT", num_items(Items.Carrot))
