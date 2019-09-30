# DB Replication Example

## To Run

```
docker-compose up -d
# Wait for things to finish starting...
docker-compose run flask initdb
```

Which starts:

+ The flask app
+ A [PostgreSQL](https://www.postgresql.org/) instance
+ An [ArangoDB](https://www.arangodb.com/) instance
+ An [Elasticsearch](https://www.elastic.co/) instance with a [Kibana](https://www.elastic.co/products/kibana) UI

## Relevant parts of the application

### [main/views.py](./db_replication/views/main/views.py)

The flask router itself. All the relevant endpoints can be found here.

### [models/relational](./db_replication/models/relational)

Our SQLAlchemy-defined relational models. These are standard Model definitions using the SQLAlchemy declarative base format.

#### User

Our standard social network user object. These users have a "following" relationship to other Users (the kind of thing you'd possibly want to store in a directed graph) and a collection of Posts.

#### Post

Posts are social media posts. They have a title and a body, and the body can get quite long. The kind of thing you'd want to store in a databased designed for document search and retrieval.

### [models/graph](./db_replication/models/graph)

This directory is composed of two files, `listeners.py` and `user.py`. `user.py` is just a module full of AQL executing functions, like you would use if ArangoDB was your primary datastore and you weren't using an ORM. `listeners.py` is where the magic happens.

SQLAlchemy exposes "event listeners" with annotations (there is also a more traditional syntax of [`event.listen`](https://docs.sqlalchemy.org/en/13/orm/events.html). Here, we're waiting for User inserts, and then modifications to the User.following collection. When we see one of those events, we are able to replicate the corresponding data changes to our ArangoDB instance.

### [models/document](./db_replication/models/document)

We have a similar setup Elasticsearch and Posts. `post.py` has a wrapper around an ES [more like this query](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-mlt-query.html) - an operation that has effectively no parallel in RDBMS land.

Since posts are not currently editable, we only need a single listener for Post inserts to replicate Posts to ES.

## See it in action

Login to http://localhost:5000/ with username "alice".

"Friends of Friends" is a demo of an ArangoDB graph query.

"More like this" is a demo of an Elasticsearch "more like this" query.

### ArangoDB

See: [http://localhost:8529](http://localhost:8529/_db/docker/_admin/aardvark/index.html#graph/users-following)

### Elasticsearch

See: [http://localhost:5601](http://localhost:5601/app/kibana)

You'll need to create an index filter for "post".
