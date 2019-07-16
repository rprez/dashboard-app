# coding=utf-8

import flask
from flask_restful import Api
import dash
import os

from services.notification import Notification, NotificationList
from services.alert import Alert, AlertList
import dash_html_components as html
import dash_core_components as dcc
import dash_table
from dash.dependencies import Input, Output
from controlers.notification import NotificationControler

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

server = flask.Flask(__name__)

server.config['DEBUG'] = True

server.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
server.secret_key = '3b4be1bd-c8a8-466d-bffd-9ac2a2de6c8c'


@server.route('/')
def index():
    return 'Hello Flask app'


app = dash.Dash(
    __name__,
    server=server,
    routes_pathname_prefix='/dash/'
)


api = Api(server)

api.add_resource(Notification, '/notification/<string:imei>')
api.add_resource(Alert, '/alert/<string:imei>')
api.add_resource(NotificationList, '/notifications')
api.add_resource(AlertList, '/alerts')

app.layout = html.Div(
        html.Div([
            html.H1(children="Dashboard"),
            html.Div(children='''
               Dashboard: Monitoreo de medidores.
           '''),
            dash_table.DataTable(
                id='notifications',
                columns=[{"name": i, "id": i} for i in NotificationControler.get_atributes_list()],
                data=[]
            ),
            dcc.Interval(
                id='interval-component',
                interval=1 * 1000,  # in milliseconds
                n_intervals=0
            )
        ])
    )


@app.callback(Output('notifications', 'data'), [Input('interval-component', 'n_intervals')])
def generate_table(n):
    print("ACTUALIZO")
    return [x.json() for x in NotificationControler.get_all_notifications()]

if __name__ == '__main__':
    from db import db
    db.init_app(server)

    if server.config['DEBUG']:
        @server.before_first_request
        def create_tables():
            db.create_all()

    server.run(debug=True ,port=5000)



