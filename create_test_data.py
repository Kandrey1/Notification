import random
from app import create_app
from config import Config
from app.models import db, Client

app = create_app(config_class=Config)


def create_client_in_db(count_client: int = 100):
    """Создает клиентов в БД. По умолчанию 100 шт."""
    with app.app_context():
        for i in range(1, count_client + 1):
            f = random.randint(1, 10)
            client = Client(email=f'client{i}@client',
                            tag=f'filter{f}')

            db.session.add(client)

        db.session.commit()


if __name__ == '__main__':
    create_client_in_db(count_client=1000)
