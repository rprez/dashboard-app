import datetime

from sqlalchemy import Column, Integer, String,Sequence,TIMESTAMP

from db import db

class AlertModel(db.Model):
    __tablename__ = "notifications_alert"

    id = Column(Integer,Sequence('id_seq_alert'), primary_key=True)
    imei = Column('imei', String(32))
    ip = Column('ip', String(15))
    fecha = Column('fecha', TIMESTAMP)
    alert = Column('alert', String(40))

    def __init__(self,imei,ip,fecha,alert) -> None:
        self.imei = imei
        self.ip = ip
        self.fecha = fecha
        self.alert = alert

    def __init__(self, message: dict) -> None:
        self.imei = message.get('imei')
        self.ip = message.get('ip')
        self.fecha = datetime.datetime.strptime(message.get('fecha'), '%y-%m-%d %H:%M:%S')
        self.alert = message.get('alert')

    def json(self):
        return {'id': self.id, 'imei': self.imei, 'ip': self.ip, 'fecha': self.fecha, 'alert': self.alert}

    @classmethod
    def find_by_imei(cls, imei):
        return cls.query.filter_by(imei=imei).first()

    @classmethod
    def get_alert_by_id(cls,id: int) -> "AlertModel":
        return cls.query.get(id)

    @classmethod
    def get_alert_by_imei(cls,imei: str) -> "AlertModel":
        return cls.query.filter_by(imei=imei).first()

    @classmethod
    def get_alert_by_date(cls,date: datetime) -> list:
        return cls.query.filter_by(date=date).all()

    @classmethod
    def get_alert_by_type(cls, type_alert: str) -> list:
        return cls.query.filter_by(alert=type_alert).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()