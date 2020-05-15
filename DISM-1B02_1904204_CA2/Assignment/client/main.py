# Kivy modules to import
from kivy.config import Config
# make windows unresizable
Config.set('graphics', 'resizable', False)
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, SwapTransition
from kivy.core.window import Window
from kivy import utils
from kivy.animation import Animation, AnimationTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder
# my modules to import
from food import all_foodcourts
from cart import Cart
from promo import PromoManager
from client import Client
# fix windows size
Window.size = (480, 853)

# init bg colour of start screen
class StartScreen(Screen):
    Window.clearcolor = utils.get_color_from_hex("#040e0d0")

# init bg colour of normal screens
class MainScreen(Screen):
    Window.clearcolor = utils.get_color_from_hex("#00ced1")

# search menu screen
class SearchScreen(Screen):
    pass

# Food stall screen
class FoodScreen(Screen):
    pass

# food detail screen
class FoodDetailsScreen(Screen):
    food_amount: str = "0"

    # update food amount label
    def update_food_amt(self):
        self.ids.food_amt_label.text = self.food_amount

    # increase food amount label
    def inc_food_amt(self):
        # print("Increase!")
        self.food_amount = str(int(self.food_amount) + 1)
        self.update_food_amt()

    # decrease food amount label     
    def dec_food_amt(self):
        # print("Decrease!")
        if int(self.food_amount) > 0:
            self.food_amount = str(int(self.food_amount) - 1)
        else:
            self.food_amount = "0"
        self.update_food_amt()

# checkout screen
class CheckoutScreen(Screen):
    pass

# promotions screen
class PromoScreen(Screen):
    pass

# cart screen
class CartScreen(Screen):
    pass

# widgets init here but real content in .kv file
class MenuLayout(BoxLayout):
    pass

class MyLabel(Label):
    pass

# my own screen manager to control the screens
class MyScreenManager(ScreenManager):
    # change the screen
    def change_screen(self, name):
        for c in self.get_screen(name).ids.main_box.children:
            if type(c) == MenuLayout:
                self.get_screen(name).ids.main_box.remove_widget(c)
        # reload updated menu button when screen changed
        self.user_menu = Builder.load_string('''
MenuLayout:
    orientation: "horizontal"
    size_hint: None, None
    BoxLayout:
        orientation: "horizontal"
        size: (root.width * 0.7, self.parent.height)
        size_hint: None, None
        padding: (20, 0)
        MyLabel:
            text: "Items: "
            bold: True
        MyLabel:
            text: app.my_cart.total_items
        MyLabel:
            bold: True
            text: "Cost: "
        MyLabel:
            text: app.my_cart.total_cost
    RelativeLayout:
        ButImage:
            id: cart_btn
            source: "images/cart.png"
            pos: (menu_btn.x, menu_btn.y)
            on_press: app.open_cart()
        ButImage:
            id: promo_btn
            source: "images/promo.png"
            pos: (menu_btn.x, menu_btn.y)
            on_press: app.change_screen("promo-screen")
        ButImage:
            id: eat_btn
            source: "images/eat.png"
            pos: (menu_btn.x, menu_btn.y)
            on_press: app.change_screen('main-screen')
        ButImage:
            id: menu_btn
            source: "images/menu.png"
            pos: (0, self.parent.height * 0.3)
            on_press: app.toggle_menu(root)
            ''')
        self.user_menu.size = (Window.width, Window.height * 0.1)
        self.get_screen(name).ids.main_box.add_widget(self.user_menu)
        self.current = name

# set transition type for screen manager
sm = MyScreenManager(transition=SwapTransition())

# my main root app
class SpamApp(App):
    my_cart: Cart

    # run first when executed
    def build(self):
        # load the .kv file
        self.load_kv("layout.kv")
        # init all the diff screens
        sm.add_widget(StartScreen(name="start-screen"))
        sm.add_widget(MainScreen(name="main-screen"))
        sm.add_widget(SearchScreen(name="search-screen"))
        sm.add_widget(FoodScreen(name="food-screen"))
        sm.add_widget(FoodDetailsScreen(name="food-details-screen"))
        sm.add_widget(CartScreen(name="cart-screen"))
        sm.add_widget(CheckoutScreen(name="checkout-screen"))
        sm.add_widget(PromoScreen(name="promo-screen"))

        # init my cart object
        self.my_cart = Cart()

        # init all the promos
        my_promo_manager = PromoManager()
        my_promo_manager.init_promos(sm)

        # start app with start screen
        sm.current = "start-screen"
        return sm

    def change_screen(self, name):
        sm.change_screen(name)

    # go back to previous page
    def go_back(self):
        sm.change_screen(sm.previous())

    # search for food by name
    def search_food(self):
        food_query = sm.get_screen('main-screen').ids.search_box.text
        matches = self.my_cart.search_similar_food(food_query)

        search_grid = sm.get_screen('search-screen').ids.search_grid
        search_grid.clear_widgets()

        if len(matches) == 0:
            search_grid.add_widget(MyLabel(text="No Matches :(", font_size=40))
        else:
            for food in matches:
                food_label = food.init_food_label(sm)
                search_grid.add_widget(food_label)
        sm.get_screen('main-screen').ids.search_box.text = ""
        self.change_screen('search-screen')

    # open specific foodcourt page based on index
    def open_foodcourt(self, root, ind: int):
        current_fc = all_foodcourts[ind]
        current_fc.display_food_screen(root, sm)

        self.change_screen('food-screen')

    # open the cart screen
    def open_cart(self):
        self.my_cart.update_cart_screen(sm)
        self.change_screen('cart-screen')

    # add food to cart
    def modify_cart(self):
        food_amt = int(sm.get_screen('food-details-screen').ids.food_amt_label.text)
        food_name = sm.get_screen('food-details-screen').ids.food_name.text

        self.my_cart.update_food_items(food_name, food_amt)

        self.change_screen('main-screen')

    # finalise cart and checkout
    def checkout(self):
        checkout_screen = sm.get_screen('checkout-screen')
        # print(self.my_cart.total_items)
        if self.my_cart.total_items in [0, "0"]:
            print("Cart can't be empty!")
            return

        client = Client()
        client.log_purchase(self.my_cart.total_items, self.my_cart.total_cost)

        checkout_screen.ids.items_label.text = f"You bought {self.my_cart.total_items} Items"
        checkout_screen.ids.cost_label.text = f"Your total cost is ${self.my_cart.total_cost}"
        sm.current = "checkout-screen"

    # menu button animation
    def toggle_menu(self, root):
        menu_btn = root.ids.menu_btn
        cart_btn = root.ids.cart_btn
        promo_btn = root.ids.promo_btn
        eat_btn = root.ids.eat_btn

        # close the menu
        if cart_btn.y != menu_btn.y:
            open_menu_anim = Animation(x=menu_btn.x, y=menu_btn.y,
                                       duration=0.3)
            open_menu_anim.start(cart_btn)
            open_menu_anim.start(promo_btn)
            open_menu_anim.start(eat_btn)
        # open the menu
        else:
            Animation(x=menu_btn.x, y=menu_btn.y + menu_btn.height * 1.5,
                      duration=0.3).start(cart_btn)
            Animation(x=menu_btn.x - menu_btn.width * 0.75,
                      y=menu_btn.y + menu_btn.height * 1.25,
                      duration=0.3).start(promo_btn)
            Animation(x=menu_btn.x - menu_btn.width, y=menu_btn.y,
                      duration=0.3).start(eat_btn)

    def exit_app(self):
        self.stop()

    
if __name__ == '__main__':
    SpamApp().run()