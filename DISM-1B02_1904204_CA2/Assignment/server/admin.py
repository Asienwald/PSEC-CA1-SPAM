import shlex
import os.path
dir_path = os.path.dirname(os.path.realpath(__file__))
from db import Database
from misc import convert_cost_to_currency

# Controls all admin actions to modify database
class Admin():
    db = Database()
    day_of_week = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", 
                   "Saturday", "Sunday")

    # parse food rows and display
    def display_food_rows(self, rows):
        print(f"Found {len(rows)} matches.\n")
        for count, row in enumerate(rows):
            price = convert_cost_to_currency(row[2])
            print(f"{count + 1}. {row[0]:<20s} <{row[3]}>\tPrice: {price}")

            days_avail = []
            for day_num in row[4]:
                days_avail.append(self.day_of_week[int(day_num)])
            print(f"\tDays Available: {', '.join(days_avail)}")
        print("---------------------------------")

    # parse promo rows and display
    def display_promo_rows(self, rows):
        for row in rows:
            day = self.day_of_week[row[2]]
            print(f"<{day}>")
            print(f"Description: {row[0]}")
            print(f"FoodType: {row[1]}")
            print(f"Discount: {row[3]}")
            print("-----------------------------\n")

    # parse log rows and display
    def display_log_rows(self, rows):
        print("Displaying Logs...")
        print(f"Total {len(rows)} logs.\n")

        for row in rows:
            price = convert_cost_to_currency(row[2])
            print(f"{row[0]}\t{row[1]:<4} Items\t{price:<8} total.")
        print("---------------------------------")

    # Food Menu Actions
    def search_food(self):
        query = input("Search Food: ")
        rows = self.db.get_similar_food_by_name(query)
        self.display_food_rows(rows)

    # list all food in db table Food
    def list_food(self):
        rows = self.db.get_all_foods()
        self.display_food_rows(rows)

    # add food to db
    def add_food(self):
        def isFloat(string):
            try:
                float(string)
                return True
            except ValueError:
                return False
            
        # instructions
        print('Command to add: ADD "<food name>" "<image>" <price> <type> <days available>')
        print('''NOTE:
- Food Image refers to the name of the image used for the food
    - Image must be in the "images" directory
    - If path not found, "default.jpg" will be used
- Food Day will be a string of numbers 
    - Monday is 0, Tuesday is 1...Sunday is 6

Example usage: ADD "Carbonara" "carbonara.jpg" 9.90 "Western" 124
type "exit" to exit.''')
        cmd = input(">>> ")
        if cmd == "exit":
            return
        cmd_params = shlex.split(cmd)

        valid_foodtypes = ("Western", "Japanese", "Chinese", "Malay", "Drinks")
        try:
            # validating user input
            if cmd_params[0] == "ADD":
                if len(cmd_params) != 6:
                    print("Wrong length")
                    raise Exception
                elif not os.path.isfile(dir_path + "/images/" + cmd_params[2]):
                    print("Image file cannot be found in the images/ directory.")
                    print("default.jpg used.")
                    cmd_params[2] = "default.jpg"
                elif not isFloat(cmd_params[3]):
                    print("Give valid price.")
                    raise Exception
                elif cmd_params[4] not in valid_foodtypes:
                    print("Give valid food type.")
                    raise Exception
                elif not cmd_params[5].isnumeric():
                    print("Give valid available days.")
                    raise Exception
                self.db.add_food(cmd_params[1], cmd_params[2], cmd_params[3], cmd_params[4], cmd_params[5])
            else:
                raise Exception
        except Exception:
            print("Command Invalid.\n")
            self.add_food()

    # delete food from db with its name
    def delete_food(self):
        print('Command to Delete: DEL "<Food Name>"')
        print('''Note: Food name is case-sensitive
    Example: DEL "Nasi Lemak"''')
        cmd = input(">>> ")
        if cmd == "exit":
            return
        cmd_params = shlex.split(cmd)
        try:
            if cmd_params[0] == "DEL":
                if len(cmd_params) != 2:
                    raise Exception
                self.db.del_food(cmd_params[1])
            else:
                raise Exception
        except Exception:
            print("Command Invalid.\n")
            self.delete_food()

    # Promo Menu Actions
    def list_promos(self):
        rows = self.db.get_promos()
        self.display_promo_rows(rows)

    # change promo for certain day
    def modify_promos(self):
        print('Command to Modify: MOD "<Day>" "<Description>" "<Food Type>" <Discount>')
        print('''Note:
- Day is numeric (0 for monday, 2 for tuesday, ..., 6 for sunday
- Food type is case sensitive
    - Valid food types = (Western, Japanese, Malay, Chinese, Drinks, All)
- Discount is a float between 0 and 1

Example: MOD 1 "30% off Malay on Tuesdays!" "Malay" 0.3
Type "exit" to exit''')
        cmd = input(">>> ")
        if cmd == "exit":
            return
        cmd_params = shlex.split(cmd)
        valid_foodtypes = ("Western", "Japanese", "Chinese", "Malay", "Drinks", "All")
        try:
            if cmd_params[0] == "MOD":
                if len(cmd_params) != 5:
                    raise Exception
                elif int(cmd_params[1]) < 0 or int(cmd_params[1]) > 6:
                    print("Invalid day.")
                    raise Exception
                elif cmd_params[3] not in valid_foodtypes:
                    print("Invalid food type.")
                    raise Exception
                elif float(cmd_params[4]) < 0 or float(cmd_params[4]) > 1:
                    print("Invalid discount.")
                    raise Exception
                self.db.update_promo(cmd_params[2], cmd_params[3], cmd_params[1], cmd_params[4])
            else:
                raise Exception
        except Exception as e:
            print(e)
            print("Command Invalid.\n")
            self.modify_promos()



# to handle menus to display
class AdminMenu():
    admin = Admin()

    # Start Menu
    def start_menu(self):
        actions = {1: self.food_menu, 2: self.promo_menu, 3: self.list_logs,
                   4: exit}
        try:
            print("\n>>> Admin Menu for SPAM <<<\n")
            inp = int(input('''Choose Category:
1. Food
2. Promos
3. List Logs
4. Exit
>>> '''))
            if inp in list(actions.keys()):
                actions[inp]()
            else:
                raise ValueError
        except Exception:
            print("Input invalid.")
            self.start_menu()

    # Food Menu
    def food_menu(self):
        actions = {1: self.admin.search_food, 2: self.admin.list_food, 
                   3: self.admin.add_food, 4: self.admin.delete_food,
                   5: self.start_menu}
        try:
            print("\n>>> Food Menu <<<\n")
            inp = int(input('''Choose Action:
1. Search Food
2. List Food
3. Add Food
4. Delete Food
5. Back
>>> '''))
            if inp in list(actions.keys()):
                actions[inp]()
                self.food_menu()
            else:
                raise ValueError
        except Exception as e:
            print(e)
            print("Input invalid.")
            self.food_menu()

    # Promo Menu
    def promo_menu(self):
        actions = {1: self.admin.list_promos, 2: self.admin.modify_promos, 
                   3: self.start_menu}
        try:
            print("\n>>> Promo Menu <<<\n")
            inp = int(input('''Choose Action:
1. List Promo
2. Modify Promo
3. Back
>>> '''))
            if inp in list(actions.keys()):
                actions[inp]()
                self.promo_menu()
            else:
                raise ValueError
        except Exception:
            print("Input invalid.")
            self.promo_menu()

    # Log Menu Actions
    def list_logs(self):
        rows = self.admin.db.get_all_logs()
        self.admin.display_log_rows(rows)

        self.start_menu()


if __name__ == "__main__":
    admin_menu = AdminMenu()
    admin_menu.start_menu()
