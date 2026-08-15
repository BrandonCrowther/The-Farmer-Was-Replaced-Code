import Full_Reset_Algs

def can_farm(entity):
	table = {
		Items.Hay: num_unlocked(Unlocks.Grass), 
		Items.Wood: num_unlocked(Unlocks.Plant),
		Items.Carrot: num_unlocked(Unlocks.Carrots),
		Items.Cactus: num_unlocked(Unlocks.Cactus),
		Items.Pumpkin: num_unlocked(Unlocks.Pumpkins),
		Items.Power: num_unlocked(Unlocks.Sunflowers),
		Items.Bone: num_unlocked(Unlocks.Dinosaurs),
		Items.Weird_Substance: num_unlocked(Unlocks.Fertilizer),
		Items.Gold: num_unlocked(Unlocks.Mazes)
	}
	return table[entity] > 0

def is_valid_goal(costs):
	if len(costs) == 0:
		return False
	for k in costs:
		v = costs[k]
		if not can_farm(k):
			return False
	return True


unlocks = [
	Unlocks.Grass,
	Unlocks.Speed,
	Unlocks.Hats,
	Unlocks.Plant,
	Unlocks.Expand,
	Unlocks.Carrots,
	Unlocks.Watering,
	Unlocks.Fertilizer,
	Unlocks.Mazes,
	Unlocks.Trees,
	Unlocks.Pumpkins,
	Unlocks.Cactus,
	Unlocks.Dinosaurs,
	Unlocks.Leaderboard,
	Unlocks.Polyculture
]

def choose_unlock():
	choices = {}
	for u in unlocks:
		costs = get_cost(u)
		if is_valid_goal(costs):
			choices[u] = costs
	
	best_choice = None
	current_lowest = None

	for choice in choices:
		costs = choices[choice]
		total_cost = 0
		for type in costs:
			num = costs[type]
			total_cost += num
		
		if current_lowest == None or total_cost < current_lowest:
			best_choice = choice
			current_lowest = total_cost

	return best_choice

goal_unlock = None
goal_resources = {}
while num_unlocked(Unlocks.Leaderboard) == 0:
	if goal_unlock == None:
		goal_unlock = choose_unlock()
		goal_resources = get_cost(goal_unlock)
		
	for r in goal_resources:
		amount = goal_resources[r]
		while num_items(r) < amount:
			Full_Reset_Algs.get_algorithm(r)()

	unlock(goal_unlock)
	goal_unlock = None
	