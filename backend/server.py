from flask import Flask
from flask import request, jsonify
from config import app, db
from models import Veggies
from flask_cors import CORS
CORS(app)
# algorithm imports
import sqlite3
from pprint import pprint
from Garden import Garden
from Column import Column
from Row import Row

@app.route("/", methods=["GET"])
def main():
    database_initialization()


# route that is receiving form information
@app.route("/process-form", methods=["POST"])
def process_form():
    form_data = request.json
    length = form_data.get("length")
    width = form_data.get("width")
    veggies = form_data.get("veggies")
    my_garden = Garden(length, width)
    
    # now that we have all the information we need, we can now
    # execute backend algorithms

    # run algorithm to decide # of column objects to store in garden collection
    subsets, number_of_columns = how_many_columns(veggies, my_garden)









    return jsonify({"length": length, "width": width, "veggies": veggies})

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

# function to decide # of column objects to store in garden collection (based on dimensions)
def how_many_columns(veggie_list, my_garden):
    total_sbr = 0
    sbr_list = []
    for num in veggie_list:
        sbr = retrieve_sbr(num)
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
        subsets, number_of_columns = column_facilitator(
            2, (my_garden.length * 12), subsets, veggie_list, sbr_list
        )
        return subsets, number_of_columns

def retrieve_sbr(num):
    # establish connection to db
    conn = sqlite3.connect("veggies.db")
    cursor = conn.cursor()

    cursor.execute("SELECT sbr FROM veggies WHERE veggie_id=" + num)
    result = cursor.fetchone()
    sbr = result[0]

    return sbr

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
