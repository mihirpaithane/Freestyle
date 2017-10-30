from party_optimizer import *


#create_optimized_party_choices(30.0, 'Initial Test/people.txt', 'Initial Test/optimized_party_choices.txt', food_file = 'Initial Test/food.txt', drinks_file = 'Initial Test/drinks.txt')


budget = 800.0

for i in range(5):
	create_optimized_party_choices(budget, 'Testing/Test Case Preferences/people' + str(i) + '.txt', 'Testing/Test Case Outputs/optimized_party_' + str(i) + "_" + str(budget) + '_.txt', food_file = 'Testing/food.txt', drinks_file = 'Testing/drinks.txt')
