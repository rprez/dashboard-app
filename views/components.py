from dash_table import DataTable
from controlers.notification import NotificationController
from controlers.alert import AlertController
from dash_core_components import RadioItems,Graph
import dash_html_components as html


def generate_notification_table():

    return DataTable(
                id='notifications',
                columns=[{"name": i, "id": i} for i in NotificationController.get_atributes_list()],
                data=[],
                filter_action="custom",
                page_action="custom",
                page_current=0,
                page_size=20,
                style_table={
                      'maxHeight': '300px',
                      'overflowY': 'scroll',
                      'border': 'thin lightgrey solid',
                  },
    )

def generate_interval_input():
    return RadioItems(
                id='time_filter',
                options=[{'label': '24hs', 'value': 'h'},{'label': 'Semana', 'value': 'd'},{'label': 'Mes', 'value': 'm'}],
                value='h',
                labelStyle={'display': 'inline-block'}
            )

def generate_alert_table():
    return DataTable(
                id='alerts',
                columns=[{"name": i, "id": i} for i in AlertController.get_atributes_list()],
                data=[],
                page_action="custom",
                page_current=0,
                page_size=20,
                style_table={
                      'maxHeight': '300px',
                      'overflowY': 'scroll',
                      'border': 'thin lightgrey solid',
                  },
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
            [html.H6(id="total_notifications_text"), html.P("Notificaciones"),html.Span("Cantidad de notificaciones en 1hs",className="tooltiptext")],
            id="total_notifications",
            className="mini_container tooltip",
        ),
        html.Div(
            [html.H6(id="alert_text"), html.P("Alertas"),html.Span("Cantidad de alertas en 1hs",className="tooltiptext")],
            id="alert",
            className="mini_container tooltip",
        ),
        html.Div(
            [html.H6(id="actives_text"), html.P("Activos"),html.Span("Medidores reportados en 1hs ",className="tooltiptext")],
            id="actives",
            className="mini_container tooltip",
        ),
        html.Div(
            [html.H6(id="down_meter_text"), html.P("Sin respuesta"),html.Span("Sin respuestas en 1hs ",className="tooltiptext")],
            id="down_meter",
            className="mini_container tooltip",
        ),
        html.Div(
            [html.H6(id="total_imei_reports_text"), html.P("Total reportados"),html.Span("Total de medidores reportados",className="tooltiptext")],
            id="total_imei_reports",
            className="mini_container tooltip",
        )
    ]


def generate_graph():
    return [Graph(id="main_graph")]