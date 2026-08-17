# exp-cactus_single-002 -- resources, unlocks, cascade-yield scaling
#
# Follow-up to 001: check Pumpkin stock and the Cactus unlock level
# (001's single harvest yielded 32, not the literal n**2=1 for a lone
# cactus -- some multiplier must be in play), then force a real 2-cactus
# cascade (using swap() to fix sort order, since 001 found size is fixed
# once fully grown, not something that converges by waiting) and read
# the actual yield to back out the formula.
#
# Not chasing the target -- terminates quickly. Expect "Run Failed".

quick_print("START", "PUMPKIN", num_items(Items.Pumpkin), "CACTUS_UNLOCK",
	num_unlocked(Unlocks.Cactus), "COST_CACTUS", get_cost(Entities.Cactus))

AX, AY = get_pos_x(), get_pos_y()
if get_ground_type() != Grounds.Soil:
	till()
plant(Entities.Cactus)

move(East)
BX, BY = get_pos_x(), get_pos_y()
if get_ground_type() != Grounds.Soil:
	till()
plant(Entities.Cactus)

# Wait for both to be fully grown (drone is on B right now).
h = can_harvest()
while not h:
	h = can_harvest()
size_b = measure()

move(West)
h = can_harvest()
while not h:
	h = can_harvest()
size_a = measure()

quick_print("SIZES", "A", size_a, "B", size_b)

# Sorted order for this pair (A west of B) requires size(A) <= size(B)
# -- B is A's East neighbor and must be >= A; A is B's West neighbor and
# must be <= B, the same inequality either way.
move(East)
if size_a > size_b:
	swap(West)
	size_b = measure()
	move(West)
	size_a = measure()
	move(East)
	quick_print("SWAPPED", "A_NOW", size_a, "B_NOW", size_b)

move(West)
before = num_items(Items.Cactus)
harvest()
gained = num_items(Items.Cactus) - before
quick_print("CASCADE_HARVEST", "GAINED", gained, "SIZE_A", size_a, "SIZE_B", size_b)
