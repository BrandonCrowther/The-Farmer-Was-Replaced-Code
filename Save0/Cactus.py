import Common

def sort(stack, comparator):
	for index in range(len(stack)):
		lowest_index = index
		for c in range(index + 1, len(stack)):
			if comparator(stack[c], stack[lowest_index]):
				lowest_index = c
		tmp = stack[index]
		stack[index] = stack[lowest_index]
		stack[lowest_index] = tmp
	return stack

def sort_asc(stack):
	def comparator(a, b):
		return a < b
	return sort(stack, comparator)
	
def sort_desc(stack):
	def comparator(a, b):
		return a > b
	return sort(stack, comparator)

def prep_field(entity, dir, instructions):
	sizes = []
	for i in range(get_world_size()):
		instructions()
		plant(entity)
		sizes.append(measure())
		move(dir)
	return sizes
	

def move_item(x, y):
	while get_pos_x() < x:
		swap(East)
		move(East)
	while get_pos_x() > x:
		swap(West)
		move(West)
	while get_pos_y() < y:
		swap(North)
		move(North)
	while get_pos_y() > y:
		swap(South)
		move(South)
	
def perform_sort(array, dir):
	for i in range(len(array)):
		target_number = array[i]
		m = measure()
		while m != target_number:
			move(dir)
			m = measure()
		if dir == North or dir == South:
			x = get_pos_x()
			move_item(x, i)
			if i + 1 < get_world_size():
				Common.move_to(x, i + 1)
		else:
			y = get_pos_y()
			move_item(i, y)
			if i + 1 < get_world_size():
				Common.move_to(i + 1, y)