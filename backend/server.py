from flask import Flask
from flask import request, jsonify
from config import app, db
from models import Veggies


app = Flask(__name__)

@app.route("/")
def main():
    return("Hi")


if __name__ == "__main__":
    app.run(debug=True)