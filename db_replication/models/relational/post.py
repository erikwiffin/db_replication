# pylint: disable=no-member
from sqlalchemy.sql import func

from db_replication.extensions import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    body = db.Column(db.Text, nullable=False)

    created = db.Column(db.DateTime, default=func.now())

    def __init__(self, title, body):
        self.title = title
        self.body = body
