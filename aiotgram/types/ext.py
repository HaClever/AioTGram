# -*- coding: utf-8 -*-
"""
Modules contains ext types.

Types:
- Chat
- Message
- CallbackQuery
- Poll
"""

try:
    import ujson as json
except ImportError:
    import json

from .base import JsonDeserializable

from .common import User, PhotoSize, MessageEntity
from .primary import (
    Audio, Document, Video, VideoNote,
    Contact, Location, Venue, Dice
)

from .chat import ChatPhoto, ChatPermissions, GroupChat
from .poll import PollOption
from .games import Animation, Game
from .stickers import Sticker
from .payments import Invoice, SuccessfulPayment


class Chat(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None

        obj = cls.check_json(json_string)
        id_ = obj['id']
        type_ = obj['type']
        title = obj.get('title')
        username = obj.get('username')
        first_name = obj.get('first_name')
        last_name = obj.get('last_name')
        all_members_are_administrators = obj.get('all_members_are_administrators')
        photo = ChatPhoto.de_json(obj.get('photo'))
        description = obj.get('description')
        invite_link = obj.get('invite_link')
        pinned_message = Message.de_json(obj.get('pinned_message'))
        permissions = ChatPermissions.de_json(obj.get('permissions'))
        slow_mode_delay = obj.get('slow_mode_delay')
        sticker_set_name = obj.get('sticker_set_name')
        can_set_sticker_set = obj.get('can_set_sticker_set')

        return cls(
            id_, type_, title, username, first_name, last_name,
            all_members_are_administrators, photo, description, invite_link,
            pinned_message, permissions, slow_mode_delay, sticker_set_name,
            can_set_sticker_set)

    def __init__(self, id_, type_, title=None, username=None, first_name=None,
                 last_name=None, all_members_are_administrators=None,
                 photo=None, description=None, invite_link=None,
                 pinned_message=None, permissions=None, slow_mode_delay=None,
                 sticker_set_name=None, can_set_sticker_set=None):
        self.id_ = id_
        self.type_ = type_
        self.title = title
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.all_members_are_administrators = all_members_are_administrators
        self.photo = photo
        self.description = description
        self.invite_link = invite_link
        self.pinned_message = pinned_message
        self.permissions = permissions
        self.slow_mode_delay = slow_mode_delay
        self.sticker_set_name = sticker_set_name
        self.can_set_sticker_set = can_set_sticker_set


class Message(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None

        obj = cls.check_json(json_string)
        message_id = obj['message_id']
        from_user = User.de_json(obj.get('from'))
        date = obj['date']
        chat = Chat.de_json(obj['chat'])
        content_type = None

        opts = {}
        if 'forward_from' in obj:
            opts['forward_from'] = User.de_json(obj['forward_from'])
        if 'forward_from_chat' in obj:
            opts['forward_from_chat'] = Chat.de_json(obj['forward_from_chat'])
        if 'forward_from_message_id' in obj:
            opts['forward_from_message_id'] = obj.get('forward_from_message_id')
        if 'forward_signature' in obj:
            opts['forward_signature'] = obj.get('forward_signature')
        if 'forward_date' in obj:
            opts['forward_date'] = obj.get('forward_date')
        if 'reply_to_message' in obj:
            opts['reply_to_message'] = Message.de_json(obj['reply_to_message'])
        if 'edit_date' in obj:
            opts['edit_date'] = obj.get('edit_date')
        if 'media_group_id' in obj:
            opts['media_group_id'] = obj.get('media_group_id')
        if 'author_signature' in obj:
            opts['author_signature'] = obj.get('author_signature')
        if 'text' in obj:
            opts['text'] = obj['text']
            content_type = 'text'
        if 'entities' in obj:
            opts['entities'] = Message.parse_entities(obj['entities'])
        if 'caption_entities' in obj:
            opts['caption_entities'] = Message.parse_entities(obj['caption_entities'])
        if 'audio' in obj:
            opts['audio'] = Audio.de_json(obj['audio'])
            content_type = 'audio'
        if 'animation' in obj:
            opts['animation'] = Animation.de_json(obj['animation'])
            content_type = 'animation'
        if 'document' in obj:
            opts['document'] = Document.de_json(obj['document'])
            content_type = 'document'
        if 'game' in obj:
            opts['game'] = Game.de_json(obj['game'])
            content_type = 'game'
        if 'photo' in obj:
            opts['photo'] = Message.parse_photo(obj['photo'])
            content_type = 'photo'
        if 'sticker' in obj:
            opts['sticker'] = Sticker.de_json(obj['sticker'])
            content_type = 'sticker'
        if 'video' in obj:
            opts['video'] = Video.de_json(obj['video'])
            content_type = 'video'
        if 'video_note' in obj:
            opts['video_note'] = VideoNote.de_json(obj['video_note'])
            content_type = 'video_note'
        if 'voice' in obj:
            opts['voice'] = Audio.de_json(obj['voice'])
            content_type = 'voice'
        if 'caption' in obj:
            opts['caption'] = obj['caption']
        if 'contact' in obj:
            opts['contact'] = Contact.de_json(json.dumps(obj['contact']))
            content_type = 'contact'
        if 'location' in obj:
            opts['location'] = Location.de_json(obj['location'])
            content_type = 'location'
        if 'venue' in obj:
            opts['venue'] = Venue.de_json(obj['venue'])
            content_type = 'venue'
        if 'dice' in obj:
            opts['dice'] = Dice.de_json(obj['dice'])
            content_type = 'dice'
        if 'new_chat_members' in obj:
            new_chat_members = []
            for member in obj['new_chat_members']:
                new_chat_members.append(User.de_json(member))
            opts['new_chat_members'] = new_chat_members
            content_type = 'new_chat_members'
        if 'left_chat_member' in obj:
            opts['left_chat_member'] = User.de_json(obj['left_chat_member'])
            content_type = 'left_chat_member'
        if 'new_chat_title' in obj:
            opts['new_chat_title'] = obj['new_chat_title']
            content_type = 'new_chat_title'
        if 'new_chat_photo' in obj:
            opts['new_chat_photo'] = Message.parse_photo(obj['new_chat_photo'])
            content_type = 'new_chat_photo'
        if 'delete_chat_photo' in obj:
            opts['delete_chat_photo'] = obj['delete_chat_photo']
            content_type = 'delete_chat_photo'
        if 'group_chat_created' in obj:
            opts['group_chat_created'] = obj['group_chat_created']
            content_type = 'group_chat_created'
        if 'supergroup_chat_created' in obj:
            opts['supergroup_chat_created'] = obj['supergroup_chat_created']
            content_type = 'supergroup_chat_created'
        if 'channel_chat_created' in obj:
            opts['channel_chat_created'] = obj['channel_chat_created']
            content_type = 'channel_chat_created'
        if 'migrate_to_chat_id' in obj:
            opts['migrate_to_chat_id'] = obj['migrate_to_chat_id']
            content_type = 'migrate_to_chat_id'
        if 'migrate_from_chat_id' in obj:
            opts['migrate_from_chat_id'] = obj['migrate_from_chat_id']
            content_type = 'migrate_from_chat_id'
        if 'pinned_message' in obj:
            opts['pinned_message'] = Message.de_json(obj['pinned_message'])
            content_type = 'pinned_message'
        if 'invoice' in obj:
            opts['invoice'] = Invoice.de_json(obj['invoice'])
            content_type = 'invoice'
        if 'successful_payment' in obj:
            opts['successful_payment'] = SuccessfulPayment.de_json(obj['successful_payment'])
            content_type = 'successful_payment'
        if 'connected_website' in obj:
            opts['connected_website'] = obj['connected_website']
            content_type = 'connected_website'
        if 'poll' in obj:
            opts['poll'] = Poll.de_json(obj['poll'])
            content_type = 'poll'
        if 'passport_data' in obj:
            opts['passport_data'] = obj['passport_data']
            content_type = 'passport_data'

        return cls(message_id, from_user, date, chat, content_type, opts, json_string)

    @classmethod
    def parse_chat(cls, chat):
        if 'first_name' not in chat:
            return GroupChat.de_json(chat)
        else:
            return User.de_json(chat)

    @classmethod
    def parse_photo(cls, photo_size_array):
        ret = []
        for photo_size in photo_size_array:
            ret.append(PhotoSize.de_json(photo_size))
        return ret

    @classmethod
    def parse_entities(cls, message_entity_array):
        ret = []
        for message_entity in message_entity_array:
            ret.append(MessageEntity.de_json(message_entity))
        return ret

    def __init__(self, message_id, from_user, date, chat, content_type, options, json_string):
        self.content_type = content_type
        self.message_id = message_id
        self.from_user = from_user
        self.date = date
        self.chat = chat
        self.forward_from = None
        self.forward_from_chat = None
        self.forward_from_message_id = None
        self.forward_signature = None
        self.forward_date = None
        self.reply_to_message = None
        self.edit_date = None
        self.media_group_id = None
        self.author_signature = None
        self.text = None
        self.entities = None
        self.caption_entities = None
        self.audio = None
        self.document = None
        self.photo = None
        self.sticker = None
        self.video = None
        self.video_note = None
        self.voice = None
        self.caption = None
        self.contact = None
        self.location = None
        self.venue = None
        self.animation = None
        self.dice = None
        self.new_chat_member = None  # Deprecated since Bot API 3.0. Not processed anymore
        self.new_chat_members = None
        self.left_chat_member = None
        self.new_chat_title = None
        self.new_chat_photo = None
        self.delete_chat_photo = None
        self.group_chat_created = None
        self.supergroup_chat_created = None
        self.channel_chat_created = None
        self.migrate_to_chat_id = None
        self.migrate_from_chat_id = None
        self.pinned_message = None
        self.invoice = None
        self.successful_payment = None
        self.connected_website = None
        for key in options:
            setattr(self, key, options[key])
        self.json = json_string

    def __html_text(self, text, entities):
        """
        Author: @sviat9440
        Updaters: @badiboy
        Message: "*Test* parse _formatting_, [url](https://example.com), [text_mention](tg://user?id=123456) and mention @username"
        Example:
            message.html_text
            >> "<b>Test</b> parse <i>formatting</i>, <a href=\"https://example.com\">url</a>, <a href=\"tg://user?id=123456\">text_mention</a> and mention @username"
        Cusom subs:
            You can customize the substitutes. By default, there is no substitute for the entities: hashtag, bot_command, email. You can add or modify substitute an existing entity.
        Example:
            message.custom_subs = {"bold": "<strong class=\"example\">{text}</strong>", "italic": "<i class=\"example\">{text}</i>", "mention": "<a href={url}>{text}</a>"}
            message.html_text
            >> "<strong class=\"example\">Test</strong> parse <i class=\"example\">formatting</i>, <a href=\"https://example.com\">url</a> and <a href=\"tg://user?id=123456\">text_mention</a> and mention <a href=\"https://t.me/username\">@username</a>"
        """

        if not entities:
            return text

        _subs = {
            "bold": "<b>{text}</b>",
            "italic": "<i>{text}</i>",
            "pre": "<pre>{text}</pre>",
            "code": "<code>{text}</code>",
            # "url"      : "<a href=\"{url}\">{text}</a>", # @badiboy plain URLs have no text and do not need tags
            "text_link": "<a href=\"{url}\">{text}</a>",
            "strikethrough": "<s>{text}</s>",
            "underline": "<u>{text}</u>"
        }

        if hasattr(self, "custom_subs"):
            for key, value in self.custom_subs.items():
                _subs[key] = value
        utf16_text = text.encode("utf-16-le")
        html_text = ""

        def func(upd_text, subst_type=None, url=None, user=None):
            upd_text = upd_text.decode("utf-16-le")
            if subst_type == "text_mention":
                subst_type = "url"
                url = "tg://user?id={0}".format(user.id)
            elif subst_type == "mention":
                url = "https://t.me/{0}".format(upd_text[1:])

            upd_text = upd_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            if not subst_type or not _subs.get(subst_type):
                return

            subs = _subs.get(subst_type)
            return subs.format(text=upd_text, url=url)

        offset = 0
        for entity in entities:
            if entity.offset > offset:
                html_text += func(utf16_text[offset * 2: entity.offset * 2])
                offset = entity.offset
                html_text += func(utf16_text[offset * 2: (offset + entity.length) * 2], entity.type, entity.url, entity.user)
                offset += entity.length
            elif entity.offset == offset:
                html_text += func(utf16_text[offset * 2: (offset + entity.length) * 2], entity.type, entity.url, entity.user)
                offset += entity.length
            else:
                # TODO: process nested entities from Bot API 4.5
                # Now ignoring them
                pass
        if offset * 2 < len(utf16_text):
            html_text += func(utf16_text[offset * 2:])
        return html_text

    @property
    def html_text(self):
        return self.__html_text(self.text, self.entities)

    @property
    def html_caption(self):
        return self.__html_text(self.caption, self.caption_entities)


class CallbackQuery(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None

        obj = cls.check_json(json_string)
        id_ = obj['id']
        from_user = User.de_json(obj['from'])
        message = Message.de_json(obj.get('message'))
        inline_message_id = obj.get('inline_message_id')
        chat_instance = obj['chat_instance']
        data = obj.get('data')
        game_short_name = obj.get('game_short_name')

        return cls(id_, from_user, data, chat_instance, message, inline_message_id, game_short_name)

    def __init__(self, id_, from_user, data, chat_instance, message=None, inline_message_id=None, game_short_name=None):
        self.game_short_name = game_short_name
        self.chat_instance = chat_instance
        self.id_ = id_
        self.from_user = from_user
        self.message = message
        self.data = data
        self.inline_message_id = inline_message_id


class Poll(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None

        obj = cls.check_json(json_string)
        poll_id = obj['id']
        question = obj['question']
        options = []
        for opt in obj['options']:
            options.append(PollOption.de_json(opt))
        total_voter_count = obj['total_voter_count']
        is_closed = obj['is_closed']
        is_anonymous = obj['is_anonymous']
        poll_type = obj['type']
        allows_multiple_answers = obj['allows_multiple_answers']
        correct_option_id = obj.get('correct_option_id')
        explanation = obj.get('explanation')
        if 'explanation_entities' in obj:
            explanation_entities = Message.parse_entities(obj['explanation_entities'])
        else:
            explanation_entities = None

        open_period = obj.get('open_period')
        close_date = obj.get('close_date')
        # poll =

        return cls(
            question, options,
            poll_id, total_voter_count, is_closed, is_anonymous, poll_type,
            allows_multiple_answers, correct_option_id, explanation, explanation_entities,
            open_period, close_date)

    def __init__(
            self,
            question, options,
            poll_id=None, total_voter_count=None, is_closed=None, is_anonymous=None, poll_type=None,
            allows_multiple_answers=None, correct_option_id=None, explanation=None, explanation_entities=None,
            open_period=None, close_date=None):
        self.id_ = poll_id
        self.question = question
        self.options = options
        self.total_voter_count = total_voter_count
        self.is_closed = is_closed
        self.is_anonymous = is_anonymous
        self.type = poll_type
        self.allows_multiple_answers = allows_multiple_answers
        self.correct_option_id = correct_option_id
        self.explanation = explanation
        self.explanation_entities = explanation_entities if not(explanation_entities is None) else []
        self.open_period = open_period
        self.close_date = close_date

    def add(self, option):
        if isinstance(option, PollOption):
            self.options.append(option)
        else:
            self.options.append(PollOption(option))
