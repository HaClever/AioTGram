# -*- coding: utf-8 -*-
try:
    import ujson as json
except ImportError:
    import json

from .base import JsonDeserializable, Dictionaryable, JsonSerializable
from .common import User


class GroupChat(JsonDeserializable):
    @classmethod
    async def de_json(cls, json_string):
        if json_string is None:
            return None

        obj = await cls.check_json(json_string)
        id_ = obj['id']
        title = obj['title']

        return cls(id_, title)

    def __init__(self, id_, title):
        self.id_ = id_
        self.title = title


class ChatPhoto(JsonDeserializable):
    @classmethod
    async def de_json(cls, json_string):
        if json_string is None:
            return None

        obj = await cls.check_json(json_string)
        small_file_id = obj['small_file_id']
        big_file_id = obj['big_file_id']

        return cls(small_file_id, big_file_id)

    def __init__(self, small_file_id, big_file_id):
        self.small_file_id = small_file_id
        self.big_file_id = big_file_id


class ChatMember(JsonDeserializable):
    @classmethod
    async def de_json(cls, json_string):
        if json_string is None:
            return None

        obj = await cls.check_json(json_string)
        user = await User.de_json(obj['user'])
        status = obj['status']
        custom_title = obj.get('custom_title')
        until_date = obj.get('until_date')
        can_be_edited = obj.get('can_be_edited')
        can_post_messages = obj.get('can_post_messages')
        can_edit_messages = obj.get('can_edit_messages')
        can_delete_messages = obj.get('can_delete_messages')
        can_restrict_members = obj.get('can_restrict_members')
        can_promote_members = obj.get('can_promote_members')
        can_change_info = obj.get('can_change_info')
        can_invite_users = obj.get('can_invite_users')
        can_pin_messages = obj.get('can_pin_messages')
        is_member = obj.get('is_member')
        can_send_messages = obj.get('can_send_messages')
        can_send_media_messages = obj.get('can_send_media_messages')
        can_send_polls = obj.get('can_send_polls')
        can_send_other_messages = obj.get('can_send_other_messages')
        can_add_web_page_previews = obj.get('can_add_web_page_previews')

        return cls(
            user, status, custom_title, until_date, can_be_edited, can_post_messages,
            can_edit_messages, can_delete_messages, can_restrict_members,
            can_promote_members, can_change_info, can_invite_users, can_pin_messages,
            is_member, can_send_messages, can_send_media_messages, can_send_polls,
            can_send_other_messages, can_add_web_page_previews)

    def __init__(self, user, status, custom_title=None, until_date=None, can_be_edited=None,
                 can_post_messages=None, can_edit_messages=None, can_delete_messages=None,
                 can_restrict_members=None, can_promote_members=None, can_change_info=None,
                 can_invite_users=None, can_pin_messages=None, is_member=None,
                 can_send_messages=None, can_send_media_messages=None, can_send_polls=None,
                 can_send_other_messages=None, can_add_web_page_previews=None):
        self.user = user
        self.status = status
        self.custom_title = custom_title
        self.until_date = until_date
        self.can_be_edited = can_be_edited
        self.can_post_messages = can_post_messages
        self.can_edit_messages = can_edit_messages
        self.can_delete_messages = can_delete_messages
        self.can_restrict_members = can_restrict_members
        self.can_promote_members = can_promote_members
        self.can_change_info = can_change_info
        self.can_invite_users = can_invite_users
        self.can_pin_messages = can_pin_messages
        self.is_member = is_member
        self.can_send_messages = can_send_messages
        self.can_send_media_messages = can_send_media_messages
        self.can_send_polls = can_send_polls
        self.can_send_other_messages = can_send_other_messages
        self.can_add_web_page_previews = can_add_web_page_previews


class ChatPermissions(JsonDeserializable, JsonSerializable, Dictionaryable):
    def __init__(self, can_send_messages=None, can_send_media_messages=None,
                 can_send_polls=None, can_send_other_messages=None,
                 can_add_web_page_previews=None, can_change_info=None,
                 can_invite_users=None, can_pin_messages=None):
        self.can_send_messages = can_send_messages
        self.can_send_media_messages = can_send_media_messages
        self.can_send_polls = can_send_polls
        self.can_send_other_messages = can_send_other_messages
        self.can_add_web_page_previews = can_add_web_page_previews
        self.can_change_info = can_change_info
        self.can_invite_users = can_invite_users
        self.can_pin_messages = can_pin_messages

    @classmethod
    async def de_json(cls, json_string):
        if json_string is None:
            return json_string

        obj = await cls.check_json(json_string)
        can_send_messages = obj.get('can_send_messages')
        can_send_media_messages = obj.get('can_send_media_messages')
        can_send_polls = obj.get('can_send_polls')
        can_send_other_messages = obj.get('can_send_other_messages')
        can_add_web_page_previews = obj.get('can_add_web_page_previews')
        can_change_info = obj.get('can_change_info')
        can_invite_users = obj.get('can_invite_users')
        can_pin_messages = obj.get('can_pin_messages')

        return cls(
            can_send_messages, can_send_media_messages, can_send_polls,
            can_send_other_messages, can_add_web_page_previews,
            can_change_info, can_invite_users, can_pin_messages)

    async def to_json(self):
        return json.dumps(self.to_dict())

    async def to_dict(self):
        json_dict = dict()
        if self.can_send_messages is not None:
            json_dict['can_send_messages'] = self.can_send_messages
        if self.can_send_media_messages is not None:
            json_dict['can_send_media_messages'] = self.can_send_media_messages
        if self.can_send_polls is not None:
            json_dict['can_send_polls'] = self.can_send_polls
        if self.can_send_other_messages is not None:
            json_dict['can_send_other_messages'] = self.can_send_other_messages
        if self.can_add_web_page_previews is not None:
            json_dict['can_add_web_page_previews'] = self.can_add_web_page_previews
        if self.can_change_info is not None:
            json_dict['can_change_info'] = self.can_change_info
        if self.can_invite_users is not None:
            json_dict['can_invite_users'] = self.can_invite_users
        if self.can_pin_messages is not None:
            json_dict['can_pin_messages'] = self.can_pin_messages

        return json_dict
