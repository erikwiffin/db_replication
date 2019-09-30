# pylint: disable=no-member
from glob import glob
from pathlib import Path

import click
from flask import Blueprint

from db_replication.application import app
from db_replication.extensions import arango, db, es
from db_replication.models.relational.user import User


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

    posts_dir = Path(BP.root_path) / 'posts'
    for path in posts_dir.glob('*.txt'):
        with open(path) as fh:
            for i, line in enumerate(fh):
                user1.write_post(f'{ Path(path).name } { i }', line)

    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.add(user4)
    db.session.add(user5)
    db.session.commit()

