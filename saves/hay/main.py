quick_print("SPEED_BEFORE", num_unlocked(Unlocks.Speed))
r = unlock(Unlocks.Speed)
quick_print("UNLOCK_SPEED_RESULT", r, "SPEED_AFTER", num_unlocked(Unlocks.Speed))

quick_print("FERT_BEFORE", num_unlocked(Unlocks.Fertilizer))
r2 = unlock(Unlocks.Fertilizer)
quick_print("UNLOCK_FERT_RESULT", r2, "FERT_AFTER", num_unlocked(Unlocks.Fertilizer))
