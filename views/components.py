import dash_table
from controlers.notification import NotificationControler



@staticmethod
def generate_table():

    list_columns = NotificationControler.get_atributes_list()
    list_notification = [x.json() for x in NotificationControler.get_all_notifications()]

    return dash_table.DataTable(
        id='notifications',
        columns=[{"name": i, "id": i} for i in list_columns],
        data=list_notification
    )
