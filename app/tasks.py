import datetime
import random
import time
from celery.exceptions import MaxRetriesExceededError
from app.models import db, Mailing, Client, Message
from app.utils import Database, get_id_filtered_client
from celeryd import create_celery

celery = create_celery()


@celery.task(bind=True, max_retries=3, soft_time_limit=180, time_limit=200)
def start_mailing(self, mailing_id: int) -> int:
    """Запускает рассылку сообщений.
        :param mailing_id -- id рассылки которую необходимо запустить.
        :type mailing_id: int
        Возвращает количество клиентов которым надо сделать рассылку.
    """
    from run import app
    with app.app_context():
        mailing_start = Mailing.query.get(mailing_id)

        clients_id = get_id_filtered_client(
            filter_client=mailing_start.filter_client)

    time_start = datetime.datetime.now() - datetime.timedelta(hours=3) + \
                 datetime.timedelta(seconds=10)

    for client_id in clients_id:
        send_message_client.apply_async((client_id, mailing_start.id),
                                        eta=time_start)

    return len(clients_id)


@celery.task(bind=True, max_retries=2, soft_time_limit=20, time_limit=30)
def send_message_client(self, client_id: int, mailing_id: int) -> bool:
    """Отправляет сообщение клиенту.
        :param client_id -- id клиента в БД, которому отправить сообщение.
        :type client_id: int
        :param mailing_id -- id рассылки, в которой отправляется сообщение.
        :type mailing_id: int
        :return Статус успешности отправки. True сообщение доставлено,
                False сообщение не доставлено.
        :rtype int
    """
    from run import app
    try:
        with app.app_context():
            client = Client.query.get(client_id)
            mailing = Mailing.query.get(mailing_id)

        # Отправка сообщение на почту. Ответ статус доставки True, False
        status_message = function_send_email_client(client_email=client.email,
                                                    message=mailing.text)

        with app.app_context():
            # Получение объекта была ли такая отправка (рассылка, клиент)
            msg = Message.query.filter(Message.mailing_id == mailing_id,
                                       Message.client_id == client_id).first()

            # Сохранение в БД в таблицу Message, если отправки раньше не было
            if not msg:
                message = Message(status=status_message,
                                  mailing_id=mailing_id,
                                  client_id=client_id)
                Database.save(message)
            else:
                msg.status = status_message
                db.session.commit()

        assert status_message

    except AssertionError:
        try:
            raise self.retry(countdown=3)
        except MaxRetriesExceededError:
            raise Exception("Было выполнено максимум повторов")

    return status_message


# Функция имитирует работу функции по отправке сообщения.
def function_send_email_client(client_email: str, message: str) -> bool:
    """Отправляет сообщение клиенту. Возвращает статут отправки.
        :param client_email -- почта клиента на которую требуется
                               отправить сообщение.
        :type client_email: str
        :param message -- текст сообщения которое отправить клиенту.
        :type message: str
        :return Статус успешности отправки. True сообщение доставлено,
                False сообщение не доставлено.
        :rtype bool
    """
    # пока ответ имитируется с помощью random
    rand = random.randint(1, 100)
    time.sleep(random.randint(0, 5))
    status_send = False if 20 < rand < 100 else True
    return status_send
