# Nathan Lalor
# February 26th, 2024

# Garden Assistant Application
# ------------------------------
# A tool to assist garden layout planning, which will calculate optimized garden layout based on dimensions and desired vegetables.

# imports
import sqlite3
from Garden import Garden


def main():

    # set up the database
    database_initialization()

    # create a garden object
    l_input = float(input("Length of Garden: "))
    w_input = float(input("Width of Garden: "))
    my_garden = Garden(l_input, w_input)
    
    print(my_garden.length)

    # user input to populate garden length & width

    # run algorithm to decide # of column objects to store in garden collection




# =========================================== #
#      BEGINNING OF SUPPORTING FUNCTIONS      #
# =========================================== #
    





# function to establish connection to the database,
# using SQLite. db is used to provide vegetable information,
# most importantly the dimension requirements
def database_initialization():

    # establish connection
    conn = sqlite3.connect("veggies.db")

    # create cursor
    cursor = conn.cursor()

    # create table "veggies"
    command1 = """CREATE TABLE IF NOT EXISTS
    veggies(veggie_id INT PRIMARY KEY, name TEXT, sbp INT, sbr INT)"""

    cursor.execute(command1)

    # add to table with our veggies

    # carrots
    cursor.execute("INSERT OR IGNORE INTO veggies VALUES (1, 'Carrot', 6, 23)")
    # potatoes
    cursor.execute("INSERT OR IGNORE INTO veggies VALUES (2, 'Potato', 11, 24)")
    # tomatoes
    cursor.execute("INSERT OR IGNORE INTO veggies VALUES (3, 'Tomato', 30, 5)")
    # brussel sprouts
    cursor.execute("INSERT OR IGNORE INTO veggies VALUES (4, 'Brussel Sprout', 21, 32)")
    # spinach
    cursor.execute("INSERT OR IGNORE INTO veggies VALUES (5, 'Spinach', 9, 13)")
    # broccoli
    cursor.execute("INSERT OR IGNORE INTO veggies VALUES (6, 'Broccoli', 21, 30)")
    # snap peas
    cursor.execute("INSERT OR IGNORE INTO veggies VALUES (7, 'Snap Peas', 2, 33)")
    # onions
    cursor.execute("INSERT OR IGNORE INTO veggies VALUES (8, 'Onion', 3, 3)")
    # lettuce
    cursor.execute("INSERT OR IGNORE INTO veggies VALUES (9, 'Lettuce', 13, 14)")
    # cabbage
    cursor.execute("INSERT OR IGNORE INTO veggies VALUES (10, 'Cabbage', 18, 27)")

    conn.commit()








if __name__ == "__main__":
    main()








