from models.notification import NotificationModel


class NotificationControler():

    @staticmethod
    def get_all_notifications()  -> list:
        return NotificationModel.get_notification_list()

    @staticmethod
    def get_atributes_list() -> list:
        return ["imei","ip","fecha","ecno","rssi","cellid","log_size","temp","uptime"]