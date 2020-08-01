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

        self.message_handlers = []

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

    def message_handler(self, commands=None, regexp=None, func=None, content_types=None, **kwargs):
        """
        Message handler decorator.
        This decorator can be used to decorate functions that must handle certain types of messages.
        All message handlers are tested in the order they were added.

        Example:

        bot = AioTGram('TOKEN')

        # Handles all messages which text matches regexp.
        @bot.message_handler(regexp='someregexp')
        def command_help(message):
            bot.send_message(message.chat.id, 'Did someone call for help?')

        # Handle all sent documents of type 'text/plain'.
        @bot.message_handler(func=lambda message: message.document.mime_type == 'text/plain', content_types=['document'])
        def command_handle_document(message):
            bot.send_message(message.chat.id, 'Document received, sir!')

        # Handle all other messages.
        @bot.message_handler(func=lambda message: True, content_types=['audio', 'photo', 'voice', 'video', 'document', 'text', 'location', 'contact', 'sticker'])
        def default_command(message):
            bot.send_message(message.chat.id, "This is the default command handler.")


        :param commands: Optional list of strings (commands to handle).
        :param regexp: Optional regular expression.
        :param func: Optional lambda function. The lambda receives the message to test as the first parameter. It must return True if the command should handle the message.
        :param content_types: This commands' supported content types. Must be a list. Defaults to ['text'].
        """
        if content_types is None:
            content_types = ['text']

        def decorator(handler):
            handler_dict = self._build_handler_dict(
                handler,
                commands=commands,
                regexp=regexp,
                func=func,
                content_types=content_types,
                **kwargs
            )
            self.add_message_handler(handler_dict)

            return handler

        return decorator

    def add_message_handler(self, handler_dict):
        """
        Adds a message handler
        :param handler_dict:
        :return:
        """
        self.message_handlers.append(handler_dict)

    @staticmethod
    def _build_handler_dict(handler, **filters):
        """
        Builds a dictionary for a handler
        :param handler:
        :param filters:
        :return:
        """
        return {
            'function': handler,
            'filters': filters,
        }
