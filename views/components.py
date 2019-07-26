import dash_table
from controlers.notification import NotificationController
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go



def generate_table():

    return dash_table.DataTable(
                id='notifications',
                columns=[{"name": i, "id": i} for i in NotificationController.get_atributes_list()],
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
            [html.H6(id="total_notifications_text"), html.P("Notificaciones")],
            id="total_notifications",
            className="mini_container",
        ),
        html.Div(
            [html.H6(id="alert_text"), html.P("Alertas")],
            id="alert",
            className="mini_container",
        ),
        html.Div(
            [html.H6(id="actives_text"), html.P("Activos")],
            id="actives",
            className="mini_container",
        ),
        html.Div(
            [html.H6(id="down_meter_text"), html.P("Sin respuesta")],
            id="down_meter",
            className="mini_container",
        ),
        html.Div(
            [html.H6(id="list_errors_text"), html.P("Errores")],
            id="list_errors",
            className="mini_container",
        ),
    ]



def generate_graph():
    return [
        dcc.Graph(id="main_graph",
                  figure={
                      'data': [go.Scatter(
                                x=[],
                                y=[],
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