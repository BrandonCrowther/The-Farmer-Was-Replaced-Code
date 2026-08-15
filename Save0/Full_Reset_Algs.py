import Common
import Cactus
import Dinosaurs
import Mazes

def await_harvest():
	c = can_harvest()
	if get_entity_type() == None:
		return False
	while not c:
		c = can_harvest()
		if get_entity_type() == None or get_entity_type() == Entities.Dead_Pumpkin:
			return False

def collect_ingredients(entity):
	cost = get_cost(entity)
	for k in cost:
		v = cost[k] * get_world_size() * get_world_size()
		current_count = num_items(k)
		while num_items(k) < current_count + v:
			get_algorithm(k)()

# Simple algorithm to 
def base_algorithm(entity):
	back_to_start = False
	while not back_to_start:
		await_harvest()
		harvest()
		Common.get_planting_instructions(entity)()
		move(North)
		if get_pos_y() == 0:
			move(East)
		if get_pos_x() + get_pos_y() == 0:
			back_to_start = True

def handle_grass():
	entity = Entities.Grass
	base_algorithm(entity)

def handle_wood():
	entity = Entities.Bush
	base_algorithm(entity)
	
def handle_carrots():
	entity = Entities.Carrot
	collect_ingredients(entity)
	base_algorithm(entity)
	
def handle_pumpkin(infect = False):
	can_use_fertilizer = num_unlocked(Items.Fertilizer) > 0
	entity = Entities.Pumpkin
	collect_ingredients(entity)
	ins = Common.get_planting_instructions(entity)
	
	for x in range(get_world_size()):
		for y in range(get_world_size()):
			Common.move_to(x, y)
			harvest()
			ins()
			if infect:
				if(num_items(Items.Fertilizer) > 0):
					use_item(Items.Fertilizer)

	for x in range(get_world_size()):
		for y in range(get_world_size()):
			Common.move_to(x, y)
			while not can_harvest():
				if get_entity_type() == Entities.Dead_Pumpkin:
					ins()
				if(num_items(Items.Fertilizer) > 0):
					use_item(Items.Fertilizer)
					if not infect and num_items(Items.Weird_Substance) >= 2:
						use_item(Items.Weird_Substance)
						use_item(Items.Weird_Substance)
				else:
					await_harvest()
	harvest()
	move(North)
	move(East)
	
def handle_weird():
	handle_pumpkin(True)

def handle_cactus():
	entity = Entities.Cactus
	collect_ingredients(entity)
	ins = Common.get_planting_instructions(entity)
	for x in range(get_world_size()):
		Common.move_to(x, 0)
		arr = Cactus.prep_field(entity, North, ins)
		sorted = Cactus.sort_asc(arr)
		Cactus.perform_sort(arr, North)
	for y in range(get_world_size()):
		Common.move_to(0, y)
		arr = Cactus.prep_field(entity, East, ins)
		sorted = Cactus.sort_asc(arr)
		Cactus.perform_sort(arr, East)
	await_harvest()
	harvest()
	
def handle_bones():
	collect_ingredients(Entities.Apple)
	Dinosaurs.cycle()
	change_hat(Hats.Brown_Hat)
	
def handle_maze():
	substance_cost = get_world_size() * 2**(num_unlocked(Unlocks.Mazes) - 1)
	while num_items(Items.Weird_Substance) < substance_cost:
		handle_weird()
	if get_entity_type() != Entities.Hedge:
		Mazes.initialize_maze(get_world_size(), 0, 0)
	result = Mazes.start_solving()
	if result:
		Mazes.harvest_treasure(get_world_size())

def get_algorithm(item):
	table = {
		Items.Hay: handle_grass,
		Items.Wood: handle_wood,
		Items.Carrot: handle_carrots,
		Items.Pumpkin: handle_pumpkin,
		Items.Cactus: handle_cactus,
		Items.Weird_Substance: handle_weird,
		Items.Gold: handle_maze,
		Items.Bone: handle_bones
	}
	return table[item]

