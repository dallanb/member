from marshmallow import Schema
from webargs import fields


class WalletUpdatedSchema(Schema):
    member_uuid = fields.UUID(attribute='wallet.member_uuid')
    uuid = fields.UUID(attribute='wallet.uuid')
    balance = fields.Float(attribute='wallet.balance')
