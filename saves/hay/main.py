import Common

# exp-hay-073 -- first multi-drone champion built on the two-tile
# interleaving design (070-072). Single-drone smoke tests measured
# 923.53 ticks/harvest (water=0.75, direct move, all-static-bush
# companion policy), vs the single-tile champion's real ~1068-1220 and
# the honest floor of 615 -- this is the first real leaderboard attempt
# against those findings, not another smoke test.
#
# Each drone now owns TWO adjacent Hay tiles (base, base+East) instead
# of one, round-robining between them so growth on one tile hides
# behind the reroll-chase on the other (confirmed: wait~=1 tick/harvest
# in the single-drone tests). Every position within distance 3 of
# EITHER tile is pre-seeded once as permanent Bush -- accept a
# companion draw the instant it's a memory-matched Bush; anything else
# is cheap to reroll (207/attempt), never worth walking to.
#
# Macro-layout risk: at the champion's original 5-tile drone spacing, a
# drone's bush-wall (reaching 3 past its offset tile, i.e. 4 tiles out)
# comes within 1 tile of a same-row neighbor's own crop tiles -- a real
# collision risk if unhandled. Fixed two ways: (1) every drone's setup
# loop checks against ALL_CROPS, the full precomputed set of every
# drone's two tiles, not just its own -- geometry alone was judged too
# tight to trust; (2) overlapping BUSH WALLS between neighbors are
# harmless by design, since every drone wants the same thing (Bush) at
# any shared position -- only crop-tile collisions are dangerous, and
# those are the ones explicitly excluded.

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
		instructions()
		companion = get_companion()
		while rerolls < REROLL_LIMIT and companion != None:
			ctype, (cx, cy) = companion
			key = (cx, cy)
			if key in planted and planted[key] == ctype:
				break
			harvest()
			instructions()
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
