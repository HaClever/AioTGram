# -*- coding: utf-8 -*-

"""
Modules contains payments types.

Types:
- LabeledPrice
- Invoice
- ShippingAddress
- OrderInfo
- ShippingOption
- SuccessfulPayment
- ShippingQuery
- PreCheckoutQuery
"""

try:
    import ujson as json
except ImportError:
    import json

from .base import JsonSerializable, JsonDeserializable
from .common import User


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
    def __init__(self, id, title):
        self.id = id
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
        for price in self.prices:
            price_list.append(price.to_dict())
        json_dict = json.dumps({'id': self.id, 'title': self.title, 'prices': price_list})
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
        id = obj['id']
        from_user = User.de_json(obj['from'])
        invoice_payload = obj['invoice_payload']
        shipping_address = ShippingAddress.de_json(obj['shipping_address'])

        return cls(id, from_user, invoice_payload, shipping_address)

    def __init__(self, id, from_user, invoice_payload, shipping_address):
        self.id = id
        self.from_user = from_user
        self.invoice_payload = invoice_payload
        self.shipping_address = shipping_address


class PreCheckoutQuery(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None

        obj = cls.check_json(json_string)
        id = obj['id']
        from_user = User.de_json(obj['from'])
        currency = obj['currency']
        total_amount = obj['total_amount']
        invoice_payload = obj['invoice_payload']
        shipping_option_id = obj.get('shipping_option_id')
        order_info = OrderInfo.de_json(obj.get('order_info'))

        return cls(id, from_user, currency, total_amount, invoice_payload, shipping_option_id, order_info)

    def __init__(self, id, from_user, currency, total_amount, invoice_payload, shipping_option_id, order_info):
        self.id = id
        self.from_user = from_user
        self.currency = currency
        self.total_amount = total_amount
        self.invoice_payload = invoice_payload
        self.shipping_option_id = shipping_option_id
        self.order_info = order_info
