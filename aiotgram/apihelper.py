# -*- coding: utf-8 -*-
import asyncio

import aiohttp

from .types import JsonDeserializable


API_URL = 'https://api.telegram.org/bot{token}/{method_name}'


async def _make_request(token, method_name, method='get', params=None):
    request_url = API_URL.format(token=token, method_name=method_name)

    async with aiohttp.ClientSession(read_timeout=3) as session:
        try:
            async with session.post(request_url, data=params) as response:
                result = await response.json()
        except(aiohttp.client_exceptions.ClientConnectionError, asyncio.TimeoutError):
            result = await _make_request(token, request_url)
        except:
            # TODO: Need to raise up exception.
            pass

        return await _check_result(method_name, result)


async def _check_result(method_name, result):
    """
    Checks whether `result` is a valid API response.
    A result is considered invalid if:
        - The server returned an HTTP response code other than 200
        - The content of the result is invalid JSON.
        - The method call was unsuccessful (The JSON 'ok' field equals False)
    """
    if result['error_code']:
        msg = 'The server returned HTTP {0} {1}. Response body:\n[{2}]' \
            .format(result['error_code'], result['description'], result)


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
