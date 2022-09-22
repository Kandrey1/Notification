import datetime

import pytest
from ..config import ConfigTest
from ..app import create_app
from ..app.models import db, Client, Mailing, Message


@pytest.fixture
def app_test():
    app = create_app(config_class=ConfigTest)

    with app.app_context():
        db.create_all()

        yield app

        db.drop_all()


@pytest.fixture
def client_test(app_test):
    from ..app.blueprint_api import api_bp
    app_test.register_blueprint(api_bp, url_prefix='/api')
    return app_test.test_client()


# ------------------------------- Client ---------------------------------------
@pytest.fixture
def create_client_one():
    client = Client(email='client1@client',
                    tag='tag1')
    return client


@pytest.fixture
def create_client_two():
    client = Client(email='client2@client',
                    tag='tag2')
    return client


@pytest.fixture
def get_json_client_one():
    return {"email": "client1@client", "tag": "tag1"}


@pytest.fixture
def get_json_client_two():
    return {"email": "client2@client", "tag": "tag2"}


# ------------------------------- Client ---------------------------------------
# ------------------------------- Mailing --------------------------------------
@pytest.fixture
def create_mailing_one():
    date_start = datetime.datetime.strptime("2020-01-01 12:00",
                                            "%Y-%m-%d %H:%M")
    date_end = datetime.datetime.strptime("2021-11-11 23:30",
                                          "%Y-%m-%d %H:%M")

    mail = Mailing(start_send=date_start,
                   end_send=date_end,
                   text="message one",
                   filter_client="filter one")
    return mail


@pytest.fixture
def create_mailing_two():
    date_start = datetime.datetime.strptime("2021-11-02 10:30",
                                            "%Y-%m-%d %H:%M")
    date_end = datetime.datetime.strptime("2021-11-02 10:30",
                                          "%Y-%m-%d %H:%M")
    mail = Mailing(start_send=date_start,
                   end_send=date_end,
                   text="message two",
                   filter_client="filter two")
    return mail


@pytest.fixture
def get_json_mailing_one():

    data_json = {"start_send": "2022-11-02 10:30",
                 "end_send": "2022-11-05 11:30",
                 "text": "message one",
                 "filter_client": "filter one"}

    return data_json


@pytest.fixture
def get_json_mailing_two():

    data_json = {"start_send": "2021-11-02 10:30",
                 "end_send": "2021-11-05 11:30",
                 "text": "message two",
                 "filter_client": "filter two"}

    return data_json


# ------------------------------- Mailing --------------------------------------
# ------------------------------- Message --------------------------------------
@pytest.fixture
def create_message_one():
    message = Message(status=False,
                      mailing_id=1,
                      client_id=1)
    return message


@pytest.fixture
def create_message_one():
    message = Message(status=False,
                      mailing_id=2,
                      client_id=2)
    return message
# ------------------------------- Message --------------------------------------
