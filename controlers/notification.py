from models.notification import NotificationModel
from datetime import datetime, timedelta
from collections import Counter
from sqlalchemy import desc

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

    def get_all_notifications(self,page_current,page_size) -> list:
        result =  db.session.query(NotificationModel).order_by(NotificationModel.fecha.desc()).paginate(page_current,page_size,False).items
        return result

    def get_count_all_notifications(self) -> list:
        """Obtiene todas las mediciones enviadas. """
        return db.session.query(NotificationModel).count()

    def get_count_notifications_by_perdiod(self,days, hour, minutes) -> int:
        """Obtiene la cantidad de notificaciones enviadas segun el periodo de tiempo dado.
                    :param days
                    :param hour
                    :param minutes
                """
        now = datetime.now()
        period_time = now - timedelta(days=days, hours=hour, minutes=minutes)
        return db.session.query(NotificationModel).filter(NotificationModel.fecha <= now,
                                                          NotificationModel.fecha >= period_time).count()

    def get_active_meter_list(self,days,hour,minutes) -> list:
        """Listado de medidores con diferentes imei que reportaron medición por un perdio de tiempo.
            :param delta_time refiere a cantidad de dias.
        """
        now = datetime.now()
        period_time = now - timedelta(days=days,hours=hour,minutes=minutes)
        return db.session.query(NotificationModel.imei.distinct(), NotificationModel.fecha).filter(NotificationModel.fecha <= now,NotificationModel.fecha >= period_time).order_by(NotificationModel.fecha.desc())

    def get_init_active_graph(self, days, hour, minutes):
        """Eje de las x para grafica de activos dentro de un perdio de tiempo.
            :param days
            :param hour
            :param minutes
        """
        active_meter_list = self.get_active_meter_list(days,hour,minutes)
        return Counter([x.fecha.date() for x in active_meter_list if x.fecha])


    def get_count_active_meter_list(self,days,hour,minutes) -> int:
        """Listado de medidores activos dentro de un perdio de tiempo.
            :param days
            :param hour
            :param minutes
        """
        now = datetime.now()
        period_time = now - timedelta(days=days,hours=hour,minutes=minutes)
        return db.session.query(NotificationModel.imei.distinct()).filter(NotificationModel.fecha <= now,NotificationModel.fecha >= period_time).count()


    def get_count_distinct_imei_notification(self) -> int:
        return db.session.query(NotificationModel.imei.distinct()).count()