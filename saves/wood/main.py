import Common

# exp-wood-001 -- terminate the seeded achievement driver
#
# Seeded design: 32 drones, one per column (alternating y-offset via
# x % 2), each cycling North by 2, harvest+replant with an interleaved
# Tree/Grass companion pattern. Not growth-pipelined (each drone fully
# waits via Common.await_harvest() before moving on) -- real yield/
# tick behavior observed empirically rather than fully hand-traced.
# Target-gated so it terminates; water-topup guarded against depletion
# (same fix as sunflowers exp-001 -- saves/hay/main.py documents this
# exact unguarded shape spinning forever on failed use_item() calls).

entity = Entities.Tree
instructions = Common.get_planting_instructions(entity)
TARGET = 10000000000

def driver(x, y):
	Common.move_to(x, y)
	while num_items(Items.Wood) < TARGET:
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

quick_print("DONE", "WOOD", num_items(Items.Wood), "TICK_FINAL", get_tick_count(),
	"TIME_FINAL", get_time())
