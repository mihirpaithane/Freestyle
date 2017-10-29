from pulp import *
from budget_functions import *

# Set budget
budget = 50.0

# Extract Food Cost Dictionary
food_cost_dict = get_item_costs('food.txt')

# Extract Drink Cost Dictionary
drink_cost_dict = get_item_costs('drinks.txt')

# Create Cost Database
cost_data = (food_cost_dict, drink_cost_dict)
    
# Create Inventory
inventory_data = [cost_data[0].keys(), cost_data[1].keys()]

# Extract Preferences
preferences = get_preferences('people.txt')

# Create food and drink combos
food_drink_combos = []
for food in food_cost_dict.keys():
	for drink in drink_cost_dict.keys():
		fd_combo = (food, drink, food_cost_dict[food] + drink_cost_dict[drink], get_preference_score(food, preferences) + get_preference_score(drink, preferences))
		food_drink_combos.append(fd_combo)

#print food_drink_combos

# Data input
choices = [x[0] + " + " + x[1] for x in food_drink_combos]
#print choices

price = [x[2] for x in food_drink_combos]
#print price

preference = [x[3] for x in food_drink_combos]
#print preference

C = range(len(choices))

# Declare problem instance, maximization problem
prob = LpProblem("Portfolio", LpMaximize)

# Declare decision variable x, 1 if food-drink combo is included and 0 else
x = LpVariable.matrix("x", list(C), 0, 1, LpInteger)

# Objective function -> Maximize preferences
prob += sum(preference[c] * x[c] for c in C)

# Constraint definition
prob += sum(price[c] * x[c] for c in C) <= budget

# Solve
prob.solve()

# Extract solution
portfolio = [(choices[c], price[c], preference[c]) for c in C if x[c].varValue]

print(portfolio)