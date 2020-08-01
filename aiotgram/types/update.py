# -*- coding: utf-8 -*-
from .base import JsonDeserializable
from .ext import Message, CallbackQuery, Poll

from .inlinequery import InlineQuery, ChosenInlineResult
from .payments import ShippingQuery, PreCheckoutQuery
from .inputmedia import PollAnswer


class Update(JsonDeserializable):
    @classmethod
    async def de_json(cls, json_string):
        if json_string is None:
            return None

        obj = await cls.check_json(json_string)
        update_id = obj['update_id']
        message = await Message.de_json(obj.get('message'))
        edited_message = await Message.de_json(obj.get('edited_message'))
        channel_post = await Message.de_json(obj.get('channel_post'))
        edited_channel_post = await Message.de_json(obj.get('edited_channel_post'))
        inline_query = await InlineQuery.de_json(obj.get('inline_query'))
        chosen_inline_result = await ChosenInlineResult.de_json(obj.get('chosen_inline_result'))
        callback_query = await CallbackQuery.de_json(obj.get('callback_query'))
        shipping_query = await ShippingQuery.de_json(obj.get('shipping_query'))
        pre_checkout_query = await PreCheckoutQuery.de_json(obj.get('pre_checkout_query'))
        poll = await Poll.de_json(obj.get('poll'))
        poll_answer = await PollAnswer.de_json(obj.get('poll_answer'))

        return cls(update_id, message, edited_message, channel_post, edited_channel_post, inline_query,
                   chosen_inline_result, callback_query, shipping_query, pre_checkout_query, poll, poll_answer)

    def __init__(self, update_id, message, edited_message, channel_post, edited_channel_post, inline_query,
                 chosen_inline_result, callback_query, shipping_query, pre_checkout_query, poll, poll_answer):
        self.update_id = update_id
        self.message = message
        self.edited_message = edited_message
        self.channel_post = channel_post
        self.edited_channel_post = edited_channel_post
        self.inline_query = inline_query
        self.chosen_inline_result = chosen_inline_result
        self.callback_query = callback_query
        self.shipping_query = shipping_query
        self.pre_checkout_query = pre_checkout_query
        self.poll = poll
        self.poll_answer = poll_answer
