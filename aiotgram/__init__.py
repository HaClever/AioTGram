# -*- coding: utf-8 -*-
import sys
import re
import six
import asyncio

from aiotgram import apihelper, types, util

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
        self.update_listener = []

        self.last_update_id = 0

        self.next_step_backend = next_step_backend
        if not self.next_step_backend:
            self.next_step_backend = MemoryHandlerBackend()

        self.reply_backend = reply_backend
        if not self.reply_backend:
            self.reply_backend = MemoryHandlerBackend()

        self.message_handlers = []
        self.edited_message_handlers = []
        self.channel_post_handlers = []
        self.edited_channel_post_handlers = []
        self.inline_handlers = []
        self.chosen_inline_handlers = []
        self.callback_query_handlers = []
        self.shipping_query_handlers = []
        self.pre_checkout_query_handlers = []
        self.poll_handlers = []
        self.poll_answer_handlers = []

    def enable_save_next_step_handlers(self, delay=120, filename='./.handler-saves/step.save'):
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
        """
        Load next step handlers from save file

        This function is left to keep backward compatibility whose purpose was to load handlers from file with the
        help of FileHandlerBackend and is only recommended to use if next_step_backend was assigned as
        FileHandlerBackend before entering this function

        Most probably this function should be deprecated in future major releases

        :param filename: Filename of the file where handlers was saved
        :param del_file_after_loading: Is passed True, after loading save file will be deleted
        """
        self.next_step_backend.load_handlers(filename, del_file_after_loading)

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

    def process_new_updates(self, updates):
        new_messages = []
        new_edited_messages = []
        new_channel_posts = []
        new_edited_channel_posts = []
        new_inline_querys = []
        new_chosen_inline_results = []
        new_callback_querys = []
        new_shipping_querys = []
        new_pre_checkout_querys = []
        new_polls = []
        new_poll_answers = []

        for update in updates:
            # TODO: Add process_middlewares to enable middlewares

            if update.update_id > self.last_update_id:
                self.last_update_id = update.update_id
            if update.message:
                new_messages.append(update.message)
            if update.edited_message:
                new_edited_messages.append(update.edited_message)
            if update.channel_post:
                new_channel_posts.append(update.channel_post)
            if update.edited_channel_post:
                new_edited_channel_posts.append(update.edited_channel_post)
            if update.inline_query:
                new_inline_querys.append(update.inline_query)
            if update.chosen_inline_result:
                new_chosen_inline_results.append(update.chosen_inline_result)
            if update.callback_query:
                new_callback_querys.append(update.callback_query)
            if update.shipping_query:
                new_shipping_querys.append(update.shipping_query)
            if update.pre_checkout_query:
                new_pre_checkout_querys.append(update.pre_checkout_query)
            if update.poll:
                new_polls.append(update.poll)
            if update.poll_answer:
                new_poll_answers.append(update.poll_answer)

        if len(new_messages) > 0:
            self.process_new_messages(new_messages)
        if len(new_edited_messages) > 0:
            self.process_new_edited_messages(new_edited_messages)
        if len(new_channel_posts) > 0:
            self.process_new_channel_posts(new_channel_posts)
        if len(new_edited_channel_posts) > 0:
            self.process_new_edited_channel_posts(new_edited_channel_posts)
        if len(new_inline_querys) > 0:
            self.process_new_inline_query(new_inline_querys)
        if len(new_chosen_inline_results) > 0:
            self.process_new_chosen_inline_query(new_chosen_inline_results)
        if len(new_callback_querys) > 0:
            self.process_new_callback_query(new_callback_querys)
        if len(new_shipping_querys) > 0:
            self.process_new_shipping_query(new_shipping_querys)
        if len(new_pre_checkout_querys) > 0:
            self.process_new_pre_checkout_query(new_pre_checkout_querys)
        if len(new_polls) > 0:
            self.process_new_poll(new_polls)
        if len(new_poll_answers) > 0:
            self.process_new_poll_answer(new_poll_answers)

    def process_new_messages(self, new_messages):
        self._notify_next_handlers(new_messages)
        self._notify_reply_handlers(new_messages)
        self.__notify_update(new_messages)
        self._notify_command_handlers(self.message_handlers, new_messages)

    def process_new_edited_messages(self, edited_message):
        self._notify_command_handlers(self.edited_message_handlers, edited_message)

    def process_new_channel_posts(self, channel_post):
        self._notify_command_handlers(self.channel_post_handlers, channel_post)

    def process_new_edited_channel_posts(self, edited_channel_post):
        self._notify_command_handlers(self.edited_channel_post_handlers, edited_channel_post)

    def process_new_inline_query(self, new_inline_querys):
        self._notify_command_handlers(self.inline_handlers, new_inline_querys)

    def process_new_chosen_inline_query(self, new_chosen_inline_querys):
        self._notify_command_handlers(self.chosen_inline_handlers, new_chosen_inline_querys)

    def process_new_callback_query(self, new_callback_querys):
        self._notify_command_handlers(self.callback_query_handlers, new_callback_querys)

    def process_new_shipping_query(self, new_shipping_querys):
        self._notify_command_handlers(self.shipping_query_handlers, new_shipping_querys)

    def process_new_pre_checkout_query(self, pre_checkout_querys):
        self._notify_command_handlers(self.pre_checkout_query_handlers, pre_checkout_querys)

    def process_new_poll(self, polls):
        self._notify_command_handlers(self.poll_handlers, polls)

    def process_new_poll_answer(self, poll_answers):
        self._notify_command_handlers(self.poll_answer_handlers, poll_answers)

    def __notify_update(self, new_messages):
        for listener in self.update_listener:
            self._exec_task(listener, new_messages)

    def _notify_next_handlers(self, new_messages):
        """
        Description: TBD
        :param new_messages:
        :return:
        """
        for i, message in enumerate(new_messages):
            need_pop = False
            handlers = self.next_step_backend.get_handlers(message.chat.id)
            for handler in handlers:
                need_pop = True
                self._exec_task(handler["callback"], message, *handler["args"], **handler["kwargs"])
            if need_pop:
                new_messages.pop(i)  # removing message that detects with next_step_handler

    def _notify_reply_handlers(self, new_messages):
        """
        Notify handlers of the answers
        :param new_messages:
        :return:
        """
        for message in new_messages:
            if hasattr(message, "reply_to_message") and message.reply_to_message is not None:
                handlers = self.reply_backend.get_handlers(message.reply_to_message.message_id)
                for handler in handlers:
                    self._exec_task(handler["callback"], message, *handler["args"], **handler["kwargs"])

    def _notify_command_handlers(self, handlers, new_messages):
        """
        Notifies command handlers
        :param handlers:
        :param new_messages:
        :return:
        """
        for message in new_messages:
            for message_handler in handlers:
                if self._test_message_handler(message_handler, message):
                    self._exec_task(message_handler['function'], message)
                    break

    @staticmethod
    def _test_filter(message_filter, filter_value, message):
        """
        Test filters
        :param message_filter:
        :param filter_value:
        :param message:
        :return:
        """
        test_cases = {
            'content_types': lambda msg: msg.content_type in filter_value,
            'regexp': lambda msg: msg.content_type == 'text' and re.search(filter_value, msg.text, re.IGNORECASE),
            'commands': lambda msg: msg.content_type == 'text' and util.extract_command(msg.text) in filter_value,
            'func': lambda msg: filter_value(msg)
        }

        return test_cases.get(message_filter, lambda msg: False)(message)

    def _test_message_handler(self, message_handler, message):
        # TODO: rewrite it
        """
        Test message handler
        :param message_handler:
        :param message:
        :return:
        """
        for message_filter, filter_value in six.iteritems(message_handler['filters']):
            if filter_value is None:
                continue

            if not self._test_filter(message_filter, filter_value, message):
                return False

        return True

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

    def _exec_task(self, task, *args, **kwargs):
        asyncio.create_task(task(*args, **kwargs))
