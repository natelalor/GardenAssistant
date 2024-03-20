


// this will hold all algorithms,
// will convert everything over that was in gardenassistant.py

// this is for the convenience of easier hosting and learning javascript

const sqlite3 = require('sqlite3').verbose();
const Garden = require('./Garden');
const Column = require('./Column');
const Row = require('./Row');


function main() {
    // set up the database
    databaseInitialization();

    // create a garden object
    const l_input = parseFloat(prompt("Length of Garden: "));
    const w_input = parseFloat(prompt("Width of Garden: "));
    const my_garden = new Garden(l_input, w_input);

    // figure out which veggies they are using
    const veggie_list = vegetableSelection();

    // run algorithm to decide # of column objects to store in garden collection
    const { subsets, number_of_columns } = howManyColumns(veggie_list, my_garden);
    console.log("You will need ", number_of_columns, " columns in your garden.");
    console.log("Here is your plant list, displayed for each column: ");
    console.log("----------------------------");
    subsets.forEach((column, index) => {
        console.log("Column ", index + 1, ": ", column);
    });

    // figure out width needed per column
    const width_per_column = my_garden.width / number_of_columns;

    // create columns and add it to garden's collection of columns
    for (let counter = 0; counter < number_of_columns; counter++) {
        const new_col = new Column(width_per_column);
        my_garden.columns.push(new_col);
    }

    // algorithm to populate columns
    for (let index = 0; index < my_garden.columns.length; index++) {
        const column = my_garden.columns[index];
        const result_list = fillTheGarden(column, subsets[index], my_garden.width, my_garden.length, veggie_list);
        // TODO: Handle results
    }
}

// Database initialization
function databaseInitialization() {
    const db = new sqlite3.Database('veggies.db', (err) => {
        if (err) {
            return console.error(err.message);
        }
        console.log('Connected to the veggies database.');
    });

    const createTableCommand = `CREATE TABLE IF NOT EXISTS veggies (
        veggie_id INTEGER PRIMARY KEY,
        name TEXT,
        sbp INTEGER,
        sbr INTEGER
    )`;

    db.run(createTableCommand, (err) => {
        if (err) {
            return console.error(err.message);
        }
        console.log('Veggies table created successfully.');
    });

    const veggiesData = [
        { id: 1, name: 'Carrot', sbp: 6, sbr: 23 },
        { id: 2, name: 'Potato', sbp: 11, sbr: 24 },
        { id: 3, name: 'Tomato', sbp: 30, sbr: 5 },
        { id: 4, name: 'Brussel Sprout', sbp: 21, sbr: 32 },
        { id: 5, name: 'Spinach', sbp: 9, sbr: 13 },
        { id: 6, name: 'Broccoli', sbp: 21, sbr: 30 },
        { id: 7, name: 'Snap Peas', sbp: 2, sbr: 33 },
        { id: 8, name: 'Onion', sbp: 3, sbr: 3 },
        { id: 9, name: 'Lettuce', sbp: 13, sbr: 14 },
        { id: 10, name: 'Cabbage', sbp: 18, sbr: 27 }
    ];

    const insertVeggiesCommand = 'INSERT OR IGNORE INTO veggies (veggie_id, name, sbp, sbr) VALUES (?, ?, ?, ?)';
    veggiesData.forEach((veggie) => {
        db.run(insertVeggiesCommand, [veggie.id, veggie.name, veggie.sbp, veggie.sbr], (err) => {
            if (err) {
                return console.error(err.message);
            }
            console.log(`Inserted ${veggie.name} into veggies table.`);
        });
    });

    db.close((err) => {
        if (err) {
            return console.error(err.message);
        }
        console.log('Closed the database connection.');
    });
}

function vegetableSelection() {
    console.log("Vegetable Key List:");
    console.log("--------------------------");
    console.log("1 - Carrot");
    console.log("2 - Potato");
    console.log("3 - Tomato");
    console.log("4 - Brussel Sprout");
    console.log("5 - Spinach");
    console.log("6 - Broccoli");
    console.log("7 - Snap Peas");
    console.log("8 - Onion");
    console.log("9 - Lettuce");
    console.log("10 - Cabbage");
    console.log("--------------------------");
    const raw_user_veggie_list = prompt(
        "Please write down all numbers associated with the vegetables you want to plant: "
    );

    const sanitized_raw_user_veggie_list = raw_user_veggie_list.replace(" ", "");
    const user_veggie_list = sanitized_raw_user_veggie_list.split("");
    return user_veggie_list;
}

function howManyColumns(veggie_list, my_garden) {
    let total_sbr = 0;
    const sbr_list = [];
    veggie_list.forEach((num) => {
        const sbr = retrieveSBR(num);
        total_sbr += sbr;
        sbr_list.push(sbr);
    });

    console.log(total_sbr);

    const subsets = [];
    if (my_garden.length * 12 > total_sbr) {
        subsets.push(veggie_list);
        return { subsets, number_of_columns: 1 };
    } else {
        // Placeholder logic, needs to be replaced with actual calculation
        return { subsets, number_of_columns: 0 };
    }
}

function fillTheGarden(column, subset, total_width, total_length, veggie_list) {
    console.log("COLUMN: ", column);
    console.log("SUBSETS: ", subset);

    // Establish connection to database
    const sqlite3 = require('sqlite3').verbose();
    const db = new sqlite3.Database('veggies.db');

    let remainingLength = totalLength * 12;
    let resultsList = [];
    let totalSbrList = [];
    let totalPlantsPerRowPerPlant = [];
    let smallestSbr = 999;

    for (const list of subset) {
        let sbrList = [];
        for (const veggie of list) {
            const sql = `SELECT sbr, sbp FROM veggies WHERE veggie_id = ?`;
            db.get(sql, [veggie], (err, row) => {
                if (err) {
                    console.error(err.message);
                    return;
                }
                const sbr = row.sbr;
                const sbp = row.sbp;
                sbrList.push(sbr);

                if (smallestSbr > sbr) {
                    smallestSbr = sbr;
                }

                const totalPlantsPerRow = Math.floor((totalWidth * 12) / sbp);
                totalPlantsPerRowPerPlant.push(totalPlantsPerRow);

                remainingLength -= sbr;
                const number_of_rows = 1;
                const newList = [totalPlantsPerRow, number_of_rows];
                resultsList.push(newList);

                const new_row = new Row(veggie);
                column.rows.push(new_row);
            });
        }
        totalSbrList.push(sbrList);
    }

    console.log(resultsList);
    console.log("SBR LIST:", totalSbrList);

    let iterator = 0;

    while (remainingLength >= smallestSbr) {
        if (remainingLength - totalSbrList[iterator][0] >= 0) {
            resultsList[iterator][0] += totalPlantsPerRowPerPlant[iterator];
            remainingLength -= totalSbrList[iterator][0];
            resultsList[iterator][1] += 1;

            const new_row = new Row(iterator + 1);
            column.rows.push(new_row);
        }

        if (iterator === totalSbrList.length - 1) {
            iterator = 0;
        } else {
            iterator += 1;
        }
    }

    return resultsList;
}

function retrieveSBR(num) {
    const sqlite3 = require('sqlite3').verbose();
    const db = new sqlite3.Database('veggies.db');

    return new Promise((resolve, reject) => {
        const sql = 'SELECT sbr FROM veggies WHERE veggie_id = ?';
        db.get(sql, [num], (err, row) => {
            if (err) {
                reject(err);
            } else {
                resolve(row.sbr);
            }
        });
    });
}

main();
