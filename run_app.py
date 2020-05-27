# coding=utf-8

import flask
import os

from services.notification import Notification, NotificationList, NotificationActiveList
from services.alert import Alert, AlertList
from dashboard import DashBoard
from flask_restful import Api
from db import db

server = flask.Flask(__name__)
server.config.from_object(os.environ['APP_SETTINGS'])

@server.route('/')
def index():
    return 'Go to /monitor/'

api = Api(server)
api.add_resource(Notification, '/notification/<string:imei>')
api.add_resource(Alert, '/alert/<string:imei>')
api.add_resource(NotificationList, '/notifications')
api.add_resource(NotificationActiveList, '/actives')
api.add_resource(AlertList, '/alerts')

db.init_app(server)
ute_dashboard = DashBoard(server)
server = ute_dashboard.app.server

if __name__ == '__main__':
    if server.config['DEBUG']:
        @server.before_first_request
        def create_tables():
            db.create_all()

    ute_dashboard.app.run_server(debug=True ,port=5000)



