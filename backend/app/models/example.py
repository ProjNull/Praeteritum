from .. import db

class Example(db.Model):
    exampleid = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)

    def __init__(self, username: str):
        self.username = username

