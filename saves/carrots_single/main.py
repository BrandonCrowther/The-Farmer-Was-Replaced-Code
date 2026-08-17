# exp-carrots_single-002 -- natural-grass-growth-check
#
# 001 found every Grass-type companion request got satisfied (3/3, all
# multiplied) despite never planting anything there, while Bush/Tree
# requests never were (2/2, both bare). That's consistent with Grass.md's
# "Grass grows automatically on grassland" applying to *any* untouched
# grassland tile on the board, not just ones the drone has visited -- a
# free companion source for any crop that isn't Grass itself. This checks
# it directly: note a distant tile's entity type, do unrelated work for a
# while (several real seconds), then check the same tile again without
# ever having planted anything on it.
#
# Not chasing the target -- terminates after the check. Expect "Run
# Failed"; the duration is not a score.

Common_pos = (0, 0)
FAR = (5, 5)

quick_print("START_TICK", get_tick_count(), "START_TIME", get_time())

move(East)
move(East)
move(East)
move(East)
move(East)
move(North)
move(North)
move(North)
move(North)
move(North)
quick_print("AT_FAR", get_pos_x(), get_pos_y(), "ENTITY", get_entity_type(),
	"GROUND", get_ground_type(), "TICK", get_tick_count())

# Go back home and burn several real seconds doing unrelated carrot cycles
# -- the same real-time budget 001's 5 growth cycles used (~6.5s).
move(West)
move(West)
move(West)
move(West)
move(West)
move(South)
move(South)
move(South)
move(South)
move(South)
till()
for i in range(6):
	if get_entity_type() != Entities.Carrot:
		plant(Entities.Carrot)
	h = can_harvest()
	while not h:
		h = can_harvest()
	harvest()
quick_print("HOME_DONE_TICK", get_tick_count(), "HOME_DONE_TIME", get_time())

move(East)
move(East)
move(East)
move(East)
move(East)
move(North)
move(North)
move(North)
move(North)
move(North)
quick_print("AT_FAR_AGAIN", get_pos_x(), get_pos_y(), "ENTITY", get_entity_type(),
	"GROUND", get_ground_type(), "TICK", get_tick_count(), "TIME", get_time())

quick_print("DONE", "TICK_FINAL", get_tick_count(), "TIME_FINAL", get_time())
