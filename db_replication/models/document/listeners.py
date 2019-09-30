from sqlalchemy import event

from db_replication.extensions import es
from db_replication.models.relational.post import Post


@event.listens_for(Post, "after_insert")
def post_after_insert(mapper, connection, target: Post):
    repr = {"id": target.id, "title": target.title, "body": target.body}

    es.index(index="post", id=target.id, body=repr)
