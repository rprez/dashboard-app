from views.components import generate_table, get_antel_logo, get_ute_logo, get_mini_container, generate_graph
import dash_html_components as html
import dash_core_components as dcc
import dash
from dash.dependencies import Input, Output
from controlers.notification import NotificationController
from controlers.alert import AlertController
from datetime import datetime, timedelta
import plotly.graph_objs as go

class DashBoard(object):

    def __init__(self, server):
        self.notification_controller = NotificationController()
        self.alert_controller = AlertController()

        external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

        app = dash.Dash(
            __name__,
            server=server,
            routes_pathname_prefix='/dash/', external_stylesheets=external_stylesheets
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
                    interval=1 * 1000,  # in milliseconds
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
                        html.Div(
                            generate_graph(),
                            className="pretty_container twelve columns",
                        ),
                        html.Div(
                            generate_table(),
                            className="pretty_container twelve columns"
                        ),

                    ],
                    id="right-column",
                    className="twelve columns",
                ),
            ],
                className="row flex-display",
            ),
        ],
            id="mainContainer",
            style={"display": "flex", "flex-direction": "column"},
        )


        @app.callback(Output('main_graph', 'figure'), [Input('interval-component', 'n_intervals')])
        def update_graph(n):
            notifications = self.notification_controller.get_active_meter_list(30, 00, 00)
            return {
                      'data': [go.Scatter(
                                x= [datetime.now() - timedelta(days=x) for x in range(30)],
                                y=[self.notification_controller.get_init_active_graph(30, 00,00)],
                                text="TEXTO",
                                mode='lines+markers',
                                marker={
                                'size': 15,
                                'opacity': 0.5,
                                'line': {'width': 0.5, 'color': 'white'}
                            }
                         )
                      ],
                      'layout': {
                          'clickmode': 'event+select'
                      }
                    }


        @app.callback(Output('notifications', 'data'), [Input('interval-component', 'n_intervals')])
        def update_table(n):
            return [x.json() for x in self.notification_controller.get_all_notifications()]

        @app.callback(Output('total_notifications_text', 'children'), [Input('interval-component', 'n_intervals')])
        def update_notification_total(n):
            return self.notification_controller.get_count_all_notifications()

        @app.callback(Output('alert_text', 'children'), [Input('interval-component', 'n_intervals')])
        def update_alert_total(n):
            return self.alert_controller.get_count_all_alert()

        @app.callback(Output('actives_text', 'children'), [Input('interval-component', 'n_intervals')])
        def update_actives_total(n):
            return self.notification_controller.get_count_active_meter_list(0, 1, 00)

        @app.callback(Output('down_meter_text', 'children'), [Input('interval-component', 'n_intervals')])
        def update_total_down_meter(n):
            return self.notification_controller.get_count_down_meter(0, 1, 00)

        @app.callback(Output('list_errors_text', 'children'), [Input('interval-component', 'n_intervals')])
        def update_total_errors(n):
            return self.alert_controller.get_count_all_alert()
