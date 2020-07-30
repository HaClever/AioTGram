# -*- coding: utf-8 -*-
from . import apihelper

from . import MemoryHandlerBackend, FileHandlerBackend


__version__ = '0.1.0'


class AioTGram:
    """
    This is AioTGram Class.

    Methods:
        sendMessage
        sendNotification
    """

    def __init__(self, token, parse_mode=None,
                 next_step_backend=None, reply_backend=None):
        self.token = token
        self.parse_mode = parse_mode

        self.next_step_backend = next_step_backend
        if not self.next_step_backend:
            self.next_step_backend = MemoryHandlerBackend()

        self.reply_backend = reply_backend
        if not self.reply_backend:
            self.reply_backend = MemoryHandlerBackend()

    def enable_save_next_step_handler(self, delay=120, filename='./.handler-saves/step.save'):
        """
        Enable saving next step handlers (by default saving disabled)

        This function explicitly assigns FileHandlerBackend (instead of Saver) just to keep backward
        compatibility whose purpose was to enable file saving capability for handlers. And the same
        implementation is now available with FileHandlerBackend

        Most probably this function should be deprecated in future major releases

        :param delay: Delay between changes in handlers and saving
        :param filename: Filename of save file
        """
        self.next_step_backend = FileHandlerBackend(self.next_step_backend.handlers, filename, delay)

    def load_next_step_handlers(self, filename="./.handler-saves/step.save", del_file_after_loading=True):
        pass

    def set_webhook(self, url):
        apihelper.set_webhook(self.token, url)

    def delete_webhook(self):
        apihelper.delete_webhook(self.token)

    async def send_message(self, chat_id, text, reply_markup=None):
        await apihelper.send_message(self.token, chat_id, text, reply_markup)

    async def send_notification(self, chat_id, text, reply_markup=None):
        await apihelper.send_notification(self.token, chat_id, text, reply_markup)
