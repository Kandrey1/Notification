import pytest
from ..config import ConfigTest
from ..app import create_app
from ..app.models import db, Client


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
