# -*- coding: utf-8 -*-
try:
    import ujson as json
except ImportError:
    import json

from .base import JsonSerializable, JsonDeserializable
from .common import User, PhotoSize, MessageEntity


class InlineQueryResultGame(JsonSerializable):
    def __init__(self, id_, game_short_name, reply_markup=None):
        self.type = 'game'
        self.id_ = id_
        self.game_short_name = game_short_name
        self.reply_markup = reply_markup

    async def to_json(self):
        json_dic = {'type': self.type, 'id': self.id_, 'game_short_name': self.game_short_name}
        if self.reply_markup:
            json_dic['reply_markup'] = await self.reply_markup.to_dict()
        return json.dumps(json_dic)


class Game(JsonDeserializable):
    @classmethod
    async def de_json(cls, json_string):
        if json_string is None:
            return None

        obj = await cls.check_json(json_string)
        title = obj['title']
        description = obj['description']
        photo = await Game.parse_photo(obj['photo'])
        text = obj.get('text')
        text_entities = None
        if 'text_entities' in obj:
            text_entities = await Game.parse_entities(obj['text_entities'])
        animation = await Animation.de_json(obj.get('animation'))

        return cls(title, description, photo, text, text_entities, animation)

    @classmethod
    async def parse_photo(cls, photo_size_array):
        ret = []
        for photo_size in photo_size_array:
            ret.append(await PhotoSize.de_json(photo_size))
        return ret

    @classmethod
    async def parse_entities(cls, message_entity_array):
        ret = []
        for message_entity in message_entity_array:
            ret.append(await MessageEntity.de_json(message_entity))
        return ret

    def __init__(self, title, description, photo, text=None, text_entities=None, animation=None):
        self.title = title
        self.description = description
        self.photo = photo
        self.text = text
        self.text_entities = text_entities
        self.animation = animation


class Animation(JsonDeserializable):
    @classmethod
    async def de_json(cls, json_string):
        if json_string is None:
            return None

        obj = await cls.check_json(json_string)
        file_id = obj['file_id']
        thumb = await PhotoSize.de_json(obj.get('thumb'))
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


class GameHighScore(JsonDeserializable):
    @classmethod
    async def de_json(cls, json_string):
        if json_string is None:
            return None

        obj = await cls.check_json(json_string)
        position = obj['position']
        user = await User.de_json(obj['user'])
        score = obj['score']

        return cls(position, user, score)

    def __init__(self, position, user, score):
        self.position = position
        self.user = user
        self.score = score
