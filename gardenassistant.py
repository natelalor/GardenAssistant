# Nathan Lalor
# February 26th, 2024

# Garden Assistant Application
# ------------------------------
# A tool to assist garden layout planning, which will calculate optimized garden layout based on dimensions and desired vegetables.

# imports
import sqlite3


def main():
    print("Welcome to the Garden Assistant Application")
    dimensions_list = dimension_of_user_garden()
    database_initialization()
    veggie_list = vegetable_selection()

    optimize_garden(dimensions_list, veggie_list)


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

    # code block to ensure execution success
    cursor.execute("SELECT * FROM veggies")
    results = cursor.fetchall()
    print(results)


# a function to gather data about
# user's garden dimensions
def dimension_of_user_garden():
    length_of_garden = float(input("Length (in feet) of garden dimensions (Ex: '10'): "))
    width_of_garden = float(input("Width (in feet) of garden dimensions (Ex: '10'): "))

    dimensions_list = [length_of_garden, width_of_garden]
    return dimensions_list


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

# a function that is the bulk of algorithm and processing
# for the application. It will retrieve the SBP (Space Between Plants),
# and SBR (Space Between Rows) for every plant suggested, and will
# use those as a guideline to optimize the spacial location for each vegetable
def optimize_garden(dimensions_list, veggies_list):
    # establish connection to db
    conn = sqlite3.connect("veggies.db")
    cursor = conn.cursor()

    veggie_dimensions = []
    # retrieve veggies associated to each pk / integer in veggies_list
    for num in veggies_list:
        execute_statement = "SELECT sbp, sbr FROM veggies WHERE veggie_id=" + num
        cursor.execute(execute_statement)
        dimensions = (cursor.fetchone())
        veggie_dimensions.append(dimensions)

    length_of_garden_feet = dimensions_list[0]
    length_of_garden = length_of_garden_feet * 12
    width_of_garden_feet = dimensions_list[1]
    width_of_garden = width_of_garden_feet * 12
    area_of_garden_feet = length_of_garden_feet * width_of_garden_feet
    area_of_garden = length_of_garden * width_of_garden

    # now that we have everything initialized and prepared, let's start
    # the algorithm

    






if __name__ == "__main__":
    main()
