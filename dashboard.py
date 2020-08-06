from views.components import generate_notification_table, get_antel_logo, get_ute_logo, get_mini_container,generate_interval_input
from views.components import generate_graph, generate_alert_table
from utils import split_filter_part
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

        self.app = dash.Dash(
            __name__,
            server=server,
            routes_pathname_prefix='/monitor/',
            external_stylesheets=external_stylesheets
        )

        self.app.layout = html.Div([
            dcc.Store(id="aggregate_data"),
            html.Div(id="output-clientside"),
            html.Div([
                html.Div([
                    get_antel_logo(self.app),
                    get_ute_logo(self.app)
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
                                    "Modems", style={"margin-top": "0px"}
                                ),
                            ]
                        )
                    ],
                    className="one-half column",
                    id="title",
                ),
                dcc.Interval(
                    id='interval-component',
                    interval=30 * 1000,  # in milliseconds
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
                        generate_interval_input(),
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

        # Tables update
        @self.app.callback(Output('notifications', 'data'),
                         [Input('notifications','page_current'),Input('notifications','page_size'),Input('notifications','filter_query')])
        def update_table_notifications(page_current,page_size,filter_query):
            criteria = {}
            if filter_query:
                filtering_expressions = filter_query.split(' && ')
                for filter_part in filtering_expressions:
                    col_name, operator, filter_value = split_filter_part(filter_part)
                    criteria.update({col_name: filter_value})
            return [x.json() for x in self.notification_controller.get_all_notifications(page_current,page_size,criteria)]

        @self.app.callback(Output('alerts', 'data'),
                           [Input('alerts','page_current'),Input('alerts','page_size')])
        def update_table_alert(page_current, page_size):
            return [x.json() for x in self.alert_controller.get_all_alerts(page_current, page_size)]

        # Data Notification Update
        @self.app.callback(Output('total_notifications_text', 'children'), [Input('interval-component', 'n_intervals'),Input('time_filter', 'value')])
        def update_notification_data(n,value):
            days, hour, minutes = (30, 0, 0) if value == 'm' else (7, 0, 0) if value == 'd' else (1, 0, 0)
            return self.notification_controller.get_count_notifications_by_perdiod(days, hour, minutes)

        @self.app.callback(Output('alert_text', 'children'),  [Input('interval-component', 'n_intervals'),Input('time_filter', 'value')])
        def update_alert_total(n,value):
            days, hour, minutes = (30, 0, 0) if value == 'm' else (7, 0, 0) if value == 'd' else (1, 0, 0)
            return self.alert_controller.get_count_alert_by_perdiod(days, hour, minutes)

        @self.app.callback([Output('actives_text', 'children'),Output('down_meter_text', 'children'),Output('total_imei_reports_text', 'children')],
                           [Input('interval-component', 'n_intervals'), Input('time_filter', 'value')])
        def update_actives_total(n,value):
            days, hour, minutes = (30, 0, 0) if value == 'm' else (7, 0, 0) if value == 'd' else (1, 0, 0)
            active_count = self.notification_controller.get_count_active_meter_list(days, hour, minutes)
            total_count =  self.notification_controller.get_count_distinct_imei_notification()
            return active_count, total_count - active_count, total_count

        # Charts Update
        @self.app.callback(Output('main_graph', 'figure'), [Input('interval-component', 'n_intervals'),Input('time_filter', 'value')])
        def update_graph(n,value):
            days, hour, minutes = (30, 0, 0) if value == 'm' else (7, 0, 0) if value == 'd' else (1, 0, 0)
            data = self.notification_controller.get_init_active_graph(days, hour, minutes,value)
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
                    'title': 'Notificaciones de modems'
                }
            }

        @self.app.callback(Output('charts_errors', 'figure'), [Input('interval-component', 'n_intervals'),Input('time_filter', 'value')])
        def update_total_errors(n,value):
            days, hour, minutes = (30, 0, 0) if value == 'm' else (7, 0, 0) if value == 'd' else (1, 0, 0)
            alert_list = self.alert_controller.get_alert_list(days, hour, minutes)
            data = Counter([x[1] for x in alert_list])
            total_notification = self.notification_controller.get_count_active_meter_list(days, hour, minutes)
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

