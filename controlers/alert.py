import datetime
from models.alert import AlertModel

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

    def get_list_errors(self,days,hour,minutes) -> list:
        return "lastgasp sent"

    def get_all_alerts(self) -> list:
        return db.session.query(AlertModel).all()

    def get_count_all_alert(self) -> int:
        return db.session.query(AlertModel).count()