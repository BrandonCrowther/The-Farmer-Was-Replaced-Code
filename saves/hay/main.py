import Common

# exp-hay-054 -- reroll on distance>=2 (not just ==3), REROLL_LIMIT=5
#
# 053 tested distance==3 alone with REROLL_LIMIT=2 and regressed
# slightly -- the trigger rate (~2/3) is too high for only 2 reroll
# attempts to reliably land a cheap draw. Extending to distance>=2
# (only distance-1 draws accepted outright) raises the trigger rate
# further (~8/9) but pairs it with REROLL_LIMIT=5 (hay_single's proven
# cap) for enough attempts to actually find a cheap draw.
#
# Bounded to ~150 cycles on the main drone -- not chasing the target.
# Expect "Run Failed"; the duration is not a score.

REROLL_LIMIT = 5
entity = Entities.Grass
instructions = Common.get_planting_instructions(entity)
CYCLES = 150

def wdist(x, y, cx, cy):
	size = get_world_size()
	dx = min((cx - x) % size, (x - cx) % size)
	dy = min((cy - y) % size, (y - cy) % size)
	return dx + dy

def driver(x, y):
	Common.move_to(x, y)
	instructions()
	planted = {}
	for i in range(CYCLES + 20):
		while num_items(Items.Water) > 0 and get_water() < 0.75:
			use_item(Items.Water)
		Common.polyculture_mapped(planted)
		h = can_harvest()
		while not h:
			h = can_harvest()
		harvest()
		rerolls = 0
		instructions()
		companion = get_companion()
		while rerolls < REROLL_LIMIT and companion != None:
			ctype, (cx, cy) = companion
			bad = ctype == Entities.Carrot or wdist(x, y, cx, cy) >= 2
			if not bad:
				break
			harvest()
			instructions()
			companion = get_companion()
			rerolls = rerolls + 1

clear()
HOLES = [(1, 1), (1, 4), (4, 1), (4, 4)]
drones = []
for i in range(6):
	for j in range(6):
		if i + j != 0:
			if (i, j) not in HOLES:
				d = spawn_drone(driver, 3 + i * 5, 3 + j * 5)
				if d:
					drones.append(d)
quick_print("SPAWNED", len(drones) + 1, "of", max_drones())

# Main drone: instrumented, bounded.
ax, ay = 3, 3
Common.move_to(ax, ay)
instructions()
planted = {}

hits_skip = 0
hits_walk = 0
t_start = get_tick_count()
for c in range(CYCLES):
	while num_items(Items.Water) > 0 and get_water() < 0.75:
		use_item(Items.Water)

	companion = get_companion()
	walked = False
	if companion != None:
		plant_type, (px, py) = companion
		if Common.affordable(plant_type):
			key = (px, py)
			if key in planted and planted[key] == plant_type:
				pass
			else:
				Common.move_to(px, py)
				if get_entity_type() != plant_type:
					harvest()
					Common.plant_companion(plant_type)
				planted[key] = plant_type
				Common.move_to(ax, ay)
				walked = True

	h = can_harvest()
	while not h:
		h = can_harvest()
	harvest()

	rerolls = 0
	instructions()
	companion2 = get_companion()
	while rerolls < REROLL_LIMIT and companion2 != None:
		ctype2, (cx2, cy2) = companion2
		bad2 = ctype2 == Entities.Carrot or wdist(ax, ay, cx2, cy2) >= 2
		if not bad2:
			break
		harvest()
		instructions()
		companion2 = get_companion()
		rerolls = rerolls + 1

	if walked:
		hits_walk = hits_walk + 1
	else:
		hits_skip = hits_skip + 1

t_total = get_tick_count() - t_start
quick_print("SUMMARY", "CYCLES", CYCLES, "HITS_SKIP", hits_skip, "HITS_WALK", hits_walk,
	"TICKS", t_total, "TICKS_PER_HARVEST", t_total / CYCLES)

for d in drones:
	wait_for(d)
