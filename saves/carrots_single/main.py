# exp-carrots_single-003 -- reactive-single-tile probe
#
# Exploits both findings from 001/002: Grass companions are free (skip,
# trust the board's default state -- 002 confirmed untouched grassland
# already has Grass standing on it), and the massive starting stockpile
# means resource cost of planting/replanting Carrot is a non-issue (only
# ticks matter). Bush/Tree companions are serviced with a real walk, and
# the position is reverted back to Grass afterward so the free-grass rate
# doesn't erode over the run.
#
# Sequence per cycle: service the companion for the plant *currently
# growing* (skip if Grass, walk+plant if Bush/Tree), wait for ripeness,
# harvest (collects the multiplier if serviced), revert the serviced
# position back to Grass, replant our own tile fresh.
#
# Instrumented like Hay's 041 to answer the same growth-schedulability
# question directly: is this category growth-bound (idle time exists) or
# servicing-bound (it doesn't), before deciding whether multi-tile is
# worth building.
#
# Not chasing the target -- terminates after a bounded number of cycles.
# Expect "Run Failed"; the duration is not a score.

HOME = (get_pos_x(), get_pos_y())

def own_tile_ready():
	if get_ground_type() != Grounds.Soil:
		till()
	if get_entity_type() != Entities.Carrot:
		plant(Entities.Carrot)

def water_home():
	# BUG FIX: the first run of this probe never watered at all, so growth
	# ran at the unwatered 1x rate (~36,420 ticks, matching Plant-growth.md's
	# 6.0s mean * ~6,070 ticks/s) instead of 001's watered ~7,196. Water the
	# home tile toward the same ~0.999 level 001 measured under.
	while num_items(Items.Water) > 0 and get_water() < 0.999:
		use_item(Items.Water)

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

own_tile_ready()
water_home()

CYCLES = 40
harvests = 0
hits_grass = 0
hits_serviced = 0
t_start = get_tick_count()
for i in range(CYCLES):
	t_plant = get_tick_count()
	companion = get_companion()
	serviced_pos = None
	if companion != None:
		ctype, pos = companion
		if ctype == Entities.Grass:
			hits_grass = hits_grass + 1
		else:
			move_wrapped(pos[0], pos[1])
			if get_ground_type() != Grounds.Grassland:
				till()
			if get_entity_type() != ctype:
				# BUG FIX (r1): plant() does not overwrite an existing
				# entity -- a revisited position holding Grass (from an
				# earlier revert) silently failed to become Bush/Tree,
				# costing the multiplier on 2/40 cycles in r1. harvest()
				# first, matching Common.py's polyculture_mapped pattern.
				harvest()
				plant(ctype)
			serviced_pos = pos
			move_wrapped(HOME[0], HOME[1])
			hits_serviced = hits_serviced + 1
	t_serviced = get_tick_count()
	h = can_harvest()
	while not h:
		h = can_harvest()
	t_ripe = get_tick_count()
	before = num_items(Items.Carrot)
	harvest()
	gained = num_items(Items.Carrot) - before
	harvests = harvests + 1
	if serviced_pos != None:
		move_wrapped(serviced_pos[0], serviced_pos[1])
		harvest()
		plant(Entities.Grass)
		move_wrapped(HOME[0], HOME[1])
	own_tile_ready()
	water_home()
	t_end = get_tick_count()
	if i < 10 or i % 5 == 0:
		quick_print("CYCLE", i, "COMPANION", companion, "GAINED", gained,
			"SVC_TICKS", t_serviced - t_plant, "IDLE_TICKS", t_ripe - t_serviced,
			"TOTAL_TICKS", t_end - t_plant)

t_total = get_tick_count() - t_start
quick_print("SUMMARY", "CYCLES", CYCLES, "HARVESTS", harvests, "HITS_GRASS", hits_grass,
	"HITS_SERVICED", hits_serviced, "TICKS", t_total, "TICKS_PER_HARVEST", t_total / harvests,
	"CARROT", num_items(Items.Carrot), "HAY", num_items(Items.Hay), "WOOD", num_items(Items.Wood))
