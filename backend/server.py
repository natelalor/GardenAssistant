from flask import Flask
from flask import request, jsonify
from config import app, db
from models import Veggies
from flask_cors import CORS

CORS(app)

@app.route("/", methods=["GET"])
def main():
    return jsonify(
        {
            "users": [
                'joe',
                'tim',
                'bob'
            ]
        }
    )

# route that is receiving form information
@app.route("/process-form", methods=["POST"])
def process_form():
    form_data = request.json
    length = form_data.get("length")
    width = form_data.get("width")
    veggies = form_data.get("veggies")
    # Process form data and execute backend functions as needed
    # For example:
    # length = form_data.get("length")
    # width = form_data.get("width")
    # veggies = form_data.getlist("veggies")
    
    # now that we have all the information we need, we can now
    # execute backend algorithms
    return jsonify({"length": length, "width": width, "veggies": veggies})


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
