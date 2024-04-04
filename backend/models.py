from config import db

class Veggies(db.Model):
    veggie_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    sbp = db.Column(db.Integer, nullable=False)
    sbr = db.Column(db.Integer, nullable=False)

    def to_json(self):
        return {
            "veggie_id": self.veggie_id,
            "name": self.name,
            "sbp": self.sbp,
            "sbr": self.sbr,
        }