# coding=utf-8

import flask
import os

from services.notification import Notification, NotificationList, NotificationActiveList
from services.alert import Alert, AlertList
from dashboard import DashBoard
from flask_restful import Api

server = flask.Flask(__name__)

server.config['DEBUG'] = True

server.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
server.secret_key = '3b4be1bd-c8a8-466d-bffd-9ac2a2de6c8c'


@server.route('/')
def index():
    return 'Hi'


api = Api(server)
api.add_resource(Notification, '/notification/<string:imei>')
api.add_resource(Alert, '/alert/<string:imei>')
api.add_resource(NotificationList, '/notifications')
api.add_resource(NotificationActiveList, '/actives')
api.add_resource(AlertList, '/alerts')

ute_dashboard = DashBoard(server)

if __name__ == '__main__':
    from db import db
    db.init_app(server)

    if server.config['DEBUG']:
        @server.before_first_request
        def create_tables():
            db.create_all()

    server.run(debug=True ,port=5000)



