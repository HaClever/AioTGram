# -*- coding: utf-8 -*-
"""
Modules contains primary types.

Types:
- Dice
- Audio
- Voice
- Document
- Video
- VideoNote
- Contact
- Location
- Venue
- File
"""
try:
    import ujson as json
except ImportError:
    import json

from .base import JsonDeserializable, Dictionaryable, JsonSerializable
from .common import PhotoSize


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


class Voice(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None

        obj = cls.check_json(json_string)
        file_id = obj['file_id']
        duration = obj['duration']
        mime_type = obj.get('mime_type')
        file_size = obj.get('file_size')

        return cls(file_id, duration, mime_type, file_size)

    def __init__(self, file_id, duration, mime_type=None, file_size=None):
        self.file_id = file_id
        self.duration = duration
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


class File(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None

        obj = cls.check_json(json_string)
        file_id = obj['file_id']
        file_size = obj.get('file_size')
        file_path = obj.get('file_path')

        return cls(file_id, file_size, file_path)

    def __init__(self, file_id, file_size, file_path):
        self.file_id = file_id
        self.file_size = file_size
        self.file_path = file_path
