from flask import request
from flask_restful import Resource
from .utils import Database, get_date_from_str, get_number_clients_mailing
from .models import Client, Mailing
from .tasks import start_mailing


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
        """Удаление клиента из БД.
           Данные передаются в json {"id_delete":}
               id_delete: int - id клиента которого надо удалить.
        """
        try:
            data_json = request.get_json()
            Database().dell(table=Client, id_delete=data_json.get("id_delete"))

        except Exception as e:
            return f'{e}', 400

        return 200


class ClientUpdateController(Resource):
    """Обновления данных клиента."""
    def put(self, id_update):
        """Обновления данных атрибутов клиента.
            :param id_update -- id клиента данные которого нужно обновить.
            :type id_update: int
                Данные передаются в json {"up_email":, "up_tag":}
                    up_email: str - почта клиента.
                    up_tag: str - произвольная метка(описание) клиента.
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
    """Добавления новой рассылки и удаления существующей из БД."""
    def post(self):
        """Добавления новой рассылки в БД со всеми ее атрибутами.
            Данные передаются в json
            {"start_send":, "end_send":, "text":, "filter_client"}
            start_send: str - дата и время запуска рассылки в
                              формате '%Y-%m-%d %H:%M'.
            end_send: str - дата и время окончания рассылки
                            формате '%Y-%m-%d %H:%M'.
            text: str - текст сообщения для доставки клиенту.
            filter_client: str - фильтр свойств клиентов (определяет
                            отправлять или нет сообщение).
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
        """Удаление рассылки из БД.
            Данные передаются в json {"id_delete":}
            id_delete: int - id рассылки которую нужно удалить.
        """
        try:
            data_json = request.get_json()
            Database().dell(table=Mailing, id_delete=data_json.get("id_delete"))

        except Exception as e:
            return f'{e}', 400

        return 200


class MailingUpdateController(Resource):
    """Обновления данных рассылки."""
    def put(self, id_update):
        """ Обновления данных атрибутов рассылки.
            :param id_update -- id рассылки данные которой нужно обновить.
            :type id_update: int
                Данные передаются в json
                {"up_start_send":, "up_end_send":, "up_text":,
                 "up_filter_client"}
                up_start_send: str - дата и время запуска рассылки в
                                  формате '%Y-%m-%d %H:%M'.
                up_end_send: str - дата и время окончания рассылки
                                формате '%Y-%m-%d %H:%M'.
                up_text: str - текст сообщения для доставки клиенту.
                up_filter_client: str - фильтр свойств клиентов (определяет
                                отправлять или нет сообщение).
        """
        try:
            data_json = request.get_json()

            data_update = {"start_send": data_json.get("up_start_send"),
                           "end_send": data_json.get("up_end_send"),
                           "text": data_json.get("up_text"),
                           "filter_client": data_json.get("up_filter_client")}

            Database().update_mailing(id_update=id_update,
                                      data_request=data_update)

        except Exception as e:
            return f'{e}', 400
        return 201


class MailingStartController(Resource):
    """Запускает рассылку."""
    def post(self, id_mailing: int):
        """Запускает рассылку используя задачи celery.
           :param id_mailing -- id рассылки которую необходимо запустить.
           :type id_mailing: int
           Возвращает количество клиентов в рассылке.
        """
        try:
            number = get_number_clients_mailing(mailing_id=id_mailing)

            start_mailing.delay(mailing_id=id_mailing)

        except Exception as e:
            return f'{e}', 400

        return {f"Клиентов в рассылке id={id_mailing}": number}, 200
