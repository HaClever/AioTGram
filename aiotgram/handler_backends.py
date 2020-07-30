# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod


class HandlerBackend(meta=ABCMeta):
    """
    Class for saving (next step|reply) handlers
    """
    def __init__(self, handlers=None):
        if handlers is None:
            handlers = {}
        self.handlers = handlers

    @abstractmethod
    async def register_handler(self, handler_group_id, handler):
        pass

    @abstractmethod
    async def clear_handlers(self, handler_group_id):
        pass

    @abstractmethod
    async def get_handlers(self, handler_group_id):
        pass


class MemoryHandlerBackend(HandlerBackend):
    async def register_handler(self, handler_group_id, handler):
        if handler_group_id in self.handlers:
            self.handlers[handler_group_id] = handler
        else:
            self.handlers[handler_group_id] = [handler]

    async def clear_handlers(self, handler_group_id):
        self.handlers.pop(handler_group_id, [])

    async def get_handlers(self, handler_group_id):
        return self.handlers.pop(handler_group_id, [])


class FileHandlerBackend(HandlerBackend):
    def __init__(self, handlers=None, filename='./.handler-saves/handlers.save', delay=120):
        super(FileHandlerBackend, self).__init__(handlers)
        self.filename = filename
        self.delay = delay

    


class RedisHandlerBackend(HandlerBackend):
    pass
