import dash_html_components as html
import dash_core_components as dcc
import dash_table
import dash
from dash.dependencies import Input, Output
from controlers.notification import NotificationControler

from app import server

mi_app = dash.Dash(
    __name__,
    server=server,
    routes_pathname_prefix='/dash/'
)

mi_app.layout = html.Div(
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


@mi_app.callback(Output('notifications', 'data'), [Input('interval-component', 'n_intervals')])
def generate_table(n):
    print("ACTUALIZO")
    return [x.json() for x in NotificationControler.get_all_notifications()]