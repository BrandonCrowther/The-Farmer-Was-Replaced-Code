import Common

# exp-hay-049 -- reroll-before-walk retest, correctly timed, REROLL_LIMIT=5
#
# 038's rejection assumed a 44-66% baseline hit rate. 046/047's fresh
# measurement (with the real (3,3) home, not 047-r1's accidental (0,0))
# shows walk-rate 63% (hit-rate ~37%), at or below that range -- real
# slack for reroll-before-walk. Full generalized reroll against the
# memory dict (any type), REROLL_LIMIT=5 (hay_single's proven near-
# optimal cap), timed immediately after planting -- before any growth
# accrues, matching hay_single's exact winning shape and the lesson
# from carrots_single exp-007 (reroll must happen at plant time, not a
# lap later).
#
# Bounded to ~150 cycles on the main drone -- not chasing the target.
# Expect "Run Failed"; the duration is not a score.

REROLL_LIMIT = 5
entity = Entities.Grass
instructions = Common.get_planting_instructions(entity)
CYCLES = 150

def settle(hx, hy, planted):
	instructions()
	companion = get_companion()
	rerolls = 0
	walked = False
	while companion != None:
		ctype, (cx, cy) = companion
		key = (cx, cy)
		if key in planted and planted[key] == ctype:
			break
		if rerolls < REROLL_LIMIT:
			harvest()
			instructions()
			companion = get_companion()
			rerolls = rerolls + 1
		else:
			if Common.affordable(ctype):
				Common.move_to(cx, cy)
				if get_entity_type() != ctype:
					harvest()
					Common.plant_companion(ctype)
				planted[key] = ctype
				Common.move_to(hx, hy)
				walked = True
			break
	return walked

def driver(x, y):
	Common.move_to(x, y)
	planted = {}
	settle(x, y, planted)
	for i in range(CYCLES + 20):
		while num_items(Items.Water) > 0 and get_water() < 0.75:
			use_item(Items.Water)
		h = can_harvest()
		while not h:
			h = can_harvest()
		harvest()
		settle(x, y, planted)

clear()
HOLES = [(1, 1), (1, 4), (4, 1), (4, 4)]
drones = []
for i in range(6):
	for j in range(6):
		if i + j != 0:
			if (i, j) not in HOLES:
				d = spawn_drone(driver, 3 + i*5, 3 + j*5)
				if d:
					drones.append(d)

# Main drone: instrumented, bounded.
ax, ay = 3, 3
Common.move_to(ax, ay)
planted = {}
settle(ax, ay, planted)

hits_skip = 0
hits_walk = 0
t_start = get_tick_count()
for c in range(CYCLES):
	while num_items(Items.Water) > 0 and get_water() < 0.75:
		use_item(Items.Water)
	h = can_harvest()
	while not h:
		h = can_harvest()
	harvest()
	walked = settle(ax, ay, planted)
	if walked:
		hits_walk = hits_walk + 1
	else:
		hits_skip = hits_skip + 1

t_total = get_tick_count() - t_start
quick_print("SUMMARY", "CYCLES", CYCLES, "HITS_SKIP", hits_skip, "HITS_WALK", hits_walk,
	"TICKS", t_total, "TICKS_PER_HARVEST", t_total / CYCLES)

for d in drones:
	wait_for(d)
