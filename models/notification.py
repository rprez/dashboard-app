import datetime

from sqlalchemy import Column, Integer, String,BigInteger,Sequence,TIMESTAMP,DECIMAL

from db import db


class NotificationModel(db.Model):
    __tablename__ = "notifications"

    id = Column(Integer,Sequence('id_seq_notif'), primary_key=True)
    imei = Column('imei', BigInteger)
    ip = Column('ip', String(15))
    fecha = Column('fecha', TIMESTAMP)
    ecno = Column('ecno', Integer)
    rssi = Column('rssi', String(10))
    cellid = Column('cellid', Integer)
    log_size = Column('logsize', Integer)
    temp = Column('temp', DECIMAL)
    uptime = Column('uptime', Integer)

    def __init__(self,imei,ip,fecha,ecno,rssi,cellid,log_size,temp,uptime) -> None:
        self.imei = imei
        self.ip = ip
        self.fecha = fecha
        self.ecno = ecno
        self.rssi = rssi
        self.cellid = cellid
        self.log_size = log_size
        self.temp = temp
        self.uptime = uptime

    def __init__(self,message : dict) -> None:
        self.imei = message.get('imei')
        self.ip = message.get('ip')
        self.fecha = datetime.datetime.strptime(message.get('fecha'), '%y-%m-%d %H:%M:%S')
        self.ecno = message.get('EC/NO')
        self.rssi = message.get('rssi')
        self.cellid = message.get('cellid')
        self.log_size = message.get('logSize')
        self.temp = message.get('temp')
        self.uptime = message.get('uptime')

    def json(self):
        return {'id': self.id, 'imei': self.imei, 'ip': self.ip, 'fecha': self.fecha.__str__(),
                'ecno': self.ecno, 'rssi': self.rssi, 'cellid':self.cellid, 'log_size':self.log_size,
                'temp':self.temp.__str__(), 'uptime':self.uptime
                }

    @classmethod
    def find_by_imei(cls, imei):
        return cls.query.filter_by(imei=imei).first()

    @classmethod
    def get_alert_by_id(cls,id: int) -> "NotificationModel":
        return cls.query.get(id)

    @classmethod
    def get_alert_by_imei(cls,imei: str) -> "NotificationModel":
        return cls.query.filter_by(imei=imei).first()

    @classmethod
    def get_alert_by_date(cls,date: datetime) -> list:
        return cls.query.filter_by(date=date).all()

    @classmethod
    def get_alert_by_type(cls, type_alert: str) -> list:
        return cls.query.filter_by(alert=type_alert).all()

    @classmethod
    def get_notification_list(cls) -> list:
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()