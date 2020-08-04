# -*- coding: utf-8 -*-

"""
Modules contains inputmedia types.

Types:
- InputMedia
- InputMediaPhoto
- InputMediaVideo
- InputMediaAnimation
- InputMediaAudio
- InputMediaDocument
"""

try:
    import ujson as json
except ImportError:
    import json

from aiotgram import util

from .base import JsonSerializable, Dictionaryable


class InputMedia(Dictionaryable, JsonSerializable):
    def __init__(self, type, media, caption=None, parse_mode=None):
        self.type = type
        self.media = media
        self.caption = caption
        self.parse_mode = parse_mode

        media_is_str = util.is_string(self.media)

        if media_is_str:
            self._media_name = ''
            self._media_dic = self.media
        else:
            self._media_name = util.generate_random_token()
            self._media_dic = 'attach://{0}'.format(self._media_name)

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        json_dict = {'type': self.type, 'media': self._media_dic}

        if self.caption:
            json_dict['caption'] = self.caption
        if self.parse_mode:
            json_dict['parse_mode'] = self.parse_mode

        return json_dict

    def convert_input_media(self):
        if util.is_string(self.media):
            return self.to_json(), None

        return self.to_json(), {self._media_name: self.media}


class InputMediaPhoto(InputMedia):
    def __init__(self, media, caption=None, parse_mode=None):
        super(InputMediaPhoto, self).__init__(type="photo", media=media, caption=caption, parse_mode=parse_mode)

    def to_dict(self):
        return super(InputMediaPhoto, self).to_dict()


class InputMediaVideo(InputMedia):
    def __init__(self, media, thumb=None, caption=None, parse_mode=None, width=None, height=None, duration=None,
                 supports_streaming=None):
        super(InputMediaVideo, self).__init__(type="video", media=media, caption=caption, parse_mode=parse_mode)
        self.thumb = thumb
        self.width = width
        self.height = height
        self.duration = duration
        self.supports_streaming = supports_streaming

    def to_dict(self):
        ret = super(InputMediaVideo, self).to_dict()

        if self.thumb:
            ret['thumb'] = self.thumb
        if self.width:
            ret['width'] = self.width
        if self.height:
            ret['height'] = self.height
        if self.duration:
            ret['duration'] = self.duration
        if self.supports_streaming:
            ret['supports_streaming'] = self.supports_streaming

        return ret


class InputMediaAnimation(InputMedia):
    def __init__(self, media, thumb=None, caption=None, parse_mode=None, width=None, height=None, duration=None):
        super(InputMediaAnimation, self).__init__(type="animation", media=media, caption=caption, parse_mode=parse_mode)
        self.thumb = thumb
        self.width = width
        self.height = height
        self.duration = duration

    def to_dict(self):
        ret = super(InputMediaAnimation, self).to_dict()

        if self.thumb:
            ret['thumb'] = self.thumb
        if self.width:
            ret['width'] = self.width
        if self.height:
            ret['height'] = self.height
        if self.duration:
            ret['duration'] = self.duration

        return ret


class InputMediaAudio(InputMedia):
    def __init__(self, media, thumb=None, caption=None, parse_mode=None, duration=None, performer=None, title=None):
        super(InputMediaAudio, self).__init__(type="audio", media=media, caption=caption, parse_mode=parse_mode)
        self.thumb = thumb
        self.duration = duration
        self.performer = performer
        self.title = title

    def to_dict(self):
        ret = super(InputMediaAudio, self).to_dict()

        if self.thumb:
            ret['thumb'] = self.thumb
        if self.duration:
            ret['duration'] = self.duration
        if self.performer:
            ret['performer'] = self.performer
        if self.title:
            ret['title'] = self.title

        return ret


class InputMediaDocument(InputMedia):
    def __init__(self, media, thumb=None, caption=None, parse_mode=None):
        super(InputMediaDocument, self).__init__(type="document", media=media, caption=caption, parse_mode=parse_mode)
        self.thumb = thumb

    def to_dict(self):
        ret = super(InputMediaDocument, self).to_dict()

        if self.thumb:
            ret['thumb'] = self.thumb

        return ret
