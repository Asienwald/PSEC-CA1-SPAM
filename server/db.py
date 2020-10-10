import sqlite3 as sql
from datetime import datetime
import re
# from food import Food
from misc import convert_cost_to_currency
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

# Database class to handle everything database
class Database():
    # establish connection to the database
    def __init__(self):
        try:
            self.conn = sql.connect(dir_path + "/spam.db")
            self.cursor = self.conn.cursor()
        except Exception as e:
            print(e)
            print("An error occured. Please try again later.")

    # commit sql query and check for errors
    def commit_db(self):
        try:
            self.conn.commit() 
            print("Query commited successfully.")
        except Exception as e:
            print(e)
            print("There was an error with your query.")

    # fetch rows from sql query
    def fetch_rows(self, sql):
        self.cursor.execute(sql)

        rows = self.cursor.fetchall()
        print("Query successful. Rows fetched.")
        return rows

    # add food into database
    def add_food(self, food_name, food_img, food_price, food_type, food_day):
        def check_exists():
            sql = "SELECT 1 FROM Food WHERE FoodName = ? LIMIT 1;"
            self.cursor.execute(sql, (food_name,))
            return self.cursor.fetchone() is not None

        if check_exists():
            print("Food already exists.\n")
            return
        if food_img == "":
            food_img = "default.jpg"
        sql = "INSERT INTO Food VALUES (?, ?, ?, ?, ?);"
        data_tuple = (food_name, food_img, food_price, food_type, food_day)
        self.cursor.execute(sql, data_tuple)
        self.commit_db()

    # delete food item in database
    def del_food(self, food_name):
        def check_exists():
            sql = "SELECT 1 FROM Food WHERE FoodName=? LIMIT 1;"
            self.cursor.execute(sql, (food_name,))
            return self.cursor.fetchone() is not None

        if not check_exists():
            print("Food does not exist.\n")
            return

        sql = "DELETE FROM Food WHERE FoodName=?;"
        self.cursor.execute(sql, (food_name,))
        self.commit_db()

    # change values of certain promo day
    def update_promo(self, description, food_type, day, disc):
        sql = "UPDATE Promos SET Description=?, FoodType=?, Day=?, Discount=? WHERE Day=?"
        data_tuple = (description, food_type, day, disc, day)
        self.cursor.execute(sql, data_tuple)
        self.commit_db()

    # add a log into the database
    def add_log(self, total_items, total_cost):
        dt = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        
        sql = "INSERT INTO Log VALUES(?, ?, ?);"
        data_tuple = (dt, total_items, total_cost)

        self.cursor.execute(sql, data_tuple)
        self.commit_db()

    # get food by its name from db
    def get_food_by_name(self, food_name):
        sql = f"SELECT * FROM Food WHERE FoodName='{food_name}';"
        return self.fetch_rows(sql)

    # filter food by their availability
    def get_food_by_day(self, food_day):
        sql = f"SELECT * FROM Food WHERE FoodDay LIKE '%{food_day}%';"
        return self.fetch_rows(sql)

    # filter food by their type
    def get_food_by_type(self, food_type):
        print(f"You searched for foods of type <{food_type}>")

        sql = f"SELECT * FROM Food WHERE FoodType='{food_type}' COLLATE NOCASE;"
        return self.fetch_rows(sql)

    # get food from db by similar name
    def get_similar_food_by_name(self, query):
        if len(query) <= 2:
            return []
        sql = f"SELECT * FROM Food WHERE FoodName LIKE '%{query}%';"
        return self.fetch_rows(sql)

    ## Below functions' names are pretty self explainatory
    def get_all_logs(self):
        sql = "SELECT * FROM Log;"
        return self.fetch_rows(sql)

    def get_all_foods(self):
        sql = "SELECT * FROM Food;"
        return self.fetch_rows(sql)

    def get_foodcourts(self):
        sql = "SELECT * FROM Stalls;"
        return self.fetch_rows(sql)

    def get_promos(self):
        sql = "SELECT * FROM Promos;"
        return self.fetch_rows(sql)