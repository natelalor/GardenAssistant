# Nathan Lalor
# February 26th, 2024

# Garden Assistant Application
# ------------------------------
# A tool to assist garden layout planning, which will calculate optimized garden layout based on dimensions and desired vegetables.

# imports
import sqlite3
from Garden import Garden
from Column import Column
from Row import Row


def main():

    # set up the database
    database_initialization()

    # create a garden object
    l_input = float(input("Length of Garden: "))
    w_input = float(input("Width of Garden: "))
    my_garden = Garden(l_input, w_input)

    # figure out which veggies they are using
    veggie_list = vegetable_selection()

    # run algorithm to decide # of column objects to store in garden collection
    subsets, number_of_columns = how_many_columns(veggie_list, my_garden)
    print("You will need ", number_of_columns, " columns in your garden.")
    print("Here is your plant list, displayed for each column: ")
    print("----------------------------")
    for index, column in enumerate(subsets):
        print("Column ", index + 1, ": ", column)
    
    # figure out width needed per column
    width_per_column = float(my_garden.width / number_of_columns)

    # create columns and add it to garden's collection of columns
    
    counter = 0
    while counter < number_of_columns:
        # TODO: do I need to initialize row collection here during column creation, as well as width? idk yet
        new_col = Column(width_per_column)
        my_garden.columns.append(new_col)
        counter += 1

    # algorithm to populate columns
    # until garden is FULL of rows
    for index, column in enumerate(my_garden.columns):
        fill_the_garden(column, subsets[index], my_garden.width, my_garden.length)


    # algorithm to create rows


    
        
    # add rows to columns
    









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
    raw_user_veggie_list = input(
        "Please write down all numbers associated with the vegetables you want to plant: "
    )

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
    sbr_list = []
    for num in veggie_list:
        cursor.execute("SELECT sbr FROM veggies WHERE veggie_id=" + num)
        result = cursor.fetchone()
        sbr = result[0]
        total_sbr += sbr
        sbr_list.append(sbr)

    print(total_sbr)

    subsets = []
    # TODO: FIX THIS!!!! CHANGE * 12! 'length' INPUT WONT ALWAYS BE IN FEET!
    if (my_garden.length * 12) > total_sbr:
        subsets.append(veggie_list)
        return subsets, 1
    else:
        # this is where we need to figure out how many columns to add
        subsets, number_of_columns = column_facilitator(2, (my_garden.length * 12), subsets, veggie_list, sbr_list)
        return subsets, number_of_columns


# Recursive function to sort plants into necessary # of columns
# to be within the length of garden
def column_facilitator(number_of_subsets, total_length, subsets, veggie_list, sbr_list):

    conn = sqlite3.connect("veggies.db")
    cursor = conn.cursor()

    # divvy up plants into equal chunks
    subsets = chunkify(veggie_list, number_of_subsets)

    # now, match the sbr_subsets list to be the same exact format as subsets list
    # i.e., make it a list of lists, where each list holds the same subset of plants
    sbr_subsets = []
    highest_sbr = -1
    for list in subsets:
        new_list = []
        for veggie in list:
            cursor.execute("SELECT sbr FROM veggies WHERE veggie_id=" + veggie)
            result = cursor.fetchone()
            sbr = result[0]
            new_list.append(sbr)

            # find the highest sbr value among all the plant's sbrs
            if sbr > highest_sbr:
                highest_sbr = sbr

        sbr_subsets.append(new_list)

    # TODO: MAKE THIS ALGORITHM MORE EFFICIENT!
    # goal of algorithm:
    # sbr_subsets is currently [[24, 5], [23]]
    # we test highest sbr against total length, so we need to add
    # together all sbr's that are in the same sublist
    # so, 24+5 = 29 -- new highest sbr
    for index, list in enumerate(sbr_subsets):
        if len(list) > 1:
            new_num = 0
            for sbr_value in list:
                new_num += sbr_value
            if new_num > highest_sbr:
                highest_sbr = new_num

    # base case
    if highest_sbr < total_length:
        return subsets, number_of_subsets
    else:
        column_facilitator(
            number_of_subsets + 1, total_length, subsets, veggie_list, sbr_list
        )


# thank you for this contribution, https://stackoverflow.com/questions/2130016/splitting-a-list-into-n-parts-of-approximately-equal-length
def chunkify(lst, n):
    return [lst[i::n] for i in range(n)]




# a function to fill the column with rows of it's associated list of veggies
# then will return amount of rows of which plant
def fill_the_garden(column, subsets, total_width, total_length):
   
    print("COLUMN: ", column)
    print("SUBSETS: ", subsets)

    # also will query database to retrieve SBP info for each plant, to see how it will apply to length

    # establish connection to db
    conn = sqlite3.connect("veggies.db")
    cursor = conn.cursor()

    remaining_length = total_length

    results_list = []

    # initial 1 of every veggie down
    for list in subsets:
        for veggie in list:
            cursor.execute("SELECT sbr, sbp FROM veggies WHERE veggie_id=" + veggie)
            result = cursor.fetchone()
            sbr = result[0]
            sbp = result[1]
            
            # figure out how many plants you can make per row
            total_plants_per_row = (total_width * 12) // sbp
            print("able to plant ", total_plants_per_row, " veggies of plant type ", veggie, " per row.")

            remaining_length -= sbr
            number_of_rows = 1
            new_list = [total_plants_per_row, number_of_rows]

            results_list.append(new_list)
            new_row = Row(veggie)
            column.rows.append(new_row)

    
    print(results_list)
    # TODO:
    # implement the if chains here, start iterating through all plant types
    # and see if you can add a row of it (restraints: if remaining_length - sbr > 0)     <--- this means we will need to save the sbr, 
    # make sure to have EQUAL plant type representation, refer to illustrating in book!      do we make anothr function? or sbr_list again?

            


    # WILL CREATE ROW OBJECTS IN HERE, at the end of the if chain


    return 1











if __name__ == "__main__":
    main()
