from party_optimizer import *

for i in range(5):
	create_optimized_party_choices(800, 'Testing/Test Case Preferences/people' + str(i) + '.txt', 'Testing/Test Case Outputs/optimized_party_' + str(i) + '.txt', food_file = 'Testing/food.txt', drinks_file = 'Testing/drinks.txt')
