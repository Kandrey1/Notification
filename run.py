from app import create_app
from config import Config


app = create_app(Config)


@app.route("/health_check", methods=['GET'])
def health_check():
    """ Страница для проверки работоспособности сервиса """
    return "Service work"


if __name__ == '__main__':
    app.run(host='0.0.0.0')
