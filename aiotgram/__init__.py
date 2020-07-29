# -*- coding: utf-8 -*-
from . import apihelper


__version__ = '0.1.0'


class GramBot:
    """
    This is Gram Class.

    Methods:
        sendMessage
        sendNotification

        set_webhook
        delete_webhook
    """

    def __init__(self, token):
        self.token = token

    def set_webhook(self, url):
        apihelper.set_webhook(self.token, url)

    def delete_webhook(self):
        apihelper.delete_webhook(self.token)

    async def send_message(self, chat_id, text, reply_markup=None):
        await apihelper.send_message(self.token, chat_id, text, reply_markup)

    async def send_notification(self, chat_id, text, reply_markup=None):
        await apihelper.send_notification(self.token, chat_id, text, reply_markup)
