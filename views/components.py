import dash_table
from controlers.notification import NotificationControler
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
import random
import datetime

def generate_table():

    return dash_table.DataTable(
                id='notifications',
                columns=[{"name": i, "id": i} for i in NotificationControler.get_atributes_list()],
                data=[]
    )


def get_antel_logo(app):
    return html.Img(
            src=app.get_asset_url("antel.png"),
            id="antel-image",
            style={
                "height": "60px",
                "width": "auto",
                "margin-bottom": "10px",
            },
    )


def get_ute_logo(app):
    return html.Img(
       src=app.get_asset_url("ute.png"),
        id="ute-image",
        style={
         "height": "30px",
         "width": "70px",
         "margin-bottom": "25px",
        },
    )

def get_mini_container():
    return [
        html.Div(
            [html.H6(id="total_notifications"), html.P("Notificaciones")],
            id="wells",
            className="mini_container",
        ),
        html.Div(
            [html.H6(id="alert_text"), html.P("Alertas")],
            id="gas",
            className="mini_container",
        ),
        html.Div(
            [html.H6(id="active_text"), html.P("Activos")],
            id="oil",
            className="mini_container",
        ),
        html.Div(
            [html.H6(id="without_signal"), html.P("Sin señal")],
            id="water",
            className="mini_container",
        ),
    ]

def generate_graph():
    return [
        dcc.Graph(id="main_graph",
                  figure={
                      'data': [go.Scatter(
                                x= [datetime.datetime.now() - datetime.timedelta(days=x) for x in range (100)],
                                y=[random.randrange(100) for x in range(100)],
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
                  )
    ]