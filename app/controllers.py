from flask import request
from flask_restful import Resource
from .utils import Database
from .models import Client


class ClientController(Resource):
    """ Класс для добавления нового клиента и удаления существующего из БД """
    def post(self):
        """ Добавления нового клиента в БД со всеми его атрибутами.
            :param
                Данные передаются в json {"email":, "tag":}
                email - почта клиента.
                tag - произвольная метка(описание) клиента.
            :return
                Сообщение об успешности выполнения или ошибка.
        """
        try:
            data_json = request.get_json()

            new_client = Client(email=data_json.get("email"),
                                tag=data_json.get("tag"))

            Database().save(new_client)

        except Exception as e:
            return f'{e}', 400

        return 201

    def delete(self):
        """ Удаление клиента из БД.
            :param
                Данные передаются в json {"id_delete":}
                id_delete - id клиента которого надо удалить.
            :return
                Сообщение об успешности выполнения или ошибка.
        """
        try:
            data_json = request.get_json()
            Database().dell(table=Client, id_delete=data_json.get("id_delete"))

        except Exception as e:
            return f'{e}', 400

        return 200


class ClientUpdateController(Resource):
    """ Класс для обновления данных клиента """
    def put(self, id_update):
        """ Обновления данных атрибутов клиента.
            :param
                Данные передаются в json {"up_email":, "up_tag":}
                up_email - почта клиента.
                up_tag - произвольная метка(описание) клиента.
            :return
                Сообщение об успешности выполнения или ошибка.

        """
        try:
            data_json = request.get_json()

            data_update = {"email": data_json.get("up_email"),
                           "tag": data_json.get("up_tag")}

            Database().update_client(id_update=id_update,
                                     data_request=data_update)

        except Exception as e:
            return f'{e}', 400
        return 201


class MailingController(Resource):
    """ Класс для действия над сущностью рассылка """
    pass


class MessageController(Resource):
    """ Класс для действия над сущностью сообщения """
    pass
