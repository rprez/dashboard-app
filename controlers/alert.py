from datetime import datetime, timedelta
from models.alert import AlertModel
from sqlalchemy import desc

from db import db


class AlertController:

    @staticmethod
    def get_atributes_list() -> list:
        return ["imei", "ip", "fecha", "alert"]

    def find_by_imei(self, imei) -> "NotificationModel":
        return db.session.query(AlertModel).filter_by(imei=imei).first()

    def get_alert_by_id(self, id: int) -> "NotificationModel":
        return db.session.query(AlertModel).get(id)

    def get_alert_by_imei(self, imei: str) -> "NotificationModel":
        return db.session.query(AlertModel).filter_by(imei=imei).first()

    def get_alert_by_date(self, date: datetime) -> list:
        return db.session.query(AlertModel).filter_by(date=date).all()

    def get_alert_by_type(self, type_alert: str) -> list:
        return db.session.query(AlertModel).filter_by(alert=type_alert).all()

    def get_alert_list(self, days, hour, minutes) -> list:
        """Listado de alertas dentro de un perdio de tiempo.
            :param days
            :param hour
            :param minutes
        """
        now = datetime.now()
        period_time = now - timedelta(days=days, hours=hour, minutes=minutes)
        return db.session.query(AlertModel.id,AlertModel.alert).filter(AlertModel.fecha <= now, AlertModel.fecha >= period_time).all()

    def get_count_alert_by_perdiod(self, days, hour, minutes) -> int:
        """ Cantidad de alertas dentro de un perdio de tiempo.
            :param days
            :param hour
            :param minutes
        """
        now = datetime.now()
        period_time = now - timedelta(days=days, hours=hour, minutes=minutes)
        return db.session.query(AlertModel).filter(AlertModel.fecha <= now, AlertModel.fecha >= period_time).count()

    def get_all_alerts(self,page_current, page_size) -> list:
        return db.session.query(AlertModel).order_by(AlertModel.fecha.desc()).paginate(page_current, page_size,False).items

    def get_count_all_alert(self) -> int:
        return db.session.query(AlertModel).count()