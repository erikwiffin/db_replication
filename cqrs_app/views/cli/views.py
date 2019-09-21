# pylint: disable=no-member
import click
from flask import Blueprint

from cqrs_app.application import app
from cqrs_app.extensions import arango, db, es
from cqrs_app.models.relational.user import User


BP = Blueprint("cli", __name__)


@app.cli.command()
def initdb():
    arango.db.collection("User").truncate()
    arango.db.collection("Following").truncate()

    try:
        es.client.indices.delete("social-network")
    except:
        pass

    db.drop_all()
    db.create_all()

    user1 = User("alice", "alice@example.com")
    user2 = User("bob", "bob@example.com")
    user3 = User("carol", "carol@example.com")
    user4 = User("carlos", "carlos@example.com")
    user5 = User("charlie", "charlie@example.com")
    user1.follow(user2)
    user2.follow(user3)
    user2.follow(user4)
    user2.follow(user5)

    user1.write_post("Test Post", "Lorem ipsum dolor sit amet")
    user1.write_post("Test Post 2", "consectetur adipiscing elit")

    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.add(user4)
    db.session.add(user5)
    db.session.commit()

