from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from cqrs_app.lib.arango import ArangoExtension
from cqrs_app.lib.elasticsearch import ElasticsearchExtension


arango = ArangoExtension()
db = SQLAlchemy()
es = ElasticsearchExtension()
login_manager = LoginManager()
login_manager.login_view = "main.login"