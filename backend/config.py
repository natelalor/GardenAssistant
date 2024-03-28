from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# some configurations
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///veggies.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# creates a database instance of veggies.db
db = SQLAlchemy(app)


