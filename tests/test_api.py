from ..app.models import db, Client


def test_controllers_client_post(client_test, app_test, get_json_client_one):
    data = get_json_client_one

    response = client_test.post("/api/client", json=data)

    with app_test.app_context():
        client = Client.query.first()

    assert response.status_code == 200
    assert client.email == "client1@client"
    assert client.tag == "tag1"


def test_controllers_client_dell(client_test, app_test, create_client_one,
                                 create_client_two):
    with app_test.app_context():
        client1 = create_client_one
        client2 = create_client_two

        db.session.add(client1)
        db.session.add(client2)
        db.session.commit()

        assert Client.query.count() == 2
        assert Client.query.first().email == "client1@client"

        data_dell = {"id_delete": 1}

    response = client_test.delete("/api/client", json=data_dell)

    assert response.status_code == 200
    assert Client.query.count() == 1
    assert Client.query.first().email == "client2@client"
    assert Client.query.first().tag == "tag2"


def test_controllers_client_update(client_test, app_test, create_client_one):
    data_update = {"up_email": "client_up@client",
                   "up_tag": "tag_up"}

    with app_test.app_context():
        client = create_client_one
        db.session.add(client)
        db.session.commit()

        assert Client.query.first().email == "client1@client"

    response = client_test.put("/api/client/1", json=data_update)

    assert response.status_code == 200
    assert Client.query.first().email == "client_up@client"
    assert Client.query.first().tag == "tag_up"


