# -*- coding: utf-8 -*-
try:
    import ujson as json
except ImportError:
    import json

from abc import ABCMeta, abstractmethod


class Dictionaryable(metaclass=ABCMeta):
    @abstractmethod
    async def to_dict(self):
        pass


class JsonSerializable(metaclass=ABCMeta):
    @abstractmethod
    async def to_json(self):
        pass


class JsonDeserializable(metaclass=ABCMeta):
    """
    Subclasses of this class are guaranteed to be able to be created from a json-style dict or json formatted string.
    All subclasses of this class must override de_json.
    """

    @classmethod
    @abstractmethod
    def de_json(cls, json_string):
        """
        Returns an instance of this class from the given json dict or string.
        This function must be overridden by subclasses.
        :return: an instance of this class created from the given json dict or string.
        """
        pass

    @staticmethod
    def check_json(json_type):
        """
        Checks whether json_type is a dict or a string. If it is already a dict, it is returned as-is.
        If it is not, it is converted to a dict by means of json.loads(json_type)
        :param json_type:
        :return:
        """
        if isinstance(json_type, dict):
            return json_type
        elif isinstance(json_type, str):
            return json.loads(json_type)
        else:
            raise ValueError("json_type should be a json dict or string.")

    def __str__(self):
        # FIXME: в душе не ебу что это делает
        # d = {}
        # for x, y in six.iteritems(self.__dict__):
        #     if hasattr(y, '__dict__'):
        #         d[x] = y.__dict__
        #     else:
        #         d[x] = y

        # return six.text_type(d)
        pass


class Update(JsonDeserializable):
    # TODO: Require to add *_query objects

    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None

        obj = cls.check_json(json_string)
        update_id = obj['update_id']
        message = Message.de_json(obj.get('message'))
        edited_message = Message.de_json(obj.get('edited_message'))
        channel_post = Message.de_json(obj.get('channel_post'))
        edited_channel_post = Message.de_json(obj.get('edited_channel_post'))

        return cls(update_id, message, edited_message, channel_post, edited_channel_post)

    def __init__(self, update_id, message, edited_message, channel_post, edited_channel_post):
        self.update_id = update_id
        self.message = message
        self.edited_message = edited_message
        self.channel_post = channel_post
        self.edited_channel_post = edited_channel_post


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

    def __init__(self, id_, is_bot, first_name, last_name=None, username=None, 
                 language_code=None, can_join_groups=None, can_read_all_group_messages=None, 
                 supports_inline_queries=None):
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


class GroupChat(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None

        obj = cls.check_json(json_string)
        id_ = obj['id']
        title = obj['title']

        return cls(id_, title)

    def __init__(self, id_, title):
        self.id_ = id_
        self.title = title


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
    # TODO: require to add __html_text

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
        for me in message_entity_array:
            ret.append(MessageEntity.de_json(me))
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


class ReplyKeyboardRemove(JsonSerializable):
    def __init__(self):
        pass

    async def to_json(self):
        return json.dumps(
            {'remove_keyboard': True}
        )


class ReplyKeyboardMarkup(JsonSerializable):
    def __init__(self):
        self.keyboard = []

    async def add(self, *args):
        row = []

        for button in args:
            btn = await button.to_dict()
            row.append(btn)

        self.keyboard.append(row)

    async def to_json(self):
        return json.dumps(
            {'keyboard': self.keyboard}
        )


class KeyboardButton(Dictionaryable, JsonSerializable):
    def __init__(self, text):
        self.text = text

    async def to_json(self):
        pass

    async def to_dict(self):
        return {'text': self.text}


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


class Dice(JsonSerializable, Dictionaryable, JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None

        obj = cls.check_json(json_string)
        value = obj['value']
        emoji = obj['emoji']

        return cls(value, emoji)

    def __init__(self, value, emoji):
        self.value = value
        self.emoji = emoji

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {'value': self.value,
                'emoji': self.emoji}


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


class Audio(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None

        obj = cls.check_json(json_string)
        file_id = obj['file_id']
        duration = obj['duration']
        performer = obj.get('performer')
        title = obj.get('title')
        mime_type = obj.get('mime_type')
        file_size = obj.get('file_size')

        return cls(file_id, duration, performer, title, mime_type, file_size)

    def __init__(self, file_id, duration, performer=None, title=None, mime_type=None, file_size=None):
        self.file_id = file_id
        self.duration = duration
        self.performer = performer
        self.title = title
        self.mime_type = mime_type
        self.file_size = file_size


class Animation(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None

        obj = cls.check_json(json_string)
        file_id = obj['file_id']
        thumb = PhotoSize.de_json(obj.get('thumb'))
        file_name = obj.get('file_name')
        mime_type = obj.get('mime_type')
        file_size = obj.get('file_size')

        return cls(file_id, thumb, file_name, mime_type, file_size)

    def __init__(self, file_id, thumb=None, file_name=None, mime_type=None, file_size=None):
        self.file_id = file_id
        self.thumb = thumb
        self.file_name = file_name
        self.mime_type = mime_type
        self.file_size = file_size


class Document(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None

        obj = cls.check_json(json_string)
        file_id = obj['file_id']
        thumb = None
        if 'thumb' in obj and 'file_id' in obj['thumb']:
            thumb = PhotoSize.de_json(obj['thumb'])

        file_name = obj.get('file_name')
        mime_type = obj.get('mime_type')
        file_size = obj.get('file_size')

        return cls(file_id, thumb, file_name, mime_type, file_size)

    def __init__(self, file_id, thumb=None, file_name=None, mime_type=None, file_size=None):
        self.file_id = file_id
        self.thumb = thumb
        self.file_name = file_name
        self.mime_type = mime_type
        self.file_size = file_size


class Video(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None

        obj = cls.check_json(json_string)
        file_id = obj['file_id']
        width = obj['width']
        height = obj['height']
        duration = obj['duration']
        thumb = PhotoSize.de_json(obj.get('thumb'))
        mime_type = obj.get('mime_type')
        file_size = obj.get('file_size')

        return cls(file_id, width, height, duration, thumb, mime_type, file_size)

    def __init__(self, file_id, width, height, duration, thumb=None, mime_type=None, file_size=None):
        self.file_id = file_id
        self.width = width
        self.height = height
        self.duration = duration
        self.thumb = thumb
        self.mime_type = mime_type
        self.file_size = file_size


class VideoNote(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None

        obj = cls.check_json(json_string)
        file_id = obj['file_id']
        length = obj['length']
        duration = obj['duration']
        thumb = PhotoSize.de_json(obj.get('thumb'))
        file_size = obj.get('file_size')

        return cls(file_id, length, duration, thumb, file_size)

    def __init__(self, file_id, length, duration, thumb=None, file_size=None):
        self.file_id = file_id
        self.length = length
        self.duration = duration
        self.thumb = thumb
        self.file_size = file_size


class Contact(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None

        obj = cls.check_json(json_string)
        phone_number = obj['phone_number']
        first_name = obj['first_name']
        last_name = obj.get('last_name')
        user_id = obj.get('user_id')

        return cls(phone_number, first_name, last_name, user_id)

    def __init__(self, phone_number, first_name, last_name=None, user_id=None):
        self.phone_number = phone_number
        self.first_name = first_name
        self.last_name = last_name
        self.user_id = user_id


class Location(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None

        obj = cls.check_json(json_string)
        longitude = obj['longitude']
        latitude = obj['latitude']

        return cls(longitude, latitude)

    def __init__(self, longitude, latitude):
        self.longitude = longitude
        self.latitude = latitude


class Venue(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None

        obj = cls.check_json(json_string)
        location = Location.de_json(obj['location'])
        title = obj['title']
        address = obj['address']
        foursquare_id = obj.get('foursquare_id')

        return cls(location, title, address, foursquare_id)

    def __init__(self, location, title, address, foursquare_id=None):
        self.location = location
        self.title = title
        self.address = address
        self.foursquare_id = foursquare_id


class ChatPhoto(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None

        obj = cls.check_json(json_string)
        small_file_id = obj['small_file_id']
        big_file_id = obj['big_file_id']

        return cls(small_file_id, big_file_id)

    def __init__(self, small_file_id, big_file_id):
        self.small_file_id = small_file_id
        self.big_file_id = big_file_id


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
    def de_json(cls, json_string):
        if json_string is None:
            return json_string

        obj = cls.check_json(json_string)
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

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
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


# Stickers

class StickerSet(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None

        obj = cls.check_json(json_string)
        name = obj['name']
        title = obj['title']
        contains_masks = obj['contains_masks']
        stickers = []

        for o_sticker in obj['stickers']:
            stickers.append(Sticker.de_json(o_sticker))

        return cls(name, title, contains_masks, stickers)

    def __init__(self, name, title, contains_masks, stickers):
        self.stickers = stickers
        self.contains_masks = contains_masks
        self.title = title
        self.name = name


class Sticker(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None

        obj = cls.check_json(json_string)
        file_id = obj['file_id']
        file_unique_id = obj['file_unique_id']
        width = obj['width']
        height = obj['height']
        is_animated = obj['is_animated']
        thumb = PhotoSize.de_json(obj.get('thumb'))
        emoji = obj.get('emoji')
        set_name = obj.get('set_name')
        mask_position = MaskPosition.de_json(obj.get('mask_position'))
        file_size = obj.get('file_size')

        return cls(file_id, file_unique_id, width, height, thumb, emoji, set_name, mask_position, file_size, is_animated)

    def __init__(self, file_id, file_unique_id, width, height, thumb, emoji, set_name, mask_position, file_size, is_animated):
        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.width = width
        self.height = height
        self.thumb = thumb
        self.emoji = emoji
        self.set_name = set_name
        self.mask_position = mask_position
        self.file_size = file_size
        self.is_animated = is_animated


class MaskPosition(Dictionaryable, JsonDeserializable, JsonSerializable):
    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None

        obj = cls.check_json(json_string)
        point = obj['point']
        x_shift = obj['x_shift']
        y_shift = obj['y_shift']
        scale = obj['scale']

        return cls(point, x_shift, y_shift, scale)

    def __init__(self, point, x_shift, y_shift, scale):
        self.point = point
        self.x_shift = x_shift
        self.y_shift = y_shift
        self.scale = scale

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {'point': self.point, 'x_shift': self.x_shift, 'y_shift': self.y_shift, 'scale': self.scale}


# Games

class Game(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None

        obj = cls.check_json(json_string)
        title = obj['title']
        description = obj['description']
        photo = Game.parse_photo(obj['photo'])
        text = obj.get('text')

        text_entities = None
        if 'text_entities' in obj:
            text_entities = Game.parse_entities(obj['text_entities'])

        animation = Animation.de_json(obj.get('animation'))
        return cls(title, description, photo, text, text_entities, animation)

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

    def __init__(self, title, description, photo, text=None, text_entities=None, animation=None):
        self.title = title
        self.description = description
        self.photo = photo
        self.text = text
        self.text_entities = text_entities
        self.animation = animation


# Payments

class LabeledPrice(JsonSerializable):
    def __init__(self, label, amount):
        self.label = label
        self.amount = amount

    def to_json(self):
        return json.dumps({
            'label': self.label, 'amount': self.amount
        })


class Invoice(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None

        obj = cls.check_json(json_string)
        title = obj['title']
        description = obj['description']
        start_parameter = obj['start_parameter']
        currency = obj['currency']
        total_amount = obj['total_amount']

        return cls(title, description, start_parameter, currency, total_amount)

    def __init__(self, title, description, start_parameter, currency, total_amount):
        self.title = title
        self.description = description
        self.start_parameter = start_parameter
        self.currency = currency
        self.total_amount = total_amount


class ShippingAddress(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None

        obj = cls.check_json(json_string)
        country_code = obj['country_code']
        state = obj['state']
        city = obj['city']
        street_line1 = obj['street_line1']
        street_line2 = obj['street_line2']
        post_code = obj['post_code']

        return cls(country_code, state, city, street_line1, street_line2, post_code)

    def __init__(self, country_code, state, city, street_line1, street_line2, post_code):
        self.country_code = country_code
        self.state = state
        self.city = city
        self.street_line1 = street_line1
        self.street_line2 = street_line2
        self.post_code = post_code


class OrderInfo(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None

        obj = cls.check_json(json_string)
        name = obj.get('name')
        phone_number = obj.get('phone_number')
        email = obj.get('email')
        shipping_address = ShippingAddress.de_json(obj.get('shipping_address'))

        return cls(name, phone_number, email, shipping_address)

    def __init__(self, name, phone_number, email, shipping_address):
        self.name = name
        self.phone_number = phone_number
        self.email = email
        self.shipping_address = shipping_address


class ShippingOption(JsonSerializable):
    def __init__(self, id_, title):
        self.id_ = id_
        self.title = title
        self.prices = []

    def add_price(self, *args):
        """
        Add LabeledPrice to ShippingOption
        :param args: LabeledPrices
        """
        for price in args:
            self.prices.append(price)
        return self

    def to_json(self):
        price_list = []
        for p in self.prices:
            price_list.append(p.to_dict())

        json_dict = json.dumps({'id': self.id_, 'title': self.title, 'prices': price_list})
        return json_dict


class SuccessfulPayment(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None

        obj = cls.check_json(json_string)
        currency = obj['currency']
        total_amount = obj['total_amount']
        invoice_payload = obj['invoice_payload']
        shipping_option_id = obj.get('shipping_option_id')
        order_info = OrderInfo.de_json(obj.get('order_info'))
        telegram_payment_charge_id = obj['telegram_payment_charge_id']
        provider_payment_charge_id = obj['provider_payment_charge_id']

        return cls(currency, total_amount, invoice_payload, shipping_option_id, order_info,
                   telegram_payment_charge_id, provider_payment_charge_id)

    def __init__(self, currency, total_amount, invoice_payload, shipping_option_id, order_info,
                 telegram_payment_charge_id, provider_payment_charge_id):
        self.currency = currency
        self.total_amount = total_amount
        self.invoice_payload = invoice_payload
        self.shipping_option_id = shipping_option_id
        self.order_info = order_info
        self.telegram_payment_charge_id = telegram_payment_charge_id
        self.provider_payment_charge_id = provider_payment_charge_id


class ShippingQuery(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None

        obj = cls.check_json(json_string)
        id_ = obj['id']
        from_user = User.de_json(obj['from'])
        invoice_payload = obj['invoice_payload']
        shipping_address = ShippingAddress.de_json(obj['shipping_address'])

        return cls(id_, from_user, invoice_payload, shipping_address)

    def __init__(self, id_, from_user, invoice_payload, shipping_address):
        self.id_ = id_
        self.from_user = from_user
        self.invoice_payload = invoice_payload
        self.shipping_address = shipping_address


class PreCheckoutQuery(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None

        obj = cls.check_json(json_string)
        id_ = obj['id']
        from_user = User.de_json(obj['from'])
        currency = obj['currency']
        total_amount = obj['total_amount']
        invoice_payload = obj['invoice_payload']
        shipping_option_id = obj.get('shipping_option_id')
        order_info = OrderInfo.de_json(obj.get('order_info'))

        return cls(id_, from_user, currency, total_amount, invoice_payload, shipping_option_id, order_info)

    def __init__(self, id_, from_user, currency, total_amount, invoice_payload, shipping_option_id, order_info):
        self.id_ = id_
        self.from_user = from_user
        self.currency = currency
        self.total_amount = total_amount
        self.invoice_payload = invoice_payload
        self.shipping_option_id = shipping_option_id
        self.order_info = order_info


# InputMedia

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
        if type(option) is PollOption:
            self.options.append(option)
        else:
            self.options.append(PollOption(option))


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
