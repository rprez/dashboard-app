from flask_restful import Resource
from models.notification import NotificationModel


class Notification(Resource):
    def get(self, imei):
        notification = NotificationModel.find_by_imei(imei)
        if notification:
            return notification.json()
        return {'message': 'Notification not found'}, 404


class NotificationList(Resource):
    def get(self):
        return {'notifications': [notification.json() for notification in NotificationModel.query.all()]}


