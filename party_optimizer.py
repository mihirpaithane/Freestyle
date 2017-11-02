from budget_functions import *
import operator

def create_optimized_party_choices(allotted_budget, preferences_file, final_file_name, food_file = 'food.txt', drinks_file = 'drinks.txt'):
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

	# Extract Drink Cost List
	drink_cost_list = get_item_costs(drinks_file)
	drink_cost_dict = get_item_costs(drinks_file, type = 'Dict')
	optimized_data['Drink Cost List'] = drink_cost_list
	optimized_data['Drink Cost Dict'] = drink_cost_dict


	# Create Cost Database
	cost_data = (food_cost_list, drink_cost_list)
	    
	# Create Inventory
	inventory = [[x[0] for x in food_cost_list], [x[0] for x in drink_cost_list]]
	#print inventory

	# Extract Preferences
	preferences = get_preferences(preferences_file)
	num_people = len(preferences)

	# Determine lowest costing food-drink combo that stays under budget
	global_lcc = ()

	foods = food_cost_list
	drinks = drink_cost_list

	foods.sort(key=operator.itemgetter(1))
	#print foods

	drinks.sort(key=operator.itemgetter(1))
	#print drinks

	####### SORT ASCENDING FOR FOOD AND DRINK, LCC = FIRST OF FOOD + FIRST OF DRINK ####### 
	global_lcc = (foods[0][0], drinks[0][0], foods[0][1] + drinks[0][1])

	# print "Global LCC: " + str(global_lcc)

	# Determine lowest costing preferred food-drink combo for each individual
	indiv_lccs = []

	for person in preferences:
		#print person[0]
		indiv_lcc = ("","",float("inf"))

		indiv_foods = [f for f in food_cost_list if f[0] in person[2]]
		indiv_drinks = [d for d in drink_cost_list if d[0] in person[1]]
		indiv_foods.sort(key = operator.itemgetter(1))
		indiv_drinks.sort(key = operator.itemgetter(1))

		indiv_lcc = (person[0], indiv_foods[0][0], indiv_drinks[0][0], indiv_foods[0][1] + indiv_drinks[0][1])
		indiv_lccs.append(indiv_lcc)

	#print "\nIndividual LCCs: " + str(indiv_lccs)

	# Determine Per Person Budget (PPB)
	ppb = budget / num_people
	#print "\nPer Person (Initial) Budget: " + str(ppb)

	# BREAK PROGRAM #
	if ppb < global_lcc[2]:
		print "---------------------Solution Summary---------------------"
		print "Not Solvable."
		file.write("---------------------Solution Summary---------------------\n")
		file.write("Given your budget, this party cannot be planned.\n")
		file.write("Minimum budget of $" + str(global_lcc[2]*num_people) + " is required to accommodate all attendees with the cheapest food/drink combination available.\n")
		min_budget = sum(x[3] for x in indiv_lccs)
		file.write("Minimum budget of $" + str(min_budget) + " is required to accommodate all attendees with their cheapest preferred food/drink combination.")
		file.close()

		
		return

	# Variable to denote if any change of satisfaction occurs (boolean)
	change = True

	# Satisfaction vector (used to denote if an individual is satisfied or not)
	# 0 = not satisfied
	# 1 = satisfied
	satisfaction_vector = [0 for x in range(num_people)]

	# Final food-drink combo list
	final_fdc = []

	# Remaining budget
	rem_budget = budget

	# Loop through individuals, changing their satisfaction
	while change:
		# Set change to false
		change = False

		# Update ppb for remaining budget and number of unsatisfied people
		ppb = float(rem_budget) / satisfaction_vector.count(0)

		# For each individual attending the party
		for indiv in range(num_people):
			# If:
			#  (1) The individual has not been satisfied
			#  (2) Individuals Lowest Costing Preferred Combo is less than the alloted budget per person 
			if (satisfaction_vector[indiv] == 0) and (indiv_lccs[indiv][3] <= ppb):
				#print "SATISFIED!"

				# Add individuals LCC to final list
				final_fdc.append(indiv_lccs[indiv])

				# Reduce remaining budget
				rem_budget = rem_budget - indiv_lccs[indiv][3]

				# Individual has now been satisfied
				satisfaction_vector[indiv] = 1

				# A change in satisfaction has occurred
				change = True

				#print satisfaction_vector

		# Number of unsatisfied individuals remaining
		unsatisfied_individuals = satisfaction_vector.count(0)
		
		if unsatisfied_individuals == 0:
			# No more individuals to satisfy
			break

	# Choose lowest costing food-drink combo for all unsatisfied individuals

	# For all unsatisfied individuals remaining
	for indiv in range(num_people):
		if satisfaction_vector[indiv] == 0:
			# Add Global LCC to final list
			final_fdc.append((indiv_lccs[indiv][0], global_lcc[0], global_lcc[1], global_lcc[2]))

			# Subtract cost of Global LCC from total budget
			rem_budget = rem_budget - global_lcc[2]

	# With remaining budget, determine if any more preferences can be met	
	
	flagged_indiv_lccs = []
	count = 0
	for indiv in indiv_lccs:
		flagged_indiv_lccs.append((indiv[0], indiv[1], indiv[2], indiv[3], satisfaction_vector[count]))
		count = count + 1

	flagged_indiv_lccs.sort(key = operator.itemgetter(3))
	total_satisfied_individuals = [x[4] for x in flagged_indiv_lccs].count(1)
	final_satisfactions = {}

	for indiv in flagged_indiv_lccs:

		# If they haven't been satisfied
		if indiv[4] == 0:
			print indiv
			# print "Unsatisfied:("
			# Get location of unsatisfied individual in final fdc
			index = [x[0] for x in final_fdc].index(indiv[0])
			# print "Cost to change: " + str(indiv[3] - final_fdc[index][3])
			# print "Resulting rem_budget before change: " + str(rem_budget)

			# If changing stays within budget
			if rem_budget - (indiv[3] - final_fdc[index][3]) >= 0:
				
				# print "Changed To Preferred!"
				diff = indiv[3] - final_fdc[index][3]

				# Change their food/drink combo
				final_fdc[index] = (indiv[0], indiv[1], indiv[2], indiv[3])
				# print final_fdc[index]

				# Decrement remaining budget based on adding the new preferred combination
				rem_budget = rem_budget - diff

				total_satisfied_individuals = total_satisfied_individuals + 1
				final_satisfactions[indiv[0]] = 1
			else:
				final_satisfactions[indiv[0]] = 0
		else:
			final_satisfactions[indiv[0]] = 1


			
			# print "Remaining Budget after change: " + str(rem_budget)

	# Produce shopping list for party

	final_food_choices = {}
	final_drink_choices = {}

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

	print "\t\tPARTY AND GUEST LOGISTICS\n"
	file.write("\t\tPARTY AND GUEST LOGISTICS\n\n")

	min_budget = sum(x[3] for x in indiv_lccs)
	file.write("Given your budget, this party cannot accommodate all attendees with their cheapest preferred food/drink combination.\n")
	file.write("Minimum budget of $" + str(min_budget) + " is required to accommodate all attendees with their cheapest preferred food/drink combination.\n")
		
	# 0 - Min Budget
	optimized_data['Min Budget'] = min_budget


	print "---------------------Solution Summary---------------------"
	file.write("---------------------Solution Summary---------------------")
	print "Budget: $" + str(budget)
	file.write("\nBudget: $" + str(budget))

	# 1 - Budget
	optimized_data['Budget'] = budget

	print "Total Spent: $" + str(budget - rem_budget)
	file.write("\nTotal Spent: $" + str(budget - rem_budget))

	# 2 - Total Spent
	optimized_data['Total Spent'] = (budget - rem_budget)

	# 3 - Total Money Left
	if str(budget) == str(budget - rem_budget):
		print "Total Money Left: $" + str(int(rem_budget))
		file.write("\nTotal Money Left: $" + str(int(rem_budget)))
		optimized_data['Total Money Left'] = int(rem_budget)
	else:
		print "Total Money Saved: $" + str(rem_budget)
		file.write("\nTotal Money Saved: $" + str(rem_budget))
		optimized_data['Total Money Left'] = rem_budget

	# 4 - Total Preferences Met
	optimized_data['Total Preferences Met'] = total_satisfied_individuals
	# 5 - Total Number of People
	optimized_data['Number of Attendees'] = num_people

	print "Total Preferences Met: " + str(total_satisfied_individuals) + " of " + str(len(satisfaction_vector))
	file.write("\nTotal Preferences Met: "+ str(total_satisfied_individuals) + " of " + str(len(satisfaction_vector)))

	print("---------------------Food Information---------------------")
	file.write("\n\n---------------------Food Information---------------------\n")
	print "Food Needed: " 
	file.write("Food Needed: \n")
	total_food_cost = 0.0

	##### FIGURE THIS OUT ######

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


	final_fdc.sort()
	optimized_data['Final Food Drink Combinations'] = final_fdc
	optimized_data['Final Satisfactions'] = final_satisfactions
	count = 0
	for info in final_fdc:
		if final_satisfactions[info[0]] == 0:
			s = info[0] + "*: " + info[1] + " and " + info[2] + " ($" + str(info[3]) + ")"
		else:
			s = info[0] + ": " + info[1] + " and " + info[2] + " ($" + str(info[3]) + ")"

		# if satisfaction_vector[count] == 0:
		# 	s = info[0] + "*: " + info[1] + " and " + info[2]
		# else:
		# 	s = info[0] + ": " + info[1] + " and " + info[2] 
		print s
		file.write(s + "\n")
		count = count + 1

	print "\n* - Preferences not met"
	file.write("\n* - Preferences not met\n")
	file.close()

	return optimized_data