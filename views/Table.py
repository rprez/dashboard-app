import dash_table
from controlers.notification import NotificationControler


def generate_table():

    list_notification = NotificationControler.get_all_notifications()

    return dash_table.DataTable(
        id='notifications',
        columns=[{"name": i, "id": i.id} for i in list_notification],
        data=list_notification,
    )
