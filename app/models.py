import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


ma = Marshmallow()
db = SQLAlchemy()


class Mailing(db.Model):
    """ Таблица рассылка """
    __tablename__ = 'mailing'

    id = db.Column(db.Integer, primary_key=True)
    start_send = db.Column(db.DateTime)
    end_send = db.Column(db.DateTime)
    text = db.Column(db.String(250), nullable=False)
    filter_client = db.Column(db.String(200), nullable=False)

    def __init__(self, start_send, end_send, text, filter_client):
        self.start_send = start_send
        self.end_send = end_send
        self.text = text
        self.filter_client = filter_client

    def __repr__(self):
        return f"<{self.id} - {self.start_send} - {self.text}>"


class Client(db.Model):
    """ Таблица клиент """
    __tablename__ = 'client'

    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(11), nullable=False, unique=True)
    code_phone = db.Column(db.String(3), nullable=False)
    email = db.Column(db.String(250), unique=True)
    tag = db.Column(db.String(250))
    # todo time_zone

    def _get_code_phone(self) -> str:
        """ Возвращает код оператора из номера телефона """
        return self.phone[1:4]

    def __init__(self, phone, email, tag):
        self.phone = phone
        self.code_phone = self._get_code_phone()
        self.email = email
        self.tag = tag

    def __repr__(self):
        return f"<{self.id} - {self.phone} - {self.tag}>"


class Message(db.Model):
    """ Таблица сообщение """
    __tablename__ = 'message'

    id = db.Column(db.Integer, primary_key=True)
    create = db.Column(db.DateTime, default=datetime.datetime.today())
    status = db.Column(db.Boolean, default=False)
    mailing_id = db.Column(db.Integer, db.ForeignKey('mailing.id'),
                           nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'),
                          nullable=False)

    def __init__(self, status, mailing_id, client_id):
        self.status = status
        self.mailing_id = mailing_id
        self.client_id = client_id

    def __repr__(self):
        return f"<{self.id} - {self.mailing_id} - {self.client_id}>"


class ClientSchema(ma.Schema):
    class Meta:
        model = Client
        fields = ('id', 'phone', 'code_phone', 'email', 'tag')


class MessageSchema(ma.Schema):
    class Meta:
        model = Message
        fields = ('id', 'status', 'mailing_id', 'client_id')


class MailingSchema(ma.Schema):
    class Meta:
        model = Mailing
        fields = ('id', 'start_send', 'end_send', 'text', 'filter_client')
