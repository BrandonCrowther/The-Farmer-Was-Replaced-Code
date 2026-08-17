import Common

# exp-hay-051 -- tighter packing (spacing 4, not 5)
#
# 050 confirmed drones are truly isolated (no shared mutable state) --
# the only channel between drones is the physical game world. Reducing
# spacing from 5 to 4 (still > companion range 3, still self-collision
# safe, brute-force confirmed) packs the same 32 drones into a smaller
# region, increasing companion-footprint overlap and should raise the
# real (physical, non-reroll) skip rate.
#
# Bounded to ~150 cycles on the main drone -- not chasing the target.
# Expect "Run Failed"; the duration is not a score.

REROLL_LIMIT = 2
entity = Entities.Grass
instructions = Common.get_planting_instructions(entity)
CYCLES = 150

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
		while rerolls < REROLL_LIMIT and companion != None and companion[0] == Entities.Carrot:
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
				d = spawn_drone(driver, 2 + i * 4, 2 + j * 4)
				if d:
					drones.append(d)
quick_print("SPAWNED", len(drones) + 1, "of", max_drones())

# Main drone: instrumented, bounded.
ax, ay = 2, 2
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
	while rerolls < REROLL_LIMIT and companion2 != None and companion2[0] == Entities.Carrot:
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
