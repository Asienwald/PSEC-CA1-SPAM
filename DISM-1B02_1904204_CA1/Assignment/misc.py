# Contains misc functions

# make sure currency values have 2 dp
def convert_cost_to_currency(money):
    money = round(float(money.replace("$", "")), 2)
    return "${:.2f}".format(money)