# pylint: disable=no-member
from cqrs_app.extensions import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    body = db.Column(db.Text, nullable=False)

    def __init__(self, title, body):
        self.title = title
        self.body = body
