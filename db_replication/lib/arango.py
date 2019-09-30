from arango import ArangoClient
from furl import furl


class ArangoExtension(object):
    def __init__(self, app=None):
        self.client = None
        self.db = None
        if app:
            self.init_app(app)

    def init_app(self, app):
        url = furl(app.config['ARANGODB_DATABASE_URI'])

        host = furl(scheme=url.scheme, host=url.host, port=url.port)
        self.client = ArangoClient(hosts=host.url)
        self.db = self.client.db(name=url.path, username=url.username, password=url.password)