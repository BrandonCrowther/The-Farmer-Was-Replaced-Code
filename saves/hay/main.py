import Common

# exp-hay-047 -- pinpoint the walk-servicing tick blowup
#
# 046 found "walk" servicing costs wildly inflated (many 12,000-26,000
# tick samples vs ~800-2,000 expected) and that the champion's own
# "water is 10x short" comment is wrong (real water sits at 0.8-1.0).
# Splits the walk into move-out / service-action / move-back to find
# where the blowup actually is.
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

# Main drone: instrumented, bounded. Matches the real champion's
# driver(3, 3) exactly -- home is a hardcoded target, not "wherever we
# happen to be" (047's r1 bug: it captured position before moving,
# making move_to(ax,ay) a no-op and effectively measuring from (0,0)
# instead of the champion's real (3,3), which sits safely away from
# the world seam).
ax, ay = 3, 3
Common.move_to(ax, ay)
instructions()
planted = {}
t_start = get_tick_count()

for c in range(CYCLES):
	while num_items(Items.Water) > 0 and get_water() < 0.75:
		use_item(Items.Water)

	companion = get_companion()
	logged = False
	if companion != None:
		plant_type, (px, py) = companion
		if Common.affordable(plant_type):
			key = (px, py)
			if not (key in planted and planted[key] == plant_type):
				dist = abs(px - ax) + abs(py - ay)
				t0 = get_tick_count()
				Common.move_to(px, py)
				t1 = get_tick_count()
				if get_entity_type() != plant_type:
					harvest()
					Common.plant_companion(plant_type)
				t2 = get_tick_count()
				planted[key] = plant_type
				Common.move_to(ax, ay)
				t3 = get_tick_count()
				quick_print("WALK", "c", c, "type", plant_type, "dist", dist,
					"MOVE_OUT", t1 - t0, "SVC_ACTION", t2 - t1, "MOVE_BACK", t3 - t2,
					"pos", (px, py))
				logged = True

	if not logged:
		Common.polyculture_mapped(planted)

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

t_total = get_tick_count() - t_start
quick_print("SUMMARY", "CYCLES", CYCLES, "TICKS", t_total, "TICKS_PER_HARVEST", t_total / CYCLES)

for d in drones:
	wait_for(d)
