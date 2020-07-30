# -*- coding: utf-8 -*-
import asyncio

import aiohttp

from .types import JsonDeserializable


_API_URL = 'https://api.telegram.org/bot{token}/{method_name}'

_SESSION = None

_READ_TIMEOUT = 5
_DELAY_BETWEEN_REQUESTS = 10


async def _get_req_session():
    global _SESSION
    session = _SESSION

    if not session or session.closed:
        _SESSION = aiohttp.ClientSession(read_timeout=_READ_TIMEOUT)

    return _SESSION


async def fetch(session, method, request_url, params):
    try:
        result = await session.request(method, request_url, data=params)
    except(aiohttp.client_exceptions.ClientConnectionError,
           asyncio.TimeoutError):
        result = await fetch(session, method, request_url, params)
    except BaseException:
        raise AttributeError

    return result


async def _make_request(token, method_name, method='get', params=None):
    request_url = _API_URL.format(token=token, method_name=method_name)
    session = await _get_req_session()

    try:
        result = await session.request(method, request_url, data=params)
    except(aiohttp.client_exceptions.ClientConnectionError,
           asyncio.TimeoutError):
        result = await _make_request(token, method_name, method, params)
    except:
        msg = 'No connection to server. Used method: {}'.format(method_name)
        raise ApiException(msg, method_name)

    if result and result.status == 429:    # too many requests
        await asyncio.sleep(5)

        while True:
            result = await fetch(session, method, request_url, params)

            if result and result.status == 200:
                break

    return await _check_result(method_name, result)


async def _check_result(method_name, result):
    """
    Checks whether `result` is a valid API response.
    A result is considered invalid if:
        - The server returned an HTTP response code other than 200
        - The content of the result is invalid JSON.
        - The method call was unsuccessful (The JSON 'ok' field equals False)
    """
    pass


def set_webhook(token, url):
    method_url = 'setWebhook'
    payload = {'url': url}

    asyncio.create_task(
        _make_request(
            token,
            method_url,
            method='post',
            params=payload))


def delete_webhook(token):
    method_url = 'deleteWebhook'
    asyncio.create_task(
        _make_request(token, method_url)
    )


async def send_message(token, chat_id, text,
                       reply_markup=None):
    method_url = 'sendMessage'
    payload = {'chat_id': chat_id, 'text': text}
    if reply_markup:
        payload['reply_markup'] = await _convert_markup(reply_markup)

    await _make_request(token, method_url, method='post', params=payload)


async def send_notification(token, chat_id, text,
                            reply_markup=None):
    # NOTE: not tested yet with markup
    method_url = 'sendMessage'
    payload = {'chat_id': chat_id, 'text': text}
    await _make_request(token, method_url, params=payload)


async def _convert_markup(markup):
    if isinstance(markup, JsonDeserializable):
        return await markup.to_json()

    return markup


class ApiException(Exception):
    """
    This class represents an Exception thrown when a call to the Telegram API fails.
    In addition to an informative message, it has a `function_name` and a `result` attribute, which respectively
    contain the name of the failed function and the returned result that made the function to be considered  as
    failed.
    """

    def __init__(self, msg, function_name, result=None):
        super(ApiException, self).__init__("A request to the Telegram API was unsuccessful. {0}".format(msg))
        self.function_name = function_name
        self.result = result
