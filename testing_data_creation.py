import names
import numpy as np
name_list = [names.get_full_name().encode("utf-8") for x in range(100)]

food_list = ["Chicken Pesto", "Chicken Parmesan", "Beef Stew", "Fettucini Alfredo", 
			 "Fried Chicken", "Lasagna", "Vegetable Lasagna", "Pizza", "Breadstick",
			 "Black Bean Burger", "BLT", "Spaghetti", "Grilled Cheese", "Gyro", "Thai Curry"]
food_cost_list = [4.5, 10.3, 40.0, 10.0, 15.6, 17.4, 10.0, 6.9, 3.4, 17.8,
				  8.7, 4.5, 9.7, 19.5, 14.0]

drink_list = ["Coke", "Sprite", "Dr. Pepper", "Pepsi", "Water", "Orange Juice",
			  "Apple Juice", "Tea", "Sweetened Ice Tea", "Lemonade"]
drink_cost_list = [3.4, 2.3, 4.7, 3.2, 3.5, 1.0, 4.9, 6.3, 1.1, 9.0]


for j in range(5):
	file = open("people" + str(j) + ".txt", "w+")

	for i in range(100):
		file.write(str(name_list[i]) + "\n")

		drink_choices = np.random.choice(drink_list, 2, replace = False)
		s = ''
		for drink in drink_choices:
			s = s + str(drink) + ","
		
		file.write(s[:len(s)-1] + "\n")

		food_choices = np.random.choice(food_list, 3, replace = False)
		s = ''
		for food in food_choices:
			s = s + str(food) + ","

		file.write(s[:len(s)-1] + "\n")

	file.close()

# file = open("food.txt", "w+")
# for i in range(15):
# 	file.write(str(food_list[i]) + ":" + str(food_cost_list[i]) + "\n")

# file.close()

# file = open("drinks.txt", "w+")
# for i in range(10):
# 	file.write(str(drink_list[i]) + ":" + str(drink_cost_list[i]) + "\n")
# file.close()
