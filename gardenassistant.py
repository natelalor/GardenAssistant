# Nathan Lalor
# February 26th, 2024

# Garden Assistant Application
# ------------------------------
# A tool to assist garden layout planning, which will calculate optimized garden layout based on dimensions and desired vegetables.

# imports
import sqlite3


def main():
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

    # # code block to ensure execution success
    # cursor.execute("SELECT * FROM veggies")
    # results = cursor.fetchall()
    # print(results)


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

    
    veggie_info = []
    # retrieve veggies associated to each pk / integer in veggies_list
    for num in veggies_list:
        execute_statement = "SELECT name, sbp, sbr FROM veggies WHERE veggie_id=" + num
        cursor.execute(execute_statement)
        dimensions = (cursor.fetchone())

        # now add a third unit, density of veggie
        dimensions = list(dimensions)
        density = dimensions[1] * dimensions[2]
        dimensions.append(density)
        veggie_info.append(dimensions)
    
    # veggie_info list will now hold info in order: name, sbp, sbr, density

    # analyze units recieved and prepare variables for algorithm
    length_of_garden_feet = dimensions_list[0]
    length_of_garden = length_of_garden_feet * 12
    width_of_garden_feet = dimensions_list[1]
    width_of_garden = width_of_garden_feet * 12
    
    # ALGORITHM TO FIND PERCENTAGE (dont think its needed)
    # for veggie_info in veggie_dimensions:
    #     percent_of_area = 100 * (float(veggie_info[2]) / float(area_of_garden))
    #     print("Veggie takes up ", percent_of_area, "%% of the garden, with a density of ", veggie_info[2])
    
    # find maximum plants to fill 1 row without going over width of total area (and return how long it would be) (thus, we should know remainder as well)
    # find how long a row of each plant will be (and return the unit)
    total_length_all_veggies = 0
    complete_veggie_information = []
    for veggie in veggie_info: 
        width_row_information = total_width_per_plant(width_of_garden, veggie)
        total_length_all_veggies += veggie[2]

        temp_veggie_list = []
        temp_veggie_list.append(veggie[3]) # DENSITY
        temp_veggie_list.append(veggie[0]) # NAME
        temp_veggie_list.append(veggie[1]) # SBP
        temp_veggie_list.append(veggie[2]) # SBR
        temp_veggie_list.append(veggie[2]) # LENGTH PER ROW
        temp_veggie_list.append(width_row_information) # WIDTH PER ROW

        complete_veggie_information.append(temp_veggie_list)

    # add up all lengths of all plants to see if 1 row of each plant type doesn't exceed total length
    if length_of_garden > total_length_all_veggies:
        # this means we can fit at least one row of each veggie type
        
        # create set of veggies to send over to algorithm function (since we can fit one row of each, we send over all plant types)
        # this set must be ordered by largest plant to smallest plant (of total area, so both sbp and sbr are considered)
        sorted_complete_veggie_information = sorted(complete_veggie_information, reverse=True) # reverse so that largest is first
        
        # sorted_complete_veggie_information IS NOW IN FORMAT:
        # [
            # [BIGGEST density, name, sbp, sbr, length per row, [# of type able to be planted per row, total width per row]],
            # [density, name, sbp, sbr, length per row, [# of type able to be planted per row, total width per row]],
            # [density, name, sbp, sbr, length per row, [# of type able to be planted per row, total width per row]],
            # ...
            # ...
            # ...
            # [SMALLEST density, name, sbp, sbr, length per row, [# of type able to be planted per row, total width per row]]
        # ]


        # now we call algorithm with the sorted list, as well as the dimensions of the garden to fill it
        fill_the_garden(sorted_complete_veggie_information, length_of_garden, width_of_garden)




        # print("One row of each veggie can fit into your garden. It will be ", total_length_all_veggies, "inches and you will have ", length_of_garden-total_length_all_veggies, " space left over.")

    else:
        # this means we cannot fit one row of each veggie type
        hi = 1

        # TODO: we have to facilitate the splitting into columns and subsets of veggies here.
        # once that is done, we can call fill_the_garden() on both subsets




def total_width_per_plant(width_of_garden, veggie):
    # equal to sbp
    width_per_plant = veggie[1]

    # this will be total number of each plant you are able to plant
    counter = 0

    # a loop to figure out how many plants are able to be planted per row.
    # simultaneously figured out how many plants that will be, as well as the total width taken up (and thus the remainder)
    while width_of_garden >= width_per_plant:
        width_of_garden -= width_per_plant
        counter += 1
    
    total_width_taken_in_inches = width_per_plant * counter

    # print("You can fit ", counter, veggie[0] + "s into your garden. It will take up ", total_width_taken_in_inches, " inches of width, and you will have ", width_of_garden, " left over.")

    # counter = how many of that plant type can be planted per row
    # total_width_taken_in_inches = how long the row is (before running out of room in garden)
    width_row_information = [counter, total_width_taken_in_inches]
    return width_row_information

# this is the main algorithm chunk, where it facilitates
# filling up the garden in the best way possible, iterating
# between rows and plant types until all the possible plants are planted.
def fill_the_garden(sorted_complete_veggie_information, length_of_garden, width_of_garden):
    # this will facilitate changing the plant type using density_list
    iterator = 0

    print(sorted_complete_veggie_information) 
    # some condition here?
    # is there enough room for another row of the biggest plant?
        #add it
    # else



    return 1 



if __name__ == "__main__":
    main()
