from flask import Flask
from flask import request, jsonify
from config import app, db
from models import Veggies


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
#     if request.method == "POST":
#         length = request.form["length"]
#         width = request.form["width"]
#         return jsonify({"legnth": length, "width": width})
#     else:
#         return("This is GET!")

# @app.route("/veggies")
# def get_veggies():
#     veggies = Veggies.query.all()
#     json_veggies = list(map(lambda x: x.to_json(), veggies))
#     return jsonify({"veggies": json_veggies})


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
