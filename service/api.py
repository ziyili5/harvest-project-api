from flask import Flask, g
from flask_cors import CORS
from flask_restful import Api
from models import Base
from resources import postgresql
from config import ProdConfig

import logging

from resources import UserResource, UserFieldResource, CLUResource


def create_app(config_model=ProdConfig):
    app = Flask(__name__)
    CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": config_model.HARVEST_HOST}})
    configure_views(app)

    @app.teardown_appcontext
    def close_db(error):
        """Closes the database again at the end of the request."""
        if hasattr(g, 'psycopg_db'):
            g.psycopg_db.close()

    app.config.from_object(config_model)

    postgresql.init_app(app)

    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

    @app.before_first_request
    def setup():
        # Recreate database each time for demo
        # Base.metadata.drop_all(bind=postgresql.engine)
        Base.metadata.create_all(bind=postgresql.engine)

    return app


def configure_views(app):
    api = Api(prefix="/api")
    api.add_resource(CLUResource, '/CLUs', '/CLUs/<int:clu_id>')
    api.add_resource(UserFieldResource, '/userfield')
    api.add_resource(UserResource, '/users')
    api.init_app(app)


if __name__ == "__main__":
    app = create_app(ProdConfig)
    app.run()
