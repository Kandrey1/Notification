import datetime
import pytest
from sqlalchemy.exc import IntegrityError

from ..app.models import db, Client, Mailing, Message


def test_db_client(app_test, create_client_one):
    """Тестирование таблицы 'сlient' в БД."""
    with app_test.app_context():
        row = create_client_one

        db.session.add(row)
        db.session.commit()

    client = Client.query.first()

    assert client.email == 'client1@client'
    assert client.tag == 'tag1'

    with pytest.raises(IntegrityError):
        client_err_1 = Client(email='client1@client', tag='tag1')
        client_err_2 = Client(email=None, tag='tag1')

        db.session.add(client_err_1)
        db.session.add(client_err_2)
        db.session.commit()


def test_db_mailing(app_test, create_mailing_one):
    """Тестирование таблицы 'mailing' в БД."""
    with app_test.app_context():
        row = create_mailing_one

        db.session.add(row)
        db.session.commit()

    mail = Mailing.query.first()

    assert mail.start_send == datetime.datetime(2020, 1, 1, 12, 00)
    assert mail.end_send == datetime.datetime(2021, 11, 11, 23, 30)
    assert mail.text == "message one"
    assert mail.filter_client == "filter one"

    with pytest.raises(IntegrityError):
        mail_err_1 = Mailing(start_send=None,
                             end_send=None,
                             text=None,
                             filter_client=None)
        mail_err_2 = Mailing(start_send="error date",
                             end_send="error date",
                             text="message one",
                             filter_client="filter one")

        db.session.add(mail_err_1)
        db.session.add(mail_err_2)
        db.session.commit()


def test_db_message(app_test, create_message_one):
    """Тестирование таблицы 'message' в БД."""
    with app_test.app_context():
        row = create_message_one

        db.session.add(row)
        db.session.commit()

    message = Message.query.first()

    assert message.status == 0
    assert message.mailing_id == 2
    assert message.client_id == 2

    with pytest.raises(IntegrityError):
        message_err_1 = Message(status=None,
                                mailing_id=None,
                                client_id=None)

        db.session.add(message_err_1)
        db.session.commit()
