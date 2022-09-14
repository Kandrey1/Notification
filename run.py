from app import create_app
from config import Config
from app.models import db
from app.blueprint_api import api_bp


app = create_app(Config)

app.register_blueprint(api_bp, url_prefix='/api')


@app.before_first_request
def create_table():
    db.create_all()


@app.route("/health_check", methods=['GET'])
def health_check():
    """ Страница для проверки работоспособности сервиса """
    return "Service work"


if __name__ == '__main__':
    app.run(host='0.0.0.0')
