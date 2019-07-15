from flask_restful import Resource
from models.alert import AlertModel


class Alert(Resource):
    def get(self, imei):
        alert = AlertModel.find_by_imei(imei)
        if alert:
            return alert.json()
        return {'message': 'Alert not found'}, 404


class AlertList(Resource):
    def get(self):
        return {'alerts': [alert.json() for alert in AlertModel.query.all()]}




