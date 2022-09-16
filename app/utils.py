import datetime
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound
from sqlalchemy import delete
from .models import db, Client, Mailing


class FormattingExceptionSqlalchemy:
    """Форматирует ошибки IntegrityError SQLAlchemy.
       Возвращает текст ошибки в читаемом виде.
    """
    def __init__(self):
        self._exception = str

    def get_formatted(self, exception: IntegrityError) -> str:
        """Возвращает отформатированный текст ошибки."""
        self._exception = exception.orig
        self._create_data_exception()
        return self._case_redacted_error()

    def _create_data_exception(self) -> None:
        """Разбивает ошибку (объект IntegrityError) на две части и создает:
           self.type_error: str -- тип ошибки IntegrityError.
           self.param_error: str -- параметр ошибки (колонка таблицы).
        """
        self._list_error = self._exception.split('constraint failed:')
        self._type_error = self._list_error[0].strip()
        self._param_error = self._list_error[1].strip().split('.')[-1]

    def _case_redacted_error(self) -> str:
        """Возвращает значение из словаря варианта отредактированной ошибки."""
        self._format_error_dict = {
            "NOT NULL": f"Отсутствует параметр <{self._param_error}>",
            "UNIQUE": f"Такой параметр <{self._param_error}> уже существует"
        }
        return self._format_error_dict[self._type_error]


def get_date_from_str(date_time_str: str) -> object:
    """Преобразует дату date_time_str в формате строки в объект datetime.
       Дата в формате строки '%Y-%m-%d %H:%M' (прим. '2018-06-29 08:15')
    """
    return datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M')


class Database:
    """Методы для работы с БД."""
    @staticmethod
    def save(new_row: object) -> None:
        """Сохраняет запись в БД. При неудаче возвращает ошибку.
            :param new_row -- объект для сохранения в БД.
            :type экземпляр одного из классов таблиц БД.
        """
        try:
            db.session.add(new_row)
            db.session.commit()

        except IntegrityError as e:
            db.session.rollback()
            error = FormattingExceptionSqlalchemy().get_formatted(e)
            raise Exception(f"Ошибка сохранения в БД. {error}")

        # Отлавливание необрабатываемых(пока не найденных) исключений
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Ошибка. {e}")

    @staticmethod
    def dell(table: db.Model, id_delete: int) -> None:
        """Удаляет запись из БД.
            :param table -- таблица из которой требуется удалить запись.
            :type table: db.Model
            :param id_delete -- id записи, которую требуется удалить.
            :type  id_delete: int
        """
        try:
            if id_delete is None:
                raise Exception(f"Нет такой записи")

            db.session.execute(delete(table).where(table.id == id_delete))
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            raise Exception(f"Ошибка при удалении записи из БД")

    @staticmethod
    def update_client(id_update: int, data_request: dict) -> None:
        """Обновляет данные записи клиента в БД.
            :param id_update -- id записи для обновления.
            :type id_update: int
            :param data_request - json данные в запросе формата
                    {"email": , "tag": }
                    email: str - почта клиента.
                    tag: str - произвольная метка(описание) клиента.
            :type data_request: dict

        """
        try:
            client = Client.query.get_or_404(id_update)

            for key, val in data_request.items():
                if val is not None:
                    if key == 'phone':
                        client.phone = val
                    if key == 'email':
                        client.email = val
                    if key == 'tag':
                        client.tag = val

            db.session.commit()

        except NotFound as e:
            db.session.rollback()
            raise Exception(f"Клиента id={id_update} нет в БД")

        except Exception as ex:
            db.session.rollback()
            raise Exception(f"Ошибка при обновлении записи в БД {ex}")

    @staticmethod
    def update_mailing(id_update: int, data_request: dict) -> None:
        """Обновляет данные записи рассылки в БД.
            :param id_update -- id рассылки для обновления.
            :type id_update: int
            :param data_request - json данные в запросе формата
                {"start_send":, "end_send":, "text":, "filter_client"}
                start_send: str - дата и время запуска рассылки в
                                  формате '%Y-%m-%d %H:%M'.
                end_send: str - дата и время окончания рассылки
                                формате '%Y-%m-%d %H:%M'.
                text: str - текст сообщения для доставки клиенту.
                filter_client: str - фильтр свойств клиентов (определяет
                                     отправлять или нет сообщение).
            :type data_request: dict
        """
        try:
            mail = Mailing.query.get_or_404(id_update)

            for key, val in data_request.items():
                if val is not None:
                    if key == 'start_send':
                        mail.start_send = get_date_from_str(val)
                    if key == 'end_send':
                        mail.end_send = get_date_from_str(val)
                    if key == 'text':
                        mail.text = val
                    if key == 'filter_client':
                        mail.filter_client = val

            db.session.commit()

        except NotFound as e:
            db.session.rollback()
            raise Exception(f"Рассылки id={id_update} нет в БД")

        except Exception as ex:
            db.session.rollback()
            raise Exception(f"Ошибка при обновлении записи в БД {ex}")
