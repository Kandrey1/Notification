import datetime
import pytest
from sqlalchemy.exc import IntegrityError
from ..app.models import db, Client, Mailing, Message
from ..app.utils import Database


def test_database_save(app_test, create_client_one):
    """Сохранение записи в БД"""
    row = create_client_one

    Database.save(row)

    client = Client.query.first()

    assert client.email == 'client1@client'
    assert client.tag == 'tag1'

    with pytest.raises(IntegrityError):
        client_err_1 = Client(email='client1@client', tag='tag1')
        client_err_2 = Client(email=None, tag='tag1')

        mail_err_1 = Mailing(start_send=None,
                             end_send=None,
                             text=None,
                             filter_client=None)
        mail_err_2 = Mailing(start_send="error date",
                             end_send="error date",
                             text="message one",
                             filter_client="filter one")

        message_err_1 = Message(status=None,
                                mailing_id=None,
                                client_id=None)

        db.session.add_all([client_err_1, client_err_2, mail_err_1,
                            mail_err_2, message_err_1])
        db.session.commit()


def test_database_dell(app_test, create_client_one, create_client_two):
    """Удаление записи из БД"""
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


def test_database_update_client(app_test, create_client_one):
    """ Обновление данных клиента в БД """
    client = create_client_one
    data_update = {"email": "client_up@client", "tag": "td_up"}

    db.session.add(client)
    db.session.commit()

    assert client.email == 'client1@client'

    Database().update_client(id_update=1, data_request=data_update)

    assert client.email == 'client_up@client'
    assert client.tag == 'td_up'


def test_database_update_mailing(app_test, create_mailing_one):
    """ Обновление данных клиента в БД """
    mail = create_mailing_one
    data_update = {"start_send": "2022-12-15 14:30",
                   "end_send": "2023-03-05 22:30",
                   "text": "message up",
                   "filter_client": "filter up"}

    db.session.add(mail)
    db.session.commit()

    assert Mailing.query.first().text == "message one"

    Database().update_mailing(id_update=1, data_request=data_update)

    mail = Mailing.query.first()

    assert mail.start_send == datetime.datetime(2022, 12, 15, 14, 30)
    assert mail.end_send == datetime.datetime(2023, 3, 5, 22, 30)
    assert mail.text == "message up"
    assert mail.filter_client == "filter up"
