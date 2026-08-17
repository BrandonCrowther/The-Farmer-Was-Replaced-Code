import Common

# Leaderboards.Hay succeeds when num_items(Items.Hay) >= TARGET is true *at the
# moment the program ends*. The simulation never stops on its own, so every drone
# has to notice the target and return, and the main drone has to outlive them all.
TARGET = 2000000000

REROLL_LIMIT = 2

entity = Entities.Grass
instructions = Common.get_planting_instructions(entity)

# exp-hay-044 -- multi-tile-scheduled probe
#
# 041 measured real idle time on the main drone: ~68% of passes are misses
# (a real walk, no slack), but ~32% are hits (memory skip, ~20-30 ticks)
# and then genuinely idle-wait ~492 ticks for the plant to ripen. This
# tests using that specific window, and only that window, to tend a second
# tile -- not a blind second plot the way 027/029 were (030's postmortem:
# they assumed idle time rather than measuring it; this time it's
# measured).
#
# The scheduling: peek tile A's companion request cheaply (get_companion()
# is free, a dict lookup is a few ticks) *before* deciding whether to
# service it. If it would be cheap (memory hit, unaffordable-skip, or the
# tile itself is unsatisfiable), go tend tile B during the freed time. If
# it would be expensive (a real walk), skip B this cycle entirely and just
# do A's walk -- exactly the case with no slack to spend.
#
# Two tiles at distance 1 (cheapest possible commute, ~200 ticks each way)
# means each is inside the other's companion range, so a same-tile guard
# (FARM_TILES) is required -- 005's bug, avoided by construction this time
# per 013/015's fix.
TILE_A = (3, 3)
TILE_B = (4, 3)
FARM_TILES = set([TILE_A, TILE_B])

def peek_cheap(planted):
	# Returns (cheap, companion) without walking anywhere.
	companion = get_companion()
	if companion == None:
		return True, companion
	ctype, key = companion
	if key in FARM_TILES:
		return True, companion
	if not Common.affordable(ctype):
		return True, companion
	if key in planted and planted[key] == ctype:
		return True, companion
	return False, companion

def service_now(pos_self, companion, planted):
	if companion == None:
		return
	ctype, key = companion
	if key in FARM_TILES:
		return
	if not Common.affordable(ctype):
		return
	if key in planted and planted[key] == ctype:
		return
	Common.move_to_wrapped(key[0], key[1])
	if get_entity_type() != ctype:
		harvest()
		Common.plant_companion(ctype)
	planted[key] = ctype
	Common.move_to_wrapped(pos_self[0], pos_self[1])

def scheduled_probe():
	Common.move_to_wrapped(TILE_A[0], TILE_A[1])
	instructions()
	Common.move_to_wrapped(TILE_B[0], TILE_B[1])
	instructions()
	Common.move_to_wrapped(TILE_A[0], TILE_A[1])
	planted = {}
	harvests_a = 0
	harvests_b = 0
	cycles = 80
	t_start = get_tick_count()
	for i in range(cycles):
		while num_items(Items.Water) > 0 and get_water() < 0.75:
			use_item(Items.Water)
		cheap, companion = peek_cheap(planted)
		if cheap:
			Common.move_to_wrapped(TILE_B[0], TILE_B[1])
			while num_items(Items.Water) > 0 and get_water() < 0.75:
				use_item(Items.Water)
			_, companion_b = peek_cheap(planted)
			service_now(TILE_B, companion_b, planted)
			if can_harvest():
				harvest()
				harvests_b = harvests_b + 1
				instructions()
			Common.move_to_wrapped(TILE_A[0], TILE_A[1])
		else:
			service_now(TILE_A, companion, planted)
		h = can_harvest()
		while not h:
			h = can_harvest()
		harvest()
		harvests_a = harvests_a + 1
		instructions()
	t_end = get_tick_count()
	total_h = harvests_a + harvests_b
	quick_print("SCHEDULED", "HARVESTS_A", harvests_a, "HARVESTS_B", harvests_b,
		"TOTAL", total_h, "TICKS", t_end - t_start,
		"TICKS_PER_HARVEST", (t_end - t_start) / total_h)

def driver(x, y):
	Common.move_to(x, y)
	instructions()
	planted = {}
	for i in range(5):
		while num_items(Items.Water) > 0 and get_water() < 0.75:
			use_item(Items.Water)
		Common.polyculture_mapped(planted)
		h = can_harvest()
		while not h:
			h = can_harvest()
		harvest()
		instructions()

clear()
HOLES = [(1, 1), (1, 4), (4, 1), (4, 4)]
quick_print("FARM", "world", get_world_size(), "max_drones", max_drones())
drones = []
for i in range(6):
	for j in range(6):
		if i + j != 0:
			if (i, j) not in HOLES:
				d = spawn_drone(driver, 3 + i * 5, 3 + j * 5)
				if d:
					drones.append(d)
quick_print("SPAWNED", len(drones) + 1, "of", max_drones())
scheduled_probe()
for d in drones:
	wait_for(d)
