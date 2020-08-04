# -*- coding: utf-8 -*-

"""
Modules contains poll types.

Types:
- PollOption
- PollAnswer
"""

try:
    import ujson as json
except ImportError:
    import json

from .base import JsonSerializable, JsonDeserializable, Dictionaryable
from .common import User


class PollOption(JsonSerializable, JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None

        obj = cls.check_json(json_string)
        text = obj['text']
        voter_count = int(obj['voter_count'])

        return cls(text, voter_count)

    def __init__(self, text, voter_count=0):
        self.text = text
        self.voter_count = voter_count

    def to_json(self):
        # send_poll Option is a simple string: https://core.telegram.org/bots/api#sendpoll
        return json.dumps(self.text)


class PollAnswer(JsonSerializable, JsonDeserializable, Dictionaryable):
    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None

        obj = cls.check_json(json_string)
        poll_id = obj['poll_id']
        user = User.de_json(obj['user'])
        options_ids = obj['option_ids']

        return cls(poll_id, user, options_ids)

    def __init__(self, poll_id, user, options_ids):
        self.poll_id = poll_id
        self.user = user
        self.options_ids = options_ids

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {'poll_id': self.poll_id,
                'user': self.user.to_dict(),
                'options_ids': self.options_ids}
