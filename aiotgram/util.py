# -*- coding: utf-8 -*-
import string
import random
import asyncio

from six import string_types


class Timer:
    # NOTE: need more tests.
    def __init__(self, timeout, callback):
        self._timeout = timeout
        self._callback = callback
        self._task = asyncio.create_task(self._job())

    async def _job(self):
        await asyncio.sleep(self._timeout)
        await self._callback()

    async def is_alive(self):
        return self._task.done()

    async def cancel(self):
        self._task.cancel()


def is_command(text):
    """
    Checks if `text` is a command. Telegram chat commands start with the '/' character.
    :param text: Text to check.
    :return: True if `text` is a command, else False.
    """
    return text.startswith('/')


def extract_command(text):
    """
    Extracts the command from `text` (minus the '/') if `text` is a command (see is_command).
    If `text` is not a command, this function returns None.

    Examples:
    extract_command('/help'): 'help'
    extract_command('/help@BotName'): 'help'
    extract_command('/search black eyed peas'): 'search'
    extract_command('Good day to you'): None

    :param text: String to extract the command from
    :return: the command if `text` is a command (according to is_command), else None.
    """
    return text.split()[0].split('@')[0][1:] if is_command(text) else None


def is_string(var):
    return isinstance(var, string_types)


def generate_random_token():
    return ''.join(random.sample(string.ascii_letters, 16))
