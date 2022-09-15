from ..app.models import db, Client
from ..app.utils import Database


def test_db_client(app_test, create_client_one):
    """ Тестирование таблицы в БД 'Client' """
    with app_test.app_context():
        row = create_client_one

        db.session.add(row)
        db.session.commit()

    client = Client.query.first()

    assert client.email == 'client1@client'
    assert client.tag == 'tag1'


def test_db_utils_db_save(app_test, create_client_one):
    """ Сохранение записи в БД """
    row = create_client_one

    Database.save(row)

    client = Client.query.first()

    assert client.email == 'client1@client'
    assert client.tag == 'tag1'


def test_db_utils_db_dell(app_test, create_client_one, create_client_two):
    """ Удаление записи из БД """
    client1 = create_client_one
    client2 = create_client_two

    db.session.add_all([client1, client2])
    db.session.commit()

    assert Client.query.count() == 2

    Database.dell(table=Client, id_delete=1)

    assert Client.query.count() == 1

    client = Client.query.first()

    assert client.email == 'client2@client'
    assert client.tag == 'tag2'


def test_db_utils_update_client(app_test, create_client_one):
    """ Обновление данных клиента в БД """
    client = create_client_one
    data_update = {"email": "client_up@client", "tag": "td_up"}

    db.session.add(client)
    db.session.commit()

    assert client.email == 'client1@client'

    Database().update_client(id_update=1, data_request=data_update)

    assert client.email == 'client_up@client'
    assert client.tag == 'td_up'