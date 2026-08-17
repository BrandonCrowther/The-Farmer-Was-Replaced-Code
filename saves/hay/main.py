import Common

# exp-hay-046 -- full diagnostic re-probe (post-checkpoint)
#
# Real 32-drone contention (unchanged spawn structure), but the main
# drone's loop is instrumented to log the full per-cycle breakdown:
# yield, companion type, servicing outcome, ticks spent servicing vs
# idle, and the real achieved water level. polyculture_mapped()'s logic
# is inlined here (not modified in Common.py) so each branch can be
# logged without changing the champion's actual behavior.
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
				d = spawn_drone(driver, 3 + i*5, 3 + j*5)
				if d:
					drones.append(d)

# Main drone: instrumented, bounded.
ax, ay = get_pos_x(), get_pos_y()
Common.move_to(ax, ay)
instructions()
planted = {}

hits_skip = 0
hits_walk = 0
hits_unaffordable = 0
hits_no_companion = 0
carrot_final = 0
total_gained = 0
t_start = get_tick_count()

for c in range(CYCLES):
	while num_items(Items.Water) > 0 and get_water() < 0.75:
		use_item(Items.Water)

	t_svc_start = get_tick_count()
	water_now = get_water()
	companion = get_companion()
	outcome = "none"
	if companion == None:
		hits_no_companion = hits_no_companion + 1
	else:
		plant_type, (px, py) = companion
		if not Common.affordable(plant_type):
			hits_unaffordable = hits_unaffordable + 1
			outcome = "unaffordable_" + str(plant_type)
		else:
			key = (px, py)
			if key in planted and planted[key] == plant_type:
				hits_skip = hits_skip + 1
				outcome = "skip"
			else:
				Common.move_to(px, py)
				if get_entity_type() != plant_type:
					harvest()
					Common.plant_companion(plant_type)
				planted[key] = plant_type
				Common.move_to(ax, ay)
				hits_walk = hits_walk + 1
				outcome = "walk"
	t_svc_end = get_tick_count()

	h = can_harvest()
	while not h:
		h = can_harvest()
	t_ripe = get_tick_count()

	before = num_items(Items.Hay)
	harvest()
	gained = num_items(Items.Hay) - before
	total_gained = total_gained + gained

	rerolls = 0
	instructions()
	companion2 = get_companion()
	while rerolls < REROLL_LIMIT and companion2 != None and companion2[0] == Entities.Carrot:
		harvest()
		instructions()
		companion2 = get_companion()
		rerolls = rerolls + 1
	if companion2 != None and companion2[0] == Entities.Carrot:
		carrot_final = carrot_final + 1

	if c < 15 or c % 10 == 0:
		quick_print("CYCLE", c, "OUTCOME", outcome, "GAINED", gained, "REROLLS", rerolls,
			"SVC_TICKS", t_svc_end - t_svc_start, "IDLE_TICKS", t_ripe - t_svc_end,
			"WATER", water_now)

t_total = get_tick_count() - t_start
quick_print("SUMMARY", "CYCLES", CYCLES, "HITS_SKIP", hits_skip, "HITS_WALK", hits_walk,
	"HITS_UNAFFORDABLE", hits_unaffordable, "HITS_NO_COMPANION", hits_no_companion,
	"CARROT_FINAL_UNRESOLVED", carrot_final, "TOTAL_GAINED", total_gained,
	"TICKS", t_total, "TICKS_PER_HARVEST", t_total / CYCLES, "HAY_PER_TICK", total_gained / t_total)

for d in drones:
	wait_for(d)
