# -*- coding: utf-8 -*-
import os
import pickle
import threading

from abc import ABCMeta, abstractmethod


class HandlerBackend(metaclass=ABCMeta):
    """
    Class for saving (next step|reply) handlers
    """
    def __init__(self, handlers=None):
        if handlers is None:
            handlers = {}
        self.handlers = handlers

    @abstractmethod
    def register_handler(self, handler_group_id, handler):
        pass

    @abstractmethod
    def clear_handlers(self, handler_group_id):
        pass

    @abstractmethod
    def get_handlers(self, handler_group_id):
        pass


class MemoryHandlerBackend(HandlerBackend):
    def register_handler(self, handler_group_id, handler):
        if handler_group_id in self.handlers:
            self.handlers[handler_group_id] = handler
        else:
            self.handlers[handler_group_id] = [handler]

    def clear_handlers(self, handler_group_id):
        self.handlers.pop(handler_group_id, [])

    def get_handlers(self, handler_group_id):
        return self.handlers.pop(handler_group_id, [])


class FileHandlerBackend(HandlerBackend):
    # TODO: write custom async data serializer to file , if it require. Check it!

    def __init__(self, handlers=None, filename='./.handler-saves/handlers.save', delay=120):
        super().__init__(handlers)
        self.filename = filename
        self.delay = delay
        self.timer = threading.Timer(delay, self.save_handlers)

    def register_handler(self, handler_group_id, handler):
        if handler_group_id in self.handlers:
            self.handlers[handler_group_id].append(handler)
        else:
            self.handlers[handler_group_id] = [handler]

        self.start_save_timer()

    def clear_handlers(self, handler_group_id):
        self.handlers.pop(handler_group_id, [])

        self.start_save_timer()

    def get_handlers(self, handler_group_id):
        handlers = self.handlers.pop(handler_group_id, [])

        self.start_save_timer()

        return handlers

    def start_save_timer(self):
        # TODO: if possible rewrite threading timer to async
        if not self.timer.is_alive():
            if self.delay <= 0:
                self.save_handlers()
            else:
                self.timer = threading.Timer(self.delay, self.save_handlers)
                self.timer.start()

    def save_handlers(self):
        self.dump_handlers(self.handlers, self.filename)

    def load_handlers(self, filename=None, del_file_after_loading=True):
        if not filename:
            filename = self.filename

        tmp = self.return_load_handlers(filename, del_file_after_loading=del_file_after_loading)
        if tmp is not None:
            self.handlers.update(tmp)

    @staticmethod
    def dump_handlers(handlers, filename, file_mode='wb'):
        # TODO: Need tests
        # TODO: If possible - rewrite to async
        dirs = filename.rsplit('/', maxsplit=1)[0]
        os.makedirs(dirs, exist_ok=True)

        with open(filename + ".tmp", file_mode) as file:
            pickle.dump(handlers, file)

        if os.path.isfile(filename):
            os.remove(filename)

        os.rename(filename + ".tmp", filename)

    @staticmethod
    def return_load_handlers(filename, del_file_after_loading=True):
        if os.path.isfile(filename) and os.path.getsize(filename) > 0:
            with open(filename, "rb") as file:
                handlers = pickle.load(file)

            if del_file_after_loading:
                os.remove(filename)

            return handlers


class RedisHandlerBackend(HandlerBackend):
    def __init__(self, handlers=None, host='localhost', port=6379, db=0, prefix='AioTGram'):
        super().__init__(handlers)

    def register_handler(self, handler_group_id, handler):
        pass

    def clear_handlers(self, handler_group_id):
        pass

    def get_handlers(self, handler_group_id):
        pass
