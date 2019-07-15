import dash_table
from controlers.notification import NotificationControler

"""
        return {'id': self.id, 'imei': self.imei, 'ip': self.ip, 'fecha': self.fecha.__str__(),
                'ecno': self.ecno, 'rssi': self.rssi, 'cellid':self.cellid, 'log_size':self.log_size,
                'temp':self.temp.__str__(), 'uptime':self.uptime
                }
"""

def get_table_notification():

    list_notification = NotificationControler().get_all_notifications()

    return dash_table.DataTable(
        id='notifications',
        columns=[{"imei": i.imei, "id": i.id} for i in list_notification],
        data=list_notification,
    )