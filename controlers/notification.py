from models.notification import NotificationModel


class NotificationControler():

    @staticmethod
    def get_all_notifications()  -> list:
        return NotificationModel.get_notification_list()

    @staticmethod
    def get_atributes_list() -> list:
        return ["imei","ip","fecha","ecno","rssi","cellid","log_size","temp","uptime"]

    @staticmethod
    def get_active_meter_list(last_time) -> list:
        return None

    @staticmethod
    def get_overheat_meter_list(max_temp) -> list:
        return None

    @staticmethod
    def get_low_signal_meter_list(min_power) -> list:
        return None
