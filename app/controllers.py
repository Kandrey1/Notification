from flask_restful import Resource


class ClientController(Resource):
    """ Класс для действия над сущностью клиента """
    def get(self):
        return {}, 200


class MailingController(Resource):
    """ Класс для действия над сущностью рассылка """
    def get(self):
        return {}, 200


class MessageController(Resource):
    """ Класс для действия над сущностью сообщения """
    def get(self):
        return {}, 200
