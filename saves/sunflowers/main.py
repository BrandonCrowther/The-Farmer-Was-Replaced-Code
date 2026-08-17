import Common

# exp-sunflowers-001 -- terminate the seeded achievement driver
#
# Seeded design: 32 drones, each farming its own dedicated column (32
# tiles, wrapping) of the 32x32 world, continuous harvest+replant, base
# yield only (no max-petal 8x bonus tracking -- that's a possible
# future optimization, not needed for a first score). Target-gated both
# per-drone and the main drone's loop so it terminates. Guarded the
# water-topup loop against depletion -- saves/hay/main.py documents
# this exact unguarded shape spinning forever on failed use_item()
# calls once 32 drones exhaust a shared water pool.

entity = Entities.Sunflower
instructions = Common.get_planting_instructions(entity)
TARGET = 100000

def driver(x, y):
	Common.move_to(x, y)
	while num_items(Items.Power) < TARGET:
		while num_items(Items.Water) > 0 and get_water() < 0.75:
			use_item(Items.Water)
		if can_harvest():
			harvest()
		instructions()
		move(North)

clear()
for x in range(1, 32):
	spawn_drone(driver, x, 0)
driver(0, 0)

quick_print("DONE", "POWER", num_items(Items.Power), "TICK_FINAL", get_tick_count(),
	"TIME_FINAL", get_time())
