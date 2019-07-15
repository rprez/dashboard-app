from models.notification import NotificationModel


class NotificationControler():

    @staticmethod
    def get_all_notifications():
        return NotificationModel.get_notification_list()