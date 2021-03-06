from sqlalchemy import event

from db_replication.extensions import arango
from db_replication.models.relational.user import User


@event.listens_for(User, "after_insert")
def user_after_insert(mapper, connection, target: User):
    repr = {
        "_key": target.username,
        "id": target.id,
        "username": target.username,
        "email": target.email,
    }
    arango.db.collection("User").insert(repr)


@event.listens_for(User.following, "append")
def user_following_append(target: User, value: User, initiator):
    arango.db.collection("Following").insert(
        {"_from": f"User/{target.username}", "_to": f"User/{value.username}"}
    )


@event.listens_for(User.following, "remove")
def user_following_remove(target: User, value: User, initiator):
    arango.db.collection("Following").delete_match(
        {"_from": f"User/{target.username}", "_to": f"User/{value.username}"}
    )
