# -*- coding: utf-8 -*-
from aiotgram import apihelper

from aiotgram.handler_backends import MemoryHandlerBackend, FileHandlerBackend


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

    async def enable_save_next_step_handlers(self, delay=120, filename='./.handler-saves/step.save'):
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

    async def load_next_step_handlers(self, filename="./.handler-saves/step.save", del_file_after_loading=True):
        """
        Load next step handlers from save file

        This function is left to keep backward compatibility whose purpose was to load handlers from file with the
        help of FileHandlerBackend and is only recommended to use if next_step_backend was assigned as
        FileHandlerBackend before entering this function

        Most probably this function should be deprecated in future major releases

        :param filename: Filename of the file where handlers was saved
        :param del_file_after_loading: Is passed True, after loading save file will be deleted
        """
        await self.next_step_backend.load_handlers(filename, del_file_after_loading)

    async def set_webhook(self, url):
        await apihelper.set_webhook(self.token, url)

    async def delete_webhook(self):
        await apihelper.delete_webhook(self.token)

    async def send_message(self, chat_id, text, reply_markup=None):
        await apihelper.send_message(self.token, chat_id, text, reply_markup)

    async def send_notification(self, chat_id, text, reply_markup=None):
        await apihelper.send_notification(self.token, chat_id, text, reply_markup)
