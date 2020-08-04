# -*- coding: utf-8 -*-

"""
Modules contains common types.

Types:
- WebhookInfo
- User
- MessageEntity
- PhotoSize
- UserProfilePhotos
- ForceReply
- LoginUrl
- BotCommand
"""

import asyncio

try:
    import ujson as json
except ImportError:
    import json

from .base import JsonDeserializable, Dictionaryable, JsonSerializable


class WebhookInfo(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None

        obj = cls.check_json(json_string)
        url = obj['url']
        has_custom_certificate = obj['has_custom_certificate']
        pending_update_count = obj['pending_update_count']
        last_error_date = obj.get('last_error_date')
        last_error_message = obj.get('last_error_message')
        max_connections = obj.get('max_connections')
        allowed_updates = obj.get('allowed_updates')

        return cls(url, has_custom_certificate, pending_update_count, last_error_date, last_error_message,
                   max_connections, allowed_updates)

    def __init__(self, url, has_custom_certificate, pending_update_count, last_error_date, last_error_message,
                 max_connections, allowed_updates):
        self.url = url
        self.has_custom_certificate = has_custom_certificate
        self.pending_update_count = pending_update_count
        self.last_error_date = last_error_date
        self.last_error_message = last_error_message
        self.max_connections = max_connections
        self.allowed_updates = allowed_updates


class User(JsonDeserializable, Dictionaryable, JsonSerializable):
    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None

        obj = cls.check_json(json_string)
        id_ = obj['id']
        is_bot = obj['is_bot']
        first_name = obj['first_name']
        last_name = obj.get('last_name')
        username = obj.get('username')
        language_code = obj.get('language_code')
        can_join_groups = obj.get('can_join_groups')
        can_read_all_group_messages = obj.get('can_read_all_group_messages')
        supports_inline_queries = obj.get('supports_inline_queries')

        return cls(id_, is_bot, first_name, last_name, username, language_code,
                   can_join_groups, can_read_all_group_messages, supports_inline_queries)

    def __init__(self, id_, is_bot, first_name, last_name=None, username=None, language_code=None, 
                 can_join_groups=None, can_read_all_group_messages=None, supports_inline_queries=None):
        self.id_ = id_
        self.is_bot = is_bot
        self.first_name = first_name
        self.username = username
        self.last_name = last_name
        self.language_code = language_code
        self.can_join_groups = can_join_groups
        self.can_read_all_group_messages = can_read_all_group_messages
        self.supports_inline_queries = supports_inline_queries

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {'id': self.id_,
                'is_bot': self.is_bot,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'username': self.username,
                'language_code': self.language_code,
                'can_join_groups': self.can_join_groups,
                'can_read_all_group_messages': self.can_read_all_group_messages,
                'supports_inline_queries': self.supports_inline_queries}


class MessageEntity(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None

        obj = cls.check_json(json_string)
        type_ = obj['type']
        offset = obj['offset']
        length = obj['length']
        url = obj.get('url')
        user = User.de_json(obj.get('user'))

        return cls(type_, offset, length, url, user)

    def __init__(self, type_, offset, length, url=None, user=None):
        self.type_ = type_
        self.offset = offset
        self.length = length
        self.url = url
        self.user = user


class PhotoSize(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None

        obj = cls.check_json(json_string)
        file_id = obj['file_id']
        width = obj['width']
        height = obj['height']
        file_size = obj.get('file_size')

        return cls(file_id, width, height, file_size)

    def __init__(self, file_id, width, height, file_size=None):
        self.file_size = file_size
        self.height = height
        self.width = width
        self.file_id = file_id


class UserProfilePhotos(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None

        obj = cls.check_json(json_string)
        total_count = obj['total_count']

        photos = []
        for x in obj['photos']:
            for y in x:
                photos.append(PhotoSize.de_json(y))

        return cls(total_count, photos)

    def __init__(self, total_count, photos):
        self.total_count = total_count
        self.photos = photos


class ForceReply(JsonSerializable):
    def __init__(self, selective=None):
        self.selective = selective

    def to_json(self):
        json_dict = {'force_reply': True}
        if self.selective:
            json_dict['selective'] = True
        return json.dumps(json_dict)


class LoginUrl(Dictionaryable, JsonSerializable):
    def __init__(self, url, forward_text=None, bot_username=None, request_write_access=None):
        self.url = url
        self.forward_text = forward_text
        self.bot_username = bot_username
        self.request_write_access = request_write_access

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        json_dict = {'url': self.url}
        if self.forward_text:
            json_dict['forward_text'] = self.forward_text
        if self.bot_username:
            json_dict['bot_username'] = self.bot_username
        if self.request_write_access:
            json_dict['request_write_access'] = self.request_write_access
        return json_dict


class BotCommand(JsonSerializable):
    def __init__(self, command, description):
        """
        This object represents a bot command.
        :param command: Text of the command, 1-32 characters.
            Can contain only lowercase English letters, digits and underscores.
        :param description: Description of the command, 3-256 characters.
        :return:
        """
        self.command = command
        self.description = description

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {'command': self.command, 'description': self.description}
