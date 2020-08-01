# -*- coding: utf-8 -*-
try:
    import ujson as json
except ImportError:
    import json

from .base import JsonSerializable, JsonDeserializable, Dictionaryable
from .common import PhotoSize


class StickerSet(JsonDeserializable):
    @classmethod
    async def de_json(cls, json_string):
        if json_string is None:
            return None

        obj = await cls.check_json(json_string)
        name = obj['name']
        title = obj['title']
        contains_masks = obj['contains_masks']

        stickers = []
        for sticker in obj['stickers']:
            stickers.append(await Sticker.de_json(sticker))

        return cls(name, title, contains_masks, stickers)

    def __init__(self, name, title, contains_masks, stickers):
        self.stickers = stickers
        self.contains_masks = contains_masks
        self.title = title
        self.name = name


class Sticker(JsonDeserializable):
    @classmethod
    async def de_json(cls, json_string):
        if json_string is None:
            return None

        obj = await cls.check_json(json_string)
        file_id = obj['file_id']
        file_unique_id = obj['file_unique_id']
        width = obj['width']
        height = obj['height']
        is_animated = obj['is_animated']
        thumb = await PhotoSize.de_json(obj.get('thumb'))
        emoji = obj.get('emoji')
        set_name = obj.get('set_name')
        mask_position = await MaskPosition.de_json(obj.get('mask_position'))
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
    async def de_json(cls, json_string):
        if json_string is None:
            return None

        obj = await cls.check_json(json_string)
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

    async def to_json(self):
        return json.dumps(await self.to_dict())

    async def to_dict(self):
        return {'point': self.point, 'x_shift': self.x_shift, 'y_shift': self.y_shift, 'scale': self.scale}
