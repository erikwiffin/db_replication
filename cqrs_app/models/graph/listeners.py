from sqlalchemy import event

from cqrs_app.extensions import arango
from cqrs_app.models.relational.user import User


def my_after_insert_listener(mapper, connection, target: User):
    repr = {
        "_key": target.username,
        "id": target.id,
        "username": target.username,
        "email": target.email,
    }
    arango.db.collection("User").insert(repr)

    for followee in target.following:
        arango.db.collection("Following").insert(
            {"_from": f"User/{target.username}", "_to": f"User/{followee.username}"}
        )


# associate the listener function with SomeClass,
# to execute during the "before_insert" hook
event.listen(User, "after_insert", my_after_insert_listener)
