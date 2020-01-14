import os
import uuid

from sqla_wrapper import SQLAlchemy

db = SQLAlchemy(os.getenv("DATABASE_URL",
                          "sqlite:///localhost.sqlite")
                )


class User(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    # Login information
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    token = db.Column(db.String)
    # Additional info
    name = db.Column(db.String)
    # For game playing
    secret_number = db.Column(db.Integer)
    def profile_url(self):
        return f"/profiles/{self.uid}"

def init_data():
    db.drop_all()
    db.create_all()

    for j in range(1, 6):
        uporabnik1 = User(
            name="Uporabnik" + str(j),
            email="uporabnik" + str(j) + "@neki.domena.si",
            password="password",
            token=str(uuid.uuid4()),
            secret_number=-1
        )
        db.add(uporabnik1)
    db.commit()
