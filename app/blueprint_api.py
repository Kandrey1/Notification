from flask import Blueprint
from flask_restful import Api
from .controllers import ClientController, ClientUpdateController, \
    MailingController, MailingUpdateController, MailingStartController

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Route
api.add_resource(ClientController, '/client')
api.add_resource(ClientUpdateController, '/client/<int:id_update>')
api.add_resource(MailingController, '/mailing')
api.add_resource(MailingUpdateController, '/mailing/<int:id_update>')
api.add_resource(MailingStartController, '/mailing/start/<int:id_mailing>')
