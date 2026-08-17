import Common

# exp-carrots-001 -- terminate the seeded achievement driver
#
# Structurally identical to wood (multi)'s seeded driver (32 drones,
# one per column, interleaved Grass companion pattern), which just
# scored 06:07.889/#111 for a 10-billion target after only
# target-gating + a water-guard. Same fix applied here.

entity = Entities.Carrot
instructions = Common.get_planting_instructions(entity)
TARGET = 2000000000

def driver(x, y):
	Common.move_to(x, y)
	while num_items(Items.Carrot) < TARGET:
		Common.await_harvest()
		while num_items(Items.Water) > 0 and get_water() < 0.5:
			use_item(Items.Water)
		harvest()
		instructions()
		loop = False
		while loop == False:
			harvest()
			plant(entity)
			plant_type, (px, py) = get_companion()
			if plant_type == Entities.Grass:
				if abs(x - px) + abs(y - py) != 2:
					loop = True
		move(North)
		move(North)

clear()
for x in range(1, get_world_size()):
	spawn_drone(driver, x, x % 2)
driver(0, 0)

quick_print("DONE", "CARROT", num_items(Items.Carrot), "TICK_FINAL", get_tick_count(),
	"TIME_FINAL", get_time())
