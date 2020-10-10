# Contains misc functions
import re

# make sure currency values have 2 dp
def convert_cost_to_currency(money):
    if type(money) != str:
        money = str(money)
    money = round(float(money.replace("$", "")), 2)
    return "${:.2f}".format(money)