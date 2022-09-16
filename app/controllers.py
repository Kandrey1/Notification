from flask import request
from flask_restful import Resource
from .utils import Database, get_date_from_str
from .models import Client, Mailing


class ClientController(Resource):
    """Добавление нового клиента и удаление существующего из БД."""
    def post(self):
        """Добавляет нового клиента в БД со всеми его атрибутами.
           Данные передаются в json {"email":, "tag":}
               email: str -- почта клиента.
               tag: str -- произвольная метка(описание) клиента.

           :return Сообщение об успешности выполнения или ошибка.
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
                id_delete: int - id клиента которого надо удалить.
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
                up_email: str - почта клиента.
                up_tag: str - произвольная метка(описание) клиента.
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
    """ Класс для добавления новой рассылки и удаления существующей из БД """
    def post(self):
        """ Добавления новой рассылки в БД со всеми ее атрибутами.
            :param
                Данные передаются в json
                {"start_send":, "end_send":, "text":, "filter_client"}
                start_send: str - дата и время запуска рассылки в
                                  формате '%Y-%m-%d %H:%M'.
                end_send: str - дата и время окончания рассылки
                                формате '%Y-%m-%d %H:%M'.
                text: str - текст сообщения для доставки клиенту.
                filter_client: str - фильтр свойств клиентов (определяет
                                отправлять или нет сообщение).
            :return
                Сообщение об успешности выполнения или ошибка.
        """
        try:
            data_json = request.get_json()

            date_start = get_date_from_str(data_json.get("start_send"))
            date_end = get_date_from_str(data_json.get("end_send"))

            new_mailing = Mailing(start_send=date_start,
                                  end_send=date_end,
                                  text=data_json.get("text"),
                                  filter_client=data_json.get("filter_client"))

            Database().save(new_mailing)

        except Exception as e:
            return f'{e}', 400

        return 201

    def delete(self):
        """ Удаление рассылки из БД.
            :param
                Данные передаются в json {"id_delete":}
                id_delete: int - id рассылки которую нужно удалить.
            :return
                Сообщение об успешности выполнения или ошибка.
        """
        try:
            data_json = request.get_json()
            Database().dell(table=Mailing, id_delete=data_json.get("id_delete"))

        except Exception as e:
            return f'{e}', 400

        return 200


class MailingUpdateController(Resource):
    """ Класс для обновления данных рассылки  """
    def put(self, id_update):
        """ Обновления данных атрибутов клиента.
            :param
                Данные передаются в json {"up_email":, "up_tag":}
                up_email: str - почта клиента.
                up_tag: str - произвольная метка(описание) клиента.
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


class MessageController(Resource):
    """ Класс для действия над сущностью сообщения """
    pass
