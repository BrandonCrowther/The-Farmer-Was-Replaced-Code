import Common

# exp-carrots_single-006 -- reroll-before-walk probe (single tile)
#
# 003's single-tile design walked out to service every non-Grass
# companion draw (X ~ 3,333 ticks per 003's own backed-out number). This
# transplants hay_single's winning paradigm instead (008-013): the
# companion preference is fixed at plant time, so a cheap reroll (harvest
# + replant, ~400 ticks) redraws it, and we only fall back to a real walk
# after REROLL_LIMIT misses. hay_single's memory trick also applies
# unchanged: once a remote position is walked-and-serviced, it is *not*
# reverted -- it's left standing and remembered, so a future draw of the
# same (type, position) pair is a free hit too, same as Grass always is.
#
# Not chasing the target -- terminates after a bounded number of cycles.
# Expect "Run Failed"; the duration is not a score.

HOME = (get_pos_x(), get_pos_y())
REROLL_LIMIT = 5

def own_tile_ready():
	if get_ground_type() != Grounds.Soil:
		till()
	if get_entity_type() != Entities.Carrot:
		plant(Entities.Carrot)

def water_home():
	while num_items(Items.Water) > 0 and get_water() < 0.999:
		use_item(Items.Water)

own_tile_ready()
water_home()

# What this drone believes it has planted, keyed by companion position --
# same authoritative-memory pattern as hay_single's main.py, since only
# this drone ever touches the farm.
planted = {}

CYCLES = 40
harvests = 0
hits_grass = 0
hits_reroll = 0
hits_walk = 0
t_start = get_tick_count()
for i in range(CYCLES):
	t_plant = get_tick_count()
	companion = get_companion()
	rerolls = 0
	walked = False
	while companion != None:
		ctype, pos = companion
		key = pos
		# BUG FIX (r1 -> r2): "Grass is free" only holds for a position
		# this drone has never touched. Once a walk-service permanently
		# converts a remote position away from Grass (no revert, unlike
		# 003 -- see header), a later Grass-companion draw landing on that
		# same position is NOT actually satisfied. Must check the memory
		# dict either way, not just short-circuit on ctype == Grass.
		if key in planted:
			if planted[key] == ctype:
				hits_reroll = hits_reroll + 1
				break
		elif ctype == Entities.Grass:
			hits_grass = hits_grass + 1
			break
		if rerolls < REROLL_LIMIT:
			harvest()
			plant(Entities.Carrot)
			companion = get_companion()
			rerolls = rerolls + 1
		else:
			if Common.affordable(ctype):
				Common.move_to_wrapped(pos[0], pos[1])
				if get_entity_type() != ctype:
					harvest()
					Common.plant_companion(ctype)
				planted[key] = ctype
				Common.move_to_wrapped(HOME[0], HOME[1])
				hits_walk = hits_walk + 1
				walked = True
			break
	t_serviced = get_tick_count()
	h = can_harvest()
	while not h:
		h = can_harvest()
	t_ripe = get_tick_count()
	before = num_items(Items.Carrot)
	harvest()
	gained = num_items(Items.Carrot) - before
	harvests = harvests + 1
	own_tile_ready()
	water_home()
	t_end = get_tick_count()
	if i < 10 or i % 5 == 0:
		quick_print("CYCLE", i, "COMPANION", companion, "GAINED", gained, "REROLLS", rerolls,
			"WALKED", walked, "SVC_TICKS", t_serviced - t_plant, "IDLE_TICKS", t_ripe - t_serviced,
			"TOTAL_TICKS", t_end - t_plant)

t_total = get_tick_count() - t_start
quick_print("SUMMARY", "CYCLES", CYCLES, "HARVESTS", harvests, "HITS_GRASS", hits_grass,
	"HITS_REROLL", hits_reroll, "HITS_WALK", hits_walk, "TICKS", t_total,
	"TICKS_PER_HARVEST", t_total / harvests, "CARROT", num_items(Items.Carrot))
