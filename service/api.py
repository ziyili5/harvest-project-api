import logging
from pathlib import Path

from db import db
from db import init_db_command
from fixtures import fixtures_command
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from resources import CLUResource
from resources import UserFieldResource
from resources import UserResource


def create_app():
    app = Flask(__name__, instance_path=Path("./").resolve())
    app.config.from_pyfile("config.py")

    CORS(
        app,
        supports_credentials=True,
        resources={r"/api/*": {"origins": app.config.get("HARVEST_HOST", ["*"])}},
    )
    configure_views(app)

    db.init_app(app)
    app.cli.add_command(init_db_command)
    app.cli.add_command(fixtures_command)

    # Logging
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

    return app


def configure_views(app):
    api = Api(prefix="/api")
    api.add_resource(CLUResource, "/CLUs", "/CLUs/<int:clu_id>")
    api.add_resource(UserFieldResource, "/user-field")
    api.add_resource(UserResource, "/users")
    api.init_app(app)
