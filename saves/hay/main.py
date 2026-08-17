import Common

# exp-hay-061 -- accept cheap draws only late in the reroll sequence
#
# 060's every-attempt hybrid accept tied 057 instead of beating it --
# likely an opportunity-cost problem: accepting a paid distance-1 walk
# on an early attempt forfeits the chance that more free rerolls would
# have found a real memory hit. Restricting the cheap-accept condition
# to only the last two reroll attempts preserves early free-hit
# chances while still avoiding the worst-case (fully exhausted budget,
# possibly distance-3) fallback.

TARGET = 2000000000
REROLL_LIMIT = 5
LATE_THRESHOLD = REROLL_LIMIT - 2
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
		cheap_late = rerolls >= LATE_THRESHOLD and wdist(x, y, cx, cy) <= 2
		if cheap_late or rerolls >= REROLL_LIMIT:
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
