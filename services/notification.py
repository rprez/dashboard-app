from flask_restful import Resource
from controlers.notification import NotificationController

'''
    Clase encargada de gestionar las APIs Rest
'''

class Notification(Resource):

    def __init__(self):
        self.controler = NotificationController()

    def get(self, imei):
        notification = self.controler.find_by_imei(imei)
        if notification:
            return notification.json()
        return {'message': 'Notification not found'}, 404


class NotificationList(Resource):

    def __init__(self):
        self.controler = NotificationController()

    def get(self):
        return {'notifications': [notification.json() for notification in self.controler.get_all_notifications()]}


class NotificationActiveList(Resource):

    def __init__(self):
        self.controler = NotificationController()

    def get(self):
        return {'notifications': [notification.json() for notification in self.controler.get_active_meter_list(1,1,00)]}


