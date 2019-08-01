from views.components import generate_notification_table, get_antel_logo, get_ute_logo, get_mini_container
from views.components import generate_graph, generate_alert_table
import dash_html_components as html
import dash_core_components as dcc
import dash
from dash.dependencies import Input, Output
from controlers.notification import NotificationController
from controlers.alert import AlertController
from collections import Counter
import plotly.graph_objs as go


class DashBoard(object):

    def __init__(self, server):
        self.notification_controller = NotificationController()
        self.alert_controller = AlertController()

        external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

        app = dash.Dash(
            __name__,
            server=server,
            routes_pathname_prefix='/monitor/', external_stylesheets=external_stylesheets
        )

        app.layout = html.Div([
            dcc.Store(id="aggregate_data"),
            html.Div(id="output-clientside"),
            html.Div([
                html.Div([
                    get_antel_logo(app),
                    get_ute_logo(app)
                ],
                    className="one-third column",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    "Dashboard",
                                    style={"margin-bottom": "0px"},
                                ),
                                html.H5(
                                    "Monitoreo medidores", style={"margin-top": "0px"}
                                ),
                            ]
                        )
                    ],
                    className="one-half column",
                    id="title",
                ),
                dcc.Interval(
                    id='interval-component',
                    interval=10 * 1000,  # in milliseconds
                    n_intervals=0
                )
            ],
                id="header",
                className="row flex-display",
                style={"margin-bottom": "25px"},
            ),

            html.Div([
                html.Div(
                    [
                        html.Div(
                            get_mini_container(),
                            id="info-container",
                            className="row container-display",
                        ),
                        html.Div([
                            html.Div(
                                generate_graph(),
                                id="main_graph_container",
                                className="pretty_container eight columns",
                            ),
                            html.Div(
                                [dcc.Graph(id="charts_errors")],
                                id="list_errors",
                                className="pretty_container four columns",
                            ),
                        ],
                            className="row flex-display",
                        ),
                        html.Div([
                                        html.Div([
                                                html.H5(
                                                    "Notificaciones",
                                                    style={"text-align": "center", },
                                                ),
                                                generate_notification_table()
                                            ],
                                            className="pretty_container seven columns"
                                        ),
                                        html.Div([
                                            html.H5(
                                                "Alertas",
                                                style={"text-align": "center", },
                                            ),
                                            generate_alert_table()
                                        ],
                                            className="pretty_container five columns"
                                        ),
                        ],
                            className="row flex-display"
                        ),
                    ],
                 ),
            ],
            ),
        ],
            id="mainContainer",
            style={"display": "flex", "flex-direction": "column"},
        )

        @app.callback(Output('main_graph', 'figure'), [Input('interval-component', 'n_intervals')])
        def update_graph(n):
            data = self.notification_controller.get_init_active_graph(30, 00, 00)
            return {
                      'data': [go.Scatter(
                                x=list(data.keys()),
                                y=list(data.values()),
                                text="Notificaciones",
                                mode='lines+markers',
                                marker={
                                    'size': 15,
                                    'opacity': 0.5,
                                    'line': {'width': 0.5, 'color': 'white'}
                            }
                         )
                      ],
                      'layout': {
                          'clickmode': 'event+select',
                          'title':'Medidores que enviaron notificación'
                      }
                    }
        # Tables update
        @app.callback(Output('notifications', 'data'), [Input('interval-component', 'n_intervals')])
        def update_table_notifications(n):
            return [x.json() for x in self.notification_controller.get_all_notifications()]

        @app.callback(Output('alerts', 'data'), [Input('interval-component', 'n_intervals')])
        def update_table_alert(n):
            return [x.json() for x in self.alert_controller.get_all_alerts()]

        # Data Notification Update
        @app.callback(Output('total_notifications_text', 'children'), [Input('interval-component', 'n_intervals')])
        def update_notification_data(n):
            return self.notification_controller.get_count_notifications_by_perdiod(0, 1, 00)

        @app.callback(Output('alert_text', 'children'), [Input('interval-component', 'n_intervals')])
        def update_alert_total(n):
            return self.alert_controller.get_count_alert_by_perdiod(0, 1, 00)

        @app.callback([Output('actives_text', 'children'),Output('down_meter_text', 'children'),Output('total_imei_reports_text', 'children')], [Input('interval-component', 'n_intervals')])
        def update_actives_total(n):
            active_count = self.notification_controller.get_count_active_meter_list(0, 1, 00)
            total_count =  self.notification_controller.get_count_distinct_imei_notification()
            return active_count, total_count - active_count, total_count

        # Charts Update
        @app.callback(Output('charts_errors', 'figure'), [Input('interval-component', 'n_intervals')])
        def update_total_errors(n):
            alert_list = self.alert_controller.get_alert_list(0,1,0)
            data = Counter([x[1] for x in alert_list])
            total_notification = self.notification_controller.get_count_active_meter_list(0, 1, 0)
            data = [
                    dict(
                        type="pie",
                        labels=list(data.keys())+["Notificaciones"],
                        values=list(data.values())+[total_notification],
                        hoverinfo="text+value+percent",
                        textinfo="label+percent+name",
                        hole=0.5,
                    ),
                ]
            layout_pie = {}
            layout_pie["title"] = "Errores"
            layout_pie["font"] = dict(color="#777777")
            return dict(data=data, layout=layout_pie)

