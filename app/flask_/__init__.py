from flask import Flask
from sqlalchemy.exc import OperationalError

from app.flask_.config import flask_config, imp_config
from app.flask_.extensions import imp, db
from app.flask_.first_run import first_run
from app.flask_.models import System


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
        try:

            system = System.get_system()
            if system is None:
                first_run(imp)

        except OperationalError:
            db.create_all()
            first_run(imp)

    return app
