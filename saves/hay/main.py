import Common

# exp-hay-058 -- higher REROLL_LIMIT (10, not 5)
#
# 057 confirmed memory-matched reroll-before-walk is a real win over
# the full run. The mature per-draw hit rate (~1/3) compounds
# favorably with more attempts (1-(2/3)^(k+1)), and each attempt is
# cheap (400 ticks) relative to a real walk. Raising REROLL_LIMIT to
# 10 to capture more of that compounding.

TARGET = 2000000000
REROLL_LIMIT = 10
entity = Entities.Grass
instructions = Common.get_planting_instructions(entity)

def driver(x, y):
	Common.move_to(x, y)
	instructions()
	planted = {}
	while num_items(Items.Hay) < TARGET:
		while num_items(Items.Water) > 0 and get_water() < 0.999:
			use_item(Items.Water)
		Common.polyculture_mapped(planted)
		h = can_harvest()
		while not h and num_items(Items.Hay) < TARGET:
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
