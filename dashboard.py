
from views.components import generate_table,get_antel_logo,get_ute_logo,get_mini_container
import dash_html_components as html
import dash_core_components as dcc
import dash
from dash.dependencies import Input, Output
from controlers.notification import NotificationControler


class DashBoard(object):

    def __init__(self,server):
        external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

        app = dash.Dash(
            __name__,
            server=server,
            routes_pathname_prefix='/dash/',external_stylesheets=external_stylesheets
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
                            [dcc.Graph(id="main_graph")],
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

        @app.callback(Output('notifications', 'data'), [Input('interval-component', 'n_intervals')])
        def update_table(n):
            print("ACTUALIZO")
            return [x.json() for x in NotificationControler.get_all_notifications()]

        @app.callback(Output('total_notifications', 'children'), [Input('interval-component', 'n_intervals')])
        def update_table(n):
            return "1045"


