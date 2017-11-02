from Tkinter import *
import tkFont
from tkFileDialog import askopenfilename
from party_optimizer import *

class App:

    def __init__(self, master):
        bg_color = "#80dfff"
        frame = Frame(master, background = bg_color)
        frame.pack(side="top", fill="both", expand = True)
        frame.place(x= 0, y = 0)

        self.res = ''

        self.msg = Message(master, text="Enter the budget:", width=500, background = bg_color).pack(padx = 5, pady = 2)

        self.budget = Entry(master, highlightbackground = bg_color)
        self.budget.pack(padx = 5, pady = 2)


        # Put these three together
        self.preferences = Button(master, text='Upload Preferences', command=self.getPreferencesFileName, background = "#add8e6", highlightbackground = bg_color).pack(padx = 5, pady = 2)

        self.food = Button(master, text='Upload Food', command=self.getFoodFileName, background = bg_color, highlightbackground = bg_color).pack(padx = 5, pady = 2)

        self.drinks = Button(master, text='Upload Drinks', command=self.getDrinksFileName, background = bg_color, highlightbackground = bg_color).pack(padx = 5, pady = 2)

        # Separate line
        self.optimizer = Button(master, text="Optimize", command=self.optimize, background = bg_color, highlightbackground = bg_color).pack(padx = 5, pady = 2)

        self.result = StringVar(master)

        self.scrollbar = Scrollbar(master)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        f = tkFont.Font(family="Helvetica", size=14)

        self.res = Text(master, wrap = WORD, highlightbackground = '#b3ecff', background = '#b3ecff', state=DISABLED)
        # self.res = Label(master, text = '', wraplength = 500, font = f, background = '#b3ecff', borderwidth=2, relief = 'solid')
        self.res.pack(padx = 5, pady = 2)


    def getPreferencesFileName(self):
        Tk().withdraw() 
        self.preferences_filename = askopenfilename()  

    def getFoodFileName(self):
        Tk().withdraw() 
        self.food_filename = askopenfilename() 

    def getDrinksFileName(self):
        Tk().withdraw() 
        self.drinks_filename = askopenfilename() 

    def optimize(self):
        # self.res.configure(text = 'Optimizing Party Logistics...')
        self.res.config(state=NORMAL)        
        self.res.delete(1.0,END)
        self.res.config(state=DISABLED)
        opt = create_optimized_party_choices(float(self.budget.get()), preferences_file = self.preferences_filename, final_file_name = "bleh.txt", food_file = self.food_filename, drinks_file = self.drinks_filename)

        opt_text = ''
        
        opt_text = opt_text + 'PARTY AND GUEST LOGISTICS\n\n'
        opt_text = opt_text + 'Minimum budget of $' + str(opt['Min Budget']) + ' is required to accommodate all attendees with their cheapest preferred food/drink combination.\n'
            
        opt_text = opt_text + '\n---------------------Solution Summary---------------------\n'
        opt_text = opt_text + 'Budget: $' + str(opt['Budget'])
        
        if len(opt.keys()) == 6:
            opt_text = opt_text + "\nGiven your budget, this party cannot be planned."
        else:

            opt_text = opt_text + '\nTotal Spent: $' + str(opt['Total Spent'])
            opt_text = opt_text + '\nTotal Money Left: $' + str(opt['Total Money Left'])
            opt_text = opt_text + '\nTotal Preferences Met: ' + str(opt['Total Preferences Met']) + ' out of ' + str(opt['Number of Attendees'])
            opt_text = opt_text + '\n\n---------------------FOOD INFORMATION---------------------'
            opt_text = opt_text + '\nFood Needed:'
            
            final_food_choices = opt['Final Food Choices']
            food_cost_dict = opt['Food Cost Dict']
            for food in final_food_choices:
                opt_text = opt_text + '\n' + str(final_food_choices[food]) + "x " + str(food) + " ($" + str(food_cost_dict[food]) + "/ea)"
            opt_text = opt_text + '\nTotal Food Cost: $' + str(opt['Total Food Cost'])


            opt_text = opt_text + '\n\n---------------------DRINK INFORMATION---------------------'
            opt_text = opt_text + '\nDrinks Needed:'

            final_drink_choices = opt['Final Drink Choices']
            drink_cost_dict = opt['Drink Cost Dict']
            for drink in final_drink_choices:
                opt_text = opt_text + '\n' + str(final_drink_choices[drink]) + "x " + str(drink) + " ($" + str(drink_cost_dict[drink]) + "/ea)"
            opt_text = opt_text + '\nTotal Drink Cost: $' + str(opt['Total Drink Cost'])
            
            opt_text = opt_text + '\n\n---------------Final Food/Drink Assignments---------------'
            final_fdc = opt['Final Food Drink Combinations']

            for info in final_fdc:
                if info[4] == 0:
                    s = info[0] + "*: " + info[1] + " and " + info[2] + " ($" + str(info[3]) + ")"
                else:
                    s = info[0] + ": " + info[1] + " and " + info[2] + " ($" + str(info[3]) + ")"

                opt_text = opt_text + '\n' + s
            

            opt_text = opt_text + '\n* - Preference not met'

        self.res.config(state=NORMAL)        
        self.res.insert(INSERT, opt_text)
        self.res.config(state=DISABLED)

root = Tk()
root.config(background = "#80dfff")
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.geometry('%sx%s' % (width, height))
app = App(root)

root.mainloop()
