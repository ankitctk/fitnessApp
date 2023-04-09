"""""
from . import db

class diet(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    food_name = db.Column(db.String(200), nullable = False)
    calories = db.Column(db.Integer, nullable = False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.food_name}"

"""