import Common

# exp-hay-057 -- full memory-matched reroll-before-walk, real full run
#
# Champion only rerolls to escape Carrot (REROLL_LIMIT=2). This rerolls
# toward ANY memory-matched companion (any type), REROLL_LIMIT=5 --
# hay_single's proven cap -- since Hay has no free-type shortcut (Grass
# excludes itself as a companion), memory has to mature over many
# cycles; 049's 150-cycle probe couldn't see that, the real run gives
# each drone ~871 cycles. Water threshold raised to 0.999 (056/046/047
# found the champion's "10x short" comment measured wrong -- real
# water sits at 0.8-1.0 already).

TARGET = 2000000000
REROLL_LIMIT = 5
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
