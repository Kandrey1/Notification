from celery import Celery
from app import create_app
from config import Config


def create_celery():
    app = create_app(Config)

    celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'],
                    backend=app.config['CELERY_RESULT_BACKEND'])
    celery.conf.update(app.config)

    return celery
