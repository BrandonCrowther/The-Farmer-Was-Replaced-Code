import Common

# exp-hay-060 -- hybrid accept policy (memory-hit OR distance-1) + wrapped setup
#
# Tick-budget model: total ticks/harvest = 400 (own handling) +
# max(S, 415 growth floor). Pure memory-only reroll's asymptotic S
# (p=1/3) is R(1-p)/p = 800 -- above the growth floor, so growth is
# never the binding constraint for that paradigm no matter the cap.
# Also accepting cheap real walks (distance-1, immediate + guaranteed,
# ~900 ticks) instead of always rerolling raises the effective accept
# probability and should lower S. Setup also switched from
# Common.move_to (unwrapped) to Common.move_to_wrapped -- free
# micro-optimization, cuts worst-case single-drone setup distance from
# 56 to 28.

TARGET = 2000000000
REROLL_LIMIT = 5
entity = Entities.Grass
instructions = Common.get_planting_instructions(entity)

def wdist(x, y, cx, cy):
	size = get_world_size()
	dx = min((cx - x) % size, (x - cx) % size)
	dy = min((cy - y) % size, (y - cy) % size)
	return dx + dy

def resolve(x, y, planted):
	instructions()
	companion = get_companion()
	rerolls = 0
	while companion != None:
		ctype, (cx, cy) = companion
		key = (cx, cy)
		if key in planted and planted[key] == ctype:
			return
		if wdist(x, y, cx, cy) == 1 or rerolls >= REROLL_LIMIT:
			if Common.affordable(ctype):
				Common.move_to_wrapped(cx, cy)
				if get_entity_type() != ctype:
					harvest()
					Common.plant_companion(ctype)
				planted[key] = ctype
				Common.move_to_wrapped(x, y)
			return
		harvest()
		instructions()
		companion = get_companion()
		rerolls = rerolls + 1

def driver(x, y):
	Common.move_to_wrapped(x, y)
	instructions()
	planted = {}
	while num_items(Items.Hay) < TARGET:
		while num_items(Items.Water) > 0 and get_water() < 0.999:
			use_item(Items.Water)
		h = can_harvest()
		while not h and num_items(Items.Hay) < TARGET:
			h = can_harvest()
		if num_items(Items.Hay) >= TARGET:
			break
		harvest()
		resolve(x, y, planted)

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
driver(3, 3)
for d in drones:
	wait_for(d)
