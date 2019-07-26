from models.notification import NotificationModel
from datetime import datetime, timedelta
from collections import Counter

from db import db


class NotificationController:

    @staticmethod
    def get_atributes_list() -> list:
        return ["imei", "ip", "fecha", "ecno", "rssi", "cellid", "log_size", "temp", "uptime"]

    def find_by_imei(self,imei)  -> "NotificationModel":
        return db.session.query(NotificationModel).filter_by(imei=imei).first()

    def get_notification_by_id(self, id: int) -> "NotificationModel":
        return db.session.query(NotificationModel).get(id)

    def get_notification_by_imei(self, imei: str) -> "NotificationModel":
        return db.session.query(NotificationModel).filter_by(imei=imei).first()

    def get_notification_by_date(self, date: datetime) -> list:
        return db.session.query(NotificationModel).filter_by(date=date).all()

    def get_notification_by_type(self, type_alert: str) -> list:
        return db.session.query(NotificationModel).filter_by(alert=type_alert).all()

    def get_all_notifications(self) -> list:
        return db.session.query(NotificationModel).all()

    def get_count_all_notifications(self) -> list:
        return db.session.query(NotificationModel).count()

    def get_active_meter_list(self,days,hour,minutes) -> list:
        """Listado de medidores activos dentro de un perdio de tiempo.
            :param delta_time refiere a cantidad de dias.
        """
        now = datetime.now()
        period_time = now - timedelta(days=days,hours=hour,minutes=minutes)
        return db.session.query(NotificationModel).filter(NotificationModel.fecha <= now,NotificationModel.fecha >= period_time).all()

    def get_init_active_graph(self,days,hour,minutes):
        """Eje de las x para grafica de activos dentro de un perdio de tiempo.
            :param days
            :param hour
            :param minutes
        """
        active_meter_list = self.get_active_meter_list(days,hour,minutes)
        result = Counter([x.fecha.date() for x in active_meter_list if x.fecha])
        ACA ME QUEDE
        return result


    def get_count_active_meter_list(self,days,hour,minutes) -> int:
        """Listado de medidores activos dentro de un perdio de tiempo.
            :param days
            :param hour
            :param minutes
        """
        now = datetime.now()
        period_time = now - timedelta(days=days,hours=hour,minutes=minutes)
        return db.session.query(NotificationModel).filter(NotificationModel.fecha <= now,NotificationModel.fecha >= period_time).count()

    def get_overheat_meter_list(self,max_temp) -> list:
        return None


    def get_low_signal_meter_list(self,min_power) -> list:
        '''Listado de medidores que tienen baja señal'''
        return None


    def get_count_down_meter(self,days,hour,minutes) -> list:
        '''Listado de medidores que no se reportaron en cierto periodo de tiempo
            :param days
            :param hour
            :param minutes
        '''
        now = datetime.now()
        period_time = now - timedelta(days=days, hours=hour, minutes=minutes)
        total_meter = db.session.query(NotificationModel.id.distinct()).count()
        active_meter = db.session.query(NotificationModel).filter(NotificationModel.fecha <= now,NotificationModel.fecha >= period_time).count()

        return total_meter - active_meter


    def get_meter_by_error_code(self,period_time, error_code) -> list:
        '''Listado de medidores que reportaron cierto error de codigo'''
        return None
