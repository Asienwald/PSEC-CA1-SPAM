# for checking of date
from datetime import date
# import the foods from my food module
from food import Food, myFoodManager, all_foods
food_cats = myFoodManager.food_categories
print(food_cats)
from client import Client
# import widgets from kivy module
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

# init widgets to use
class PromoLabel(BoxLayout):
    pass

class MyLabel(Label):
    pass


# manage all the promos
class PromoManager:
    all_promos = []

    # remove all current promos from foods
    def reset_all_promos(self):
        for food in all_foods:
            food.remove_discount()

    # apply promo of the day
    def apply_promos(self):
        today_date = date.today().weekday()
        for promo in self.all_promos:
            if int(promo.day) == int(today_date):
                promo.apply_promo_to_food_type()

    # get promos from server through client
    def read_promos(self):
        client = Client()
        client.get_promos()
        rows = client.pdata
        try:
            for row in rows:
                new_promo = Promo(row[0], row[1], row[2], row[3])
                self.all_promos.append(new_promo)
        except Exception:
            pass

    # display promos in promo screen
    def display_promos(self, sm):
        promo_grid = sm.get_screen("promo-screen").ids.promo_grid
        for promo in self.all_promos:
            promo_label = promo.init_promo_label()
            promo_grid.add_widget(promo_label)

    # call this to init all needed promo vars
    def init_promos(self, sm):
        # self.read_promo_file()
        self.read_promos()
        self.display_promos(sm)
        self.apply_promos()
                

# promo object
class Promo:
    def __init__(self, name: str, food_type: str, 
                 day: int, discount_amt: float):
        self.name = name
        self.food_type = food_type
        self.day = day
        self.discount_amt = discount_amt

    # apply itself to a food type
    def apply_promo_to_food_type(self):
        target_foods = food_cats[self.food_type]
        for food in target_foods:
            food.apply_discount(self.discount_amt)

    # init label to show promo info
    def init_promo_label(self):
        promo_label = PromoLabel(width=Window.width, size_hint=(None, None),
                               orientation="horizontal")
        promo_label_name = MyLabel(text=self.name, bold=True,
                                   font_size=25)
        if int(self.day) == int(date.today().weekday()):
            promo_label_name.color = (1, 0, 0, 1)
        promo_label.add_widget(promo_label_name)

        return promo_label