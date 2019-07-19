from models.notification import NotificationModel


class NotificationControler():

    @staticmethod
    def get_all_notifications() -> list:
        return NotificationModel.get_notification_list()

    @staticmethod
    def get_atributes_list() -> list:
        return ["imei", "ip", "fecha", "ecno", "rssi", "cellid", "log_size", "temp", "uptime"]

    @staticmethod
    def get_active_meter_list(period_time) -> list:
        return None

    @staticmethod
    def get_overheat_meter_list(max_temp) -> list:
        return None

    @staticmethod
    def get_low_signal_meter_list(min_power) -> list:
        '''Listado de medidores que tienen baja señal'''
        return None

    @staticmethod
    def get_down_meter(period_time) -> list:
        '''Listado de medidores que no se reportaron en cierto periodo de tiempo'''
        return None

    @staticmethod
    def get_meter_by_error_code(period_time, error_code) -> list:
        '''Listado de medidores que reportaron cierto error de codigo'''
        return None
