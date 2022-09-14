from flask import Flask


def create_app(config_class):
    app = Flask(__name__)

    app.config.from_object(config_class)

    from .models import db
    db.init_app(app)

    from .models import Client, Message, Mailing

    return app
