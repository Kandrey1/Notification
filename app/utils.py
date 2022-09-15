from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound
from sqlalchemy import delete
from .models import db, Client


def format_error_db(error: IntegrityError) -> str:
    """ Возвращает название колонки из БД, в которой произошла ошибка
        уникальности имени при записи. Разбивает ошибку и возвращает
        последнее слово.
    """
    return str(error.orig).split('.')[-1]


class Database:
    """ Методы для работы с БД """
    @staticmethod
    def save(new_row: object) -> None:
        """ Сохраняет запись в БД. При неудаче возвращает ошибку.
            :param
                new_row - объект(db.model) для сохранения в БД.
        """
        try:

            db.session.add(new_row)
            db.session.commit()

        except IntegrityError as e:
            db.session.rollback()
            error_arg = format_error_db(e)
            raise Exception(f"Такой {error_arg} уже существует")

        except Exception as ex:
            db.session.rollback()
            raise Exception(f"Ошибка при сохранении в БД")

    @staticmethod
    def update_client(id_update: int, data_request: dict) -> None:
        """ Обновляет данные записи клиента в БД.
            :param
                data_request - json данные в запросе
                {"email": , "tag": }
        """
        try:
            client = Client.query.get_or_404(id_update)

            for key, val in data_request.items():
                if key == 'phone' and val is not None:
                    client.phone = val
                if key == 'email' and val is not None:
                    client.email = val
                if key == 'tag' and val is not None:
                    client.tag = val

            db.session.commit()

        except NotFound as e:
            db.session.rollback()
            raise Exception(f"Клиента нет в БД")

        except Exception as ex:
            db.session.rollback()
            raise Exception(f"Ошибка при обновлении записи в БД {ex}")

    @staticmethod
    def dell(table: object, id_delete: int) -> None:
        """ Удаляет запись из БД.
            :param
                table - таблица из которой требуется удалить запись.
                id_delete - id записи, которую требуется удалить.
        """
        try:
            db.session.execute(delete(table).where(table.id == id_delete))
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            raise Exception(f"Ошибка при удалении записи из БД")
