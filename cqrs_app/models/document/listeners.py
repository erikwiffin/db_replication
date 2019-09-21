from sqlalchemy import event

from cqrs_app.extensions import es
from cqrs_app.models.relational.post import Post


def my_after_insert_listener(mapper, connection, target: Post):
    repr = {"id": target.id, "title": target.title, "body": target.body}

    es.index(index="social-network", doc_type="post", id=target.id, body=repr)


# associate the listener function with SomeClass,
# to execute during the "before_insert" hook
event.listen(Post, "after_insert", my_after_insert_listener)
