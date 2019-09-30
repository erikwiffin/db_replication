from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from db_replication.lib.arango import ArangoExtension
from db_replication.lib.elasticsearch import ElasticsearchExtension


arango = ArangoExtension()
db = SQLAlchemy()
es = ElasticsearchExtension()
login_manager = LoginManager()
login_manager.login_view = "main.login"
