def get_item_costs(filename, type = 'List'):
	file = open(filename,'r')
	if type == 'List':
		item_cost_list = []
	else:
		item_cost_dict = {}
	
	for line in file:
		item, cost = line.strip().split(':')
		if type == 'List':
			item_cost_list.append((item, float(cost)))
		else:
			item_cost_dict[item] = float(cost)

	if type == 'List':
		return item_cost_list
	else:
		return item_cost_dict

def get_preferences(filename):
	people = open(filename,'r')
	names, drinks, food = [], [], []

	for count, line in enumerate(people, start=1):
		if (count % 3) == 1:
			names.append(line.strip())
		elif (count % 3) == 2:
			drinks.append(line.strip().split(','))
		elif (count % 3) == 0:
			food.append(line.strip().split(','))

	# Check if zip is efficient
	preferences = map(tuple, zip(names,drinks,food))

	return preferences

def get_preference_score(item, preferences):
	score = 0
	for preference in preferences:
		if item in preference[1]:
			score = score + 1
		if item in preference[2]:
			score = score + 2
	return score


def get_total_cost(foods, drinks, cost_data, preferences):
	food_total_cost = 0.0
	drink_total_cost = 0.0
	
	food_cost_dict = cost_data[0]
	drink_cost_dict = cost_data[1]

	for item in foods: # For each item to buy
		for preference in preferences: # For each person
			for food in preference[2]: # For each food preference
				if item == food: # If the item is in the person's preference
					cost = food_cost_dict[food] # Extract cost
					food_total_cost = food_total_cost + cost # Add to total food cost
			
	for item in drinks: # For each item to buy
		for preference in preferences: # For each person
			for drink in preference[1]: # For each drink preference
				if item == drink: # If the item is in the person's preference
					cost = drink_cost_dict[drink] # Extract cost
					drink_total_cost = drink_total_cost + cost # Add to total drink cost

	total_cost = food_total_cost + drink_total_cost

	# return (food_total_cost, drink_total_cost, total_cost)
	return total_cost