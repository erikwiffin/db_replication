from elasticsearch import Elasticsearch
from furl import furl


class ElasticsearchExtension(object):
    def __init__(self, app=None):
        self.client = None
        if app:
            self.init_app(app)

    def init_app(self, app):
        url = furl(app.config['ELASTICSEARCH_DATABASE_URI'])

        self.client = Elasticsearch(hosts=url.host, scheme=url.scheme, port=url.port)

    @property
    def index(self):
        return self.client.index

    @property
    def get(self):
        return self.client.get
    

