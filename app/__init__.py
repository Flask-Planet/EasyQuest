from flask import Flask

from app.config import flask_config, imp_config
from app.extensions import imp, db
from app.first_run import first_run
from app.models import System


def create_app():
    app = Flask(__name__)
    flask_config.apply_config(app)

    imp.init_app(app, imp_config)
    imp.import_app_resources()

    imp.import_models("models")
    imp.import_blueprints("blueprints")

    db.init_app(app)

    with app.app_context():
        db.create_all()

        system = System.get_system()

        if system is None:
            first_run(imp)

    return app
