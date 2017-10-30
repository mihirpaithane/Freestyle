from budget_functions import *

# Set budget
budget = 30.0

# Extract Food Cost Dictionary
food_cost_dict = get_item_costs('food.txt')

# Extract Drink Cost Dictionary
drink_cost_dict = get_item_costs('drinks.txt')

# Create Cost Database
cost_data = (food_cost_dict, drink_cost_dict)
    
# Create Inventory
inventory = [cost_data[0].keys(), cost_data[1].keys()]
#print inventory

# Extract Preferences
preferences = get_preferences('people.txt')
num_people = len(preferences)

# Create food and drink combos
food_drink_combos = []
for food in inventory[0]:
	for drink in inventory[1]:
		fd_combo = (food, drink, food_cost_dict[food] + drink_cost_dict[drink])
		food_drink_combos.append(fd_combo)

# Determine lowest costing food-drink combo that stays under budget
lcc = ("","",float("inf"))

# NOTE: SORT ASCENDING FOR FOOD AND DRINK, LCC = FIRST OF FOOD + FIRST OF DRINK

for combo in food_drink_combos:
	total_cost = combo[2]*num_people
	if (total_cost <= budget) and (combo[2] <= lcc[2]):
		lcc = combo

print "Global LCC: " + str(lcc)

# Determine lowest costing preferred food-drink combo for each individual
indiv_lccs = []

for person in preferences:
	#print person[0]
	indiv_lcc = ("","",float("inf"))
	for drink in person[1]:
		for food in person[2]:
			combo_cost = food_cost_dict[food] + drink_cost_dict[drink]
			# ADD NAME
			combo = (person[0], food, drink, combo_cost)
			if combo[3] < indiv_lcc[2]:
				indiv_lcc = combo
	# NOTE: SORT ASCENDING FOR FOOD AND DRINK, LCC = FIRST OF FOOD + FIRST OF DRINK
	
	indiv_lccs.append(indiv_lcc)

print "\nIndividual LCCs: " + str(indiv_lccs)

# Determine Per Person Budget (PPB)
ppb = budget / num_people
print "\nPer Person (Initial) Budget: " + str(ppb)

# BREAK PROGRAM #
if ppb < lcc[2]:
	print "Not Solvable."


# Variable to denote if any change of satisfaction occurs (boolean)
change = True

# Satisfaction vector (used to denote if an individual is satisfied or not)
satisfaction_vector = [0 for x in range(num_people)]

# Final food-drink combo list
final_fdc = []

# Remaining budget
rem_budget = budget

# Loop through individuals, changing their satisfaction
while change:
	# Set change to false
	change = False

	# For each individual attending the party
	for indiv in range(num_people):
		# If:
		#  (1) Individuals Lowest Costing Preferred Combo is less than the alloted budget per person 
		#  (2) The individual has not been satisfied
		if (indiv_lccs[indiv][2] <= ppb) and (satisfaction_vector[indiv] == 0):
			# Add individuals LCC to final list
			final_fdc.append(indiv_lccs[indiv])

			# Subtract cost of LCC from total budget
			rem_budget = rem_budget - indiv_lccs[indiv][2]

			# Individual has now been satisfied
			satisfaction_vector[indiv] = 1

			# A change in satisfaction has occurred
			change = True

			print satisfaction_vector

	unsatisfied_individuals = satisfaction_vector.count(0)
	if unsatisfied_individuals != 0:
		# Update ppb for remaining budget and number of unsatisfied people
		ppb = float(rem_budget) / satisfaction_vector.count(0)

# Choose lowest costing food-drink combo for all unsatisfied individuals

# Number of unsatisfied individuals remaining
unsatisfied_individuals = satisfaction_vector.count(0)

# For all unsatisfied individuals remaining
for i in range(unsatisfied_individuals):
	# Add overall LCC to final list
	final_fdc.append(lcc)

	# Subtract cost of Global LCC from total budget
	rem_budget = rem_budget - lcc[2]

final_food_choices = {}
final_drink_choices = {}

for c in final_fdc:
	food = c[0]
	drink = c[1]
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

print final_food_choices
print final_drink_choices