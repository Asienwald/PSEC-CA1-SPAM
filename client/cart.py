# import kivy modules
from kivy.uix.label import Label
from food import Food, all_foods
# import regex module
import re

# import my module
from misc import convert_cost_to_currency

class MyLabel(Label):
    pass

# cart class
class Cart():
    food_items: list = []
    total_items: str = "0"
    total_cost: str = "$0.00"

    # update the cart screen to display items
    def update_cart_screen(self, sm):
        cart_tab = sm.get_screen("cart-screen").ids.cart_tab
        cart_tab.clear_widgets()

        for food in self.food_items:
            food_label = food.init_food_label(sm)
            food_label_amt = MyLabel(text=str(food.amount), font_size=15)

            food_label.add_widget(food_label_amt)

            cart_tab.add_widget(food_label)

    # sarch for similar food by name (no need match fully)
    def search_similar_food(self, query: str):
        if len(query) <= 2:
            return []
        if " " in query:
            query_list = query.split(" ")
            query = ".*".join(query_list)
        food_matches = []
        if not re.match(r"^\S+$", query):
            return food_matches
        for food in all_foods:
            if re.match(f".*{query.lower()}.*", food.food_name.lower()):
                food_matches.append(food)
        return food_matches

    # find food by name (must match fully)
    def find_food_by_name(self, food_name: str):
        for food in all_foods:
            # for food in food_list:
            if food_name == food.food_name:
                return food

    # use this function with food name to update food in cart
    def update_food_items(self, food_name: str, amt: int):
        food = self.find_food_by_name(food_name)
        self.set_food_to_cart(food, amt)
                    
        self.calculate_total_cost()
        self.calculate_total_items()

    # add food to cart
    def set_food_to_cart(self, food: Food, amt: int):
        # if food item alrdy in list
        for food_in_cart in self.food_items:
            if food.food_name == food_in_cart.food_name:
                food_in_cart.amount = amt
                if food_in_cart.amount <= 0:
                    self.food_items.remove(food_in_cart)
                    food_in_cart.amount = 0
                return
        # if food item not in list and amount is not zero
        if amt > 0:
            food.amount = amt
            self.food_items.append(food)
        
    # calculate total cost of food in cart
    def calculate_total_cost(self):
        total_cost: float = 0
        for food in self.food_items:
            food_price = food.food_price
            food_price = float(food_price.replace('$', ""))
            indiv_cost = food_price * food.amount
            total_cost += indiv_cost
        self.total_cost = "$" + str(total_cost)
        self.total_cost = convert_cost_to_currency(self.total_cost)

    # calculate total items in cart
    def calculate_total_items(self):
        total_items = 0
        for food_in_cart in self.food_items:
            total_items += food_in_cart.amount
        total_items = 0 if total_items < 0 else total_items
        self.total_items = str(total_items)