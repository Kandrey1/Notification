import datetime
from ..app.models import db, Client, Mailing


# ----------------- Client start -----------------------------------------------
def test_controllers_client_post(app_test, client_test, get_json_client_one):
    """ Добавление клиента """
    data = get_json_client_one

    response = client_test.post("/api/client", json=data)

    client = Client.query.first()

    assert response.status_code == 200
    assert client.email == "client1@client"
    assert client.tag == "tag1"


# def test_controllers_client_dell(client_test, app_test, create_client_one,
#                                  create_client_two):
#     """ Удаление клиента """
#     with app_test.app_context():
#         client1 = create_client_one
#         client2 = create_client_two
#
#         db.session.add(client1)
#         db.session.add(client2)
#         db.session.commit()
#
#         assert Client.query.count() == 2
#         assert Client.query.first().email == "client1@client"
#
#         data_dell = {"id_delete": 1}
#
#     response = client_test.delete("/api/client", json=data_dell)
#
#     assert response.status_code == 200
#     assert Client.query.count() == 1
#     assert Client.query.first().email == "client2@client"
#     assert Client.query.first().tag == "tag2"
#
#
# def test_controllers_client_update(client_test, app_test, create_client_one):
#     """ Обновление данных клиента """
#     data_update = {"up_email": "client_up@client",
#                    "up_tag": "tag_up"}
#
#     with app_test.app_context():
#         client = create_client_one
#         db.session.add(client)
#         db.session.commit()
#
#         assert Client.query.first().email == "client1@client"
#
#     response = client_test.put("/api/client/1", json=data_update)
#
#     assert response.status_code == 200
#     assert Client.query.first().email == "client_up@client"
#     assert Client.query.first().tag == "tag_up"
#
#
# # ----------------- Client end -------------------------------------------------
# # ----------------- Mailing start ----------------------------------------------
# def test_controllers_mailing_post(client_test, app_test, get_json_mailing_one):
#     """ Добавление рассылки """
#     data = get_json_mailing_one
#
#     response = client_test.post("/api/mailing", json=data)
#
#     with app_test.app_context():
#         mail = Mailing.query.first()
#
#     assert response.status_code == 200
#     assert mail.start_send == datetime.datetime(2022, 11, 2, 10, 30)
#     assert mail.end_send == datetime.datetime(2022, 11, 5, 11, 30)
#     assert mail.text == "message one"
#     assert mail.filter_client == "filter one"
#
#
# def test_controllers_mailing_dell(client_test, app_test, create_mailing_one,
#                                   create_mailing_two):
#     """ Удаление рассылки """
#     with app_test.app_context():
#         mail1 = create_mailing_one
#         mail2 = create_mailing_two
#
#         db.session.add(mail1)
#         db.session.add(mail2)
#         db.session.commit()
#
#         assert Mailing.query.count() == 2
#         assert Mailing.query.first().text == "message one"
#
#         data_dell = {"id_delete": 1}
#
#     response = client_test.delete("/api/mailing", json=data_dell)
#
#     mail = Mailing.query.first()
#
#     assert response.status_code == 200
#     assert Mailing.query.count() == 1
#     assert mail.start_send == datetime.datetime(2021, 11, 2, 10, 30)
#     assert mail.end_send == datetime.datetime(2021, 11, 2, 10, 30)
#     assert mail.text == "message two"
#     assert mail.filter_client == "filter two"
#
#
# def test_controllers_mailing_update(client_test, app_test, create_mailing_one):
#     """ Обновление данных клиента """
#     data_update = {"up_start_send": "3021-11-02 10:30",
#                    "up_end_send": "3021-11-05 11:30",
#                    "up_text": "message up",
#                    "up_filter_client": "filter up"}
#
#     with app_test.app_context():
#         mail = create_mailing_one
#         db.session.add(mail)
#         db.session.commit()
#
#         assert Mailing.query.first().text == "message one"
#
#     response = client_test.put("/api/mailing/1", json=data_update)
#
#     mail1 = Mailing.query.first()
#
#     assert response.status_code == 200
#     assert mail1.start_send == datetime.datetime(3021, 11, 2, 10, 30)
#     assert mail1.end_send == datetime.datetime(3021, 11, 5, 11, 30)
#     assert mail1.text == "message up"
#     assert mail1.filter_client == "filter up"
# # ----------------- Mailing end ------------------------------------------------
