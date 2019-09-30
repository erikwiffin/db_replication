from arango import ArangoClient, exceptions
from furl import furl


class ArangoExtension(object):
    def __init__(self, app=None):
        self.client = None
        self.db = None
        self.sys = None
        if app:
            self.init_app(app)

    def init_app(self, app):
        url = furl(app.config['ARANGODB_DATABASE_URI'])

        host = furl(scheme=url.scheme, host=url.host, port=url.port)
        db_name = str(url.path).strip('/')
        self.client = ArangoClient(hosts=host.url)
        self.db = self.client.db(name=db_name, username=url.username, password=url.password)

        try:
            self.db.status()
        except exceptions.ServerStatusError:
            sys_db = self.client.db(name="_system", username=url.username, password=url.password)
            sys_db.create_database(db_name)

        try:
            self.db.collection('User').properties()
        except exceptions.CollectionPropertiesError:
            self.db.create_collection('User')

        try:
            self.db.collection('Following').properties()
        except exceptions.CollectionPropertiesError:
            self.db.create_collection('Following', edge=True)

        try:
            self.db.graph('users-following').properties()
        except exceptions.GraphPropertiesError:
            self.db.create_graph(
                'users-following',
                [{
                    'edge_collection': 'Following',
                    'from_vertex_collections': ['User'],
                    'to_vertex_collections': ['User'],
                }],
            )

