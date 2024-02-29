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

    # figure out which veggies they are using
    veggie_list = vegetable_selection()

    # run algorithm to decide # of column objects to store in garden collection
    list_of_columns = how_many_columns(veggie_list, my_garden)


    




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


# a function to facilitate the selection
# of vegetables by the user
def vegetable_selection():
    print("Vegetable Key List:")
    print("--------------------------")
    print("1 - Carrot")
    print("2 - Potato")
    print("3 - Tomato")
    print("4 - Brussel Sprout")
    print("5 - Spinach")
    print("6 - Broccoli")
    print("7 - Snap Peas")
    print("8 - Onion")
    print("9 - Lettuce")
    print("10 - Cabbage")
    print("--------------------------")
    raw_user_veggie_list = input("Please write down all numbers associated with the vegetables you want to plant: ")

    # turn user's feedback into a list of primary keys associated with out db,
    # i.e., create a list of keys for which veggies to select from db
    sanitized_raw_user_veggie_list = raw_user_veggie_list.replace(" ", "")
    user_veggie_list = list(sanitized_raw_user_veggie_list)
    return user_veggie_list





def how_many_columns(veggie_list, my_garden):
    # establish connection to db
    conn = sqlite3.connect("veggies.db")
    cursor = conn.cursor()

    total_sbr = 0
    for num in veggie_list:
        cursor.execute("SELECT sbr FROM veggies WHERE veggie_id=" + num)
        result = cursor.fetchone()
        sbr = result[0]
        total_sbr += sbr

    print(total_sbr)

    subsets = []
    if my_garden.length > total_sbr:
        subsets.append(veggie_list)
        return subsets
    else:
        #this is where we need to figure out how many columns to add
        pass
        



if __name__ == "__main__":
    main()








