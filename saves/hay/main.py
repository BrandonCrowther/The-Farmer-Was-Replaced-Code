import Common

# exp-hay-075 -- drop instructions() from the hot loop entirely.
# 066/067 already proved Grass auto-regrows and harvest() alone -- no
# ripeness check needed -- correctly destroys/regrows it every time,
# 200 ticks, 0 yield, still Grass after. 073's champion still called
# instructions() once after the real harvest AND once per reroll
# attempt anyway -- ~3.1 calls/harvest at 7 ticks each, pure guard-
# check overhead that never fires (entity_type is never anything but
# Grass to guard against). Only the two INITIAL calls (first planting
# of each tile, starting from empty ground) are load-bearing.
#
# Single-drone smoke test (075): 873.02 ticks/harvest, down from 073's
# 889.78 -- confirms the ~17-tick saving, landing within 17 ticks of
# the #2-10 cluster's upper bound (856).
#
# Everything else unchanged from 073: two adjacent Hay tiles per drone
# (base, base+East), round-robining so growth on one hides behind the
# reroll-chase on the other; every position within distance 3 of
# either tile pre-seeded once as permanent Bush; water threshold 0.75;
# direct move() for the known single-hop; global ALL_CROPS exclusion
# set so no drone's bush-wall setup can overwrite another's crop tile.

TARGET = 2000000000
REROLL_LIMIT = 30
WATER_THRESHOLD = 0.75
entity = Entities.Grass
instructions = Common.get_planting_instructions(entity)

HOLES = [(1, 1), (1, 4), (4, 1), (4, 4)]

ALL_BASES = [(3, 3)]
for i in range(6):
	for j in range(6):
		if i + j != 0:
			if (i, j) not in HOLES:
				ALL_BASES.append((3 + i * 5, 3 + j * 5))

ALL_CROPS = {}
for base in ALL_BASES:
	bx, by = base
	ALL_CROPS[(bx, by)] = True
	ALL_CROPS[(bx + 1, by)] = True

def wdist(ax, ay, bx, by, size):
	dx = min((bx - ax) % size, (ax - bx) % size)
	dy = min((by - ay) % size, (ay - by) % size)
	return dx + dy

def driver(bx, by):
	size = get_world_size()
	c1x, c1y = bx, by
	c2x, c2y = bx + 1, by

	Common.move_to(c1x, c1y)
	instructions()
	Common.move_to(c2x, c2y)
	instructions()

	planted = {}
	for dx in range(-3, 5):
		for dy in range(-3, 4):
			px = (c1x + dx) % size
			py = (c1y + dy) % size
			if (px, py) in ALL_CROPS:
				continue
			d1 = wdist(c1x, c1y, px, py, size)
			d2 = wdist(c2x, c2y, px, py, size)
			if d1 <= 3 or d2 <= 3:
				Common.move_to(px, py)
				if get_entity_type() != Entities.Bush:
					if get_entity_type() != None:
						harvest()
					Common.plant_companion(Entities.Bush)
				planted[(px, py)] = Entities.Bush
	Common.move_to(c1x, c1y)

	current_is_c1 = True
	while num_items(Items.Hay) < TARGET:
		while num_items(Items.Water) > 0 and get_water() < WATER_THRESHOLD:
			use_item(Items.Water)
		h = can_harvest()
		while not h and num_items(Items.Hay) < TARGET:
			while num_items(Items.Water) > 0 and get_water() < WATER_THRESHOLD:
				use_item(Items.Water)
			h = can_harvest()
		if num_items(Items.Hay) >= TARGET:
			break
		harvest()

		rerolls = 0
		companion = get_companion()
		while rerolls < REROLL_LIMIT and companion != None:
			ctype, (cx, cy) = companion
			key = (cx, cy)
			if key in planted and planted[key] == ctype:
				break
			harvest()
			companion = get_companion()
			rerolls = rerolls + 1

		if num_items(Items.Hay) >= TARGET:
			break
		if current_is_c1:
			move(East)
		else:
			move(West)
		current_is_c1 = not current_is_c1

clear()
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
