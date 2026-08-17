import Common
import Cactus

# exp-cactus-001 -- terminate the seeded achievement driver
#
# The seeded driver (from Cactus_Achievement.py) already implements the
# row-then-column adjacent-swap-free sort (via selection sort + physical
# move_item dragging) that cactus_single validated as a lemma: sorting
# every row, then every column, of a matrix leaves the rows still
# sorted -- so one row-sort pass (32 drones in parallel, one per row)
# followed by one column-sort pass (32 drones in parallel, one per
# column) fully sorts the whole grid in both dimensions at once.
#
# World size is 32 (confirmed via probe), and cascade yield is
# 32 * n**2 (same formula/constant as cactus_single, same
# num_unlocked(Unlocks.Cactus)=6 save state). 32 * 1024**2 = 33,554,432
# -- exactly this category's target. One full 32x32 grid, harvested
# once, should complete the whole run in a single cascade -- the
# seed's `while True:` outer loop is unnecessary; this runs the
# sequence exactly once.
#
# Each spawned drone is already self-terminating (the recursive spawn
# condition stops once num_drones() >= max_drones(), and each drone's
# driver() function has no internal loop -- it returns once its
# prep_field/sort/perform_sort finishes), so no extra bounding is
# needed there.

entity = Entities.Cactus
def driver(x, y, dir):
	Common.move_to(x, y)
	if num_drones() < max_drones():
		if dir == North or dir == South:
			spawn_drone(driver, x + 1, 0, dir)
		else:
			spawn_drone(driver, 0, y + 1, dir)
	instructions = Common.get_planting_instructions(entity)
	sizes = Cactus.prep_field(entity, dir, instructions)
	sorted = Cactus.sort_asc(sizes)
	Cactus.perform_sort(sorted, dir)

clear()

driver(0, 0, East)
count = num_drones()
while count > 1:
	count = num_drones()

driver(0, 0, North)
count = num_drones()
while count > 1:
	count = num_drones()

Common.move_to(0, 0)
before = num_items(Items.Cactus)
harvest()
gained = num_items(Items.Cactus) - before

quick_print("DONE", "GAINED", gained, "CACTUS", num_items(Items.Cactus), "TICK_FINAL",
	get_tick_count(), "TIME_FINAL", get_time())
