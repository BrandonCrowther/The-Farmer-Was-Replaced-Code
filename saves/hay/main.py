quick_print("MAX_DRONES", max_drones(), "MEGAFARM_LEVEL", num_unlocked(Unlocks.Megafarm),
	"MEGAFARM_COST", get_cost(Unlocks.Megafarm))
quick_print("POLYCULTURE_LEVEL", num_unlocked(Unlocks.Polyculture), "POLYCULTURE_COST",
	get_cost(Unlocks.Polyculture))
quick_print("WATERING_LEVEL", num_unlocked(Unlocks.Watering), "WATERING_COST",
	get_cost(Unlocks.Watering))
quick_print("HAY", num_items(Items.Hay), "WOOD", num_items(Items.Wood), "CARROT", num_items(Items.Carrot))
r = unlock(Unlocks.Megafarm)
quick_print("UNLOCK_ATTEMPT_RESULT", r, "NEW_MAX_DRONES", max_drones(), "NEW_MEGAFARM_LEVEL",
	num_unlocked(Unlocks.Megafarm))
