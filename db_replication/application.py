import os

from flask import Flask


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

app.config['ARANGODB_DATABASE_URI'] = os.getenv('ARANGODB_DATABASE_URI')
app.config['ELASTICSEARCH_DATABASE_URI'] = os.getenv('ELASTICSEARCH_DATABASE_URI')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')


def create_app():
    from db_replication import (
        extensions,
        filters,
    )
    from db_replication.views.cli.views import BP as cli_blueprint
    from db_replication.views.main.views import BP as main_blueprint

    app.register_blueprint(cli_blueprint)
    app.register_blueprint(main_blueprint)

    extensions.arango.init_app(app)
    extensions.db.init_app(app)
    extensions.es.init_app(app)
    extensions.login_manager.init_app(app)

    import db_replication.models.document.listeners
    import db_replication.models.graph.listeners

    return app
