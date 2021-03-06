from budget_functions import *
import operator

def create_optimized_party_choices(allotted_budget, preferences_file, final_file_name, food_file, drinks_file):
	satisfied, unsatisfied = 1, 0

	optimized_data = {}

	filename = final_file_name
	file = open(filename, "w+")

	# Set budget
	budget = allotted_budget

	# Extract Food Cost List and Dictionary
	food_cost_list = get_item_costs(food_file)
	food_cost_dict = get_item_costs(food_file, type = 'Dict')
	optimized_data['Food Cost List'] = food_cost_list
	optimized_data['Food Cost Dict'] = food_cost_dict

	# Extract Drink Cost List and Dictionary
	drink_cost_list = get_item_costs(drinks_file)
	drink_cost_dict = get_item_costs(drinks_file, type = 'Dict')
	optimized_data['Drink Cost List'] = drink_cost_list
	optimized_data['Drink Cost Dict'] = drink_cost_dict

	# Create Cost Database
	cost_data = (food_cost_list, drink_cost_list)
	    
	# Create Inventory
	inventory = [[x[0] for x in food_cost_list], [x[0] for x in drink_cost_list]]

	# Extract Preferences
	preferences = get_preferences(preferences_file)
	num_people = len(preferences)

	# Determine lowest costing food-drink combo that stays under budget
	global_lcc = ()

	foods = food_cost_list
	drinks = drink_cost_list

	# Sort all food and drinks available by their unit cost in increasing order
	foods.sort(key=operator.itemgetter(1))

	drinks.sort(key=operator.itemgetter(1))

	# Determine the global LCC (choosing cheapest food and cheapest drink item)
	global_lcc = (foods[0][0], drinks[0][0], foods[0][1] + drinks[0][1])

	# Determine lowest costing preferred food-drink combo for each individual
	indiv_lccs = []

	for person in preferences:
		indiv_lcc = ("","",float("inf"))

		# Extract all preferred food and drink items for an individual
		indiv_foods = [f for f in food_cost_list if f[0] in person[2]]
		indiv_drinks = [d for d in drink_cost_list if d[0] in person[1]]
		
		# Sort all preferred food and drink items for the individual by their unit cost in increasing order
		indiv_foods.sort(key = operator.itemgetter(1))
		indiv_drinks.sort(key = operator.itemgetter(1))

		# Create individual LCC
		indiv_lcc = (person[0], indiv_foods[0][0], indiv_drinks[0][0], indiv_foods[0][1] + indiv_drinks[0][1])
		indiv_lccs.append(indiv_lcc)

	# Determine minimum budget needed to provide all attendees with their lowest costing preferred food and drink
	# combination
	min_budget = sum(x[3] for x in indiv_lccs)

	optimized_data['Min Budget'] = min_budget

	optimized_data['Budget'] = budget

	# If the budget is less than the minimum amount of money needed to give all attendees the overall cheapest
	# food and drink combination
	if budget < (global_lcc[2] * num_people):
		print "---------------------Solution Summary---------------------"
		print "Not Solvable."
		file.write("---------------------Solution Summary---------------------\n")
		file.write("Given your budget, this party cannot be planned.\n")
		file.write("Minimum budget of $" + str(global_lcc[2]*num_people) + " is required to accommodate all attendees with the cheapest food/drink combination available.\n")
		file.write("Minimum budget of $" + str(min_budget) + " is required to accommodate all attendees with their cheapest preferred food/drink combination.")
		file.close()

		return optimized_data

	# Final food-drink combo list
	final_fdc = []

	# Sort individual LCCs based on the cost of the combo in increasing order 
	indiv_lccs.sort(key = operator.itemgetter(3))

	# Remaining budget after assigning everyone global LCC (leftover money if all individuals were
	# given lowest costing combo)
	rem_budget = budget - (num_people * global_lcc[2])

	for i in range(num_people):
		afford = rem_budget + global_lcc[2]
		
		# Can afford their choice
		if round(indiv_lccs[i][3], 2) <= round(afford, 2):
			final_fdc.append((indiv_lccs[i][0], indiv_lccs[i][1], indiv_lccs[i][2], indiv_lccs[i][3], satisfied))
			rem_budget = rem_budget - (indiv_lccs[i][3] - global_lcc[2])
		# Can't afford their choice, so give them the global LCC 
		else:
			final_fdc.append((indiv_lccs[i][0], global_lcc[0], global_lcc[1], global_lcc[2], unsatisfied))

	# Produce shopping list for party

	final_food_choices = {}
	final_drink_choices = {}

	# Determine counts of food and drinks needed for the party
	for c in final_fdc:
		food = c[1]
		drink = c[2]
		# Add food choice and update count of food choice
		if food in final_food_choices.keys():
			final_food_choices[food] = final_food_choices[food] + 1
		else:
			final_food_choices[food] = 1

		# Add drink choice and update count of drink choice
		if drink in final_drink_choices.keys():
			final_drink_choices[drink] = final_drink_choices[drink] + 1
		else:
			final_drink_choices[drink] = 1


	# Print all data and information
	print "\t\tPARTY AND GUEST LOGISTICS\n"
	file.write("\t\t\t\t\tPARTY AND GUEST LOGISTICS\n\n")

	# file.write("Given your budget, this party cannot accommodate all attendees with their cheapest preferred food/drink combination.\n")
	file.write("Minimum budget of $" + str(min_budget) + " is required to accommodate all attendees with their cheapest preferred food/drink combination.\n")


	print "---------------------Solution Summary---------------------"
	file.write("---------------------Solution Summary---------------------")
	print "Budget: $" + str(budget)
	file.write("\nBudget: $" + str(budget))


	print "Total Spent: $" + str(budget - rem_budget)
	file.write("\nTotal Spent: $" + str(budget - rem_budget))

	optimized_data['Total Spent'] = (budget - rem_budget)

	if str(budget) == str(budget - rem_budget):
		print "Total Money Left: $" + str(int(rem_budget))
		file.write("\nTotal Money Left: $" + str(int(rem_budget)))
		optimized_data['Total Money Left'] = int(rem_budget)
	else:
		print "Total Money Left: $" + str(rem_budget)
		file.write("\nTotal Money Left: $" + str(rem_budget))
		optimized_data['Total Money Left'] = rem_budget

	# Total number of satisfied individuals
	total_satisfied_individuals = [x[4] for x in final_fdc].count(1)

	optimized_data['Total Preferences Met'] = total_satisfied_individuals
	optimized_data['Number of Attendees'] = num_people

	print "Total Preferences Met: " + str(total_satisfied_individuals) + " of " + str(num_people)
	file.write("\nTotal Preferences Met: "+ str(total_satisfied_individuals) + " of " + str(num_people))

	print("---------------------Food Information---------------------")
	file.write("\n\n---------------------Food Information---------------------\n")
	print "Food Needed: " 
	file.write("Food Needed: \n")
	total_food_cost = 0.0

	for food in final_food_choices:
		total_item_cost = final_food_choices[food] * food_cost_dict[food]
		total_food_cost = total_food_cost + total_item_cost
		s = str(final_food_choices[food]) + "x " + str(food) + " ($" + str(food_cost_dict[food]) + "/ea)"
		print s
		file.write(s + "\n")

	print "Total Food Cost: $" + str(total_food_cost)
	file.write("Total Food Cost: $" + str(total_food_cost))

	optimized_data['Final Food Choices'] = final_food_choices
	optimized_data['Total Food Cost'] = total_food_cost

	print("\n---------------------Drink Information--------------------")
	file.write("\n\n---------------------Drink Information--------------------\n")
	print "Drinks Needed: "
	file.write("Drinks Needed: \n")
	total_drinks_cost = 0.0
	for drink in final_drink_choices:
		total_item_cost = final_drink_choices[drink] * drink_cost_dict[drink]
		total_drinks_cost = total_drinks_cost + total_item_cost
		s = str(final_drink_choices[drink]) + "x " + str(drink) + " ($" + str(drink_cost_dict[drink]) + "/ea)"
		print s
		file.write(s + "\n")

	print "Total Drink Cost: $" + str(total_drinks_cost)
	file.write("Total Drink Cost: $" + str(total_drinks_cost))

	optimized_data['Final Drink Choices'] = final_drink_choices
	optimized_data['Total Drink Cost'] = total_drinks_cost

	print "\n---------------Final Food/Drink Assignments---------------"
	file.write("\n\n---------------Final Food/Drink Assignments---------------\n")

	# Sort attendees alphabetically (for standardized visualization purposes)
	final_fdc.sort()

	optimized_data['Final Food Drink Combinations'] = final_fdc	

	# Print all attendees and the food and drink combo they were provided
	for info in final_fdc:
		# If the individual was satisfied with their LCC
		if info[4] == 0:
			s = info[0] + "*: " + info[1] + " and " + info[2] + " ($" + str(info[3]) + ")"
		# If they were not satisfied (i.e. They were given the Global LCC)
		else:
			s = info[0] + ": " + info[1] + " and " + info[2] + " ($" + str(info[3]) + ")"
		file.write(s + "\n")
		print s
	print "\n* - Preferences not met"
	file.write("\n* - Preferences not met\n")
	file.close()

	return optimized_data

# This commented out portion runs the optimizer on a simple set of preferences, food, and drinks.
# It will write to a file called "simple_optimization.txt" for you to see the results of the 
# optimization on a small set of data.
# create_optimized_party_choices((6.5+6.8+12.3+17.0), 'Initial Test/people.txt', 'simple_optimization.txt', food_file = 'Initial Test/food.txt', drinks_file = 'Initial Test/drinks.txt')