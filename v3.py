from budget_functions import *
import operator

# Set budget
budget = 50.0

# Extract Food Cost List and Dictionary
food_cost_list = get_item_costs('food.txt')
food_cost_dict = get_item_costs('food.txt', type = 'Dict')

# Extract Drink Cost List
drink_cost_list = get_item_costs('drinks.txt')
drink_cost_dict = get_item_costs('drinks.txt', type = 'Dict')

# Create Cost Database
cost_data = (food_cost_list, drink_cost_list)
    
# Create Inventory
inventory = [[x[0] for x in food_cost_list], [x[0] for x in drink_cost_list]]
#print inventory

# Extract Preferences
preferences = get_preferences('people.txt')
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

#print "Global LCC: " + str(global_lcc)

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
	print "Not Solvable."

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
	
	if unsatisfied_individuals != 0:
		# Update ppb for remaining budget and number of unsatisfied people
		ppb = float(rem_budget) / satisfaction_vector.count(0)
	
	else:
		# No more individuals to satisfy
		break

# Choose lowest costing food-drink combo for all unsatisfied individuals

# Number of unsatisfied individuals remaining
unsatisfied_individuals = satisfaction_vector.count(0)

# For all unsatisfied individuals remaining
for i in range(unsatisfied_individuals):
	# Add Global LCC to final list
	final_fdc.append(global_lcc)

	# Subtract cost of Global LCC from total budget
	rem_budget = rem_budget - global_lcc[2]

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

print "PARTY AND GUEST INFORMATION AND LOGISTICS"

print "\nInitial Budget: $" + str(budget)
print "Total Optimized Spendings: $" + str(budget - rem_budget)
print "Total Money Saved: $" + str(rem_budget)


print "\nFinal Food/Drink Assignments for All Party Attendees: \n"
for info in final_fdc:
	s = info[0] + ": " + info[1] + " and " + info[2] 
	print s

print "\nFood Needed: " 
total_food_cost = 0.0
for food in final_food_choices:
	total_item_cost = final_food_choices[food] * food_cost_dict[food]
	total_food_cost = total_food_cost + total_item_cost
	s = str(final_food_choices[food]) + "x " + str(food) + " ($" + str(total_item_cost) + ")"
	print s

print "\nTotal Food Cost: $" + str(total_food_cost)

print "\nDrinks Needed: "
total_drinks_cost = 0.0
for drink in final_drink_choices:
	total_item_cost = final_drink_choices[drink] * drink_cost_dict[drink]
	total_drinks_cost = total_drinks_cost + total_item_cost
	s = str(final_drink_choices[drink]) + "x " + str(drink) + " ($" + str(total_item_cost) + ")"
	print s

print "\nTotal Drink Cost: $" + str(total_drinks_cost)