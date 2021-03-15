from marshmallow import Schema, pre_dump
from webargs import fields


class WalletUpdatedSchema(Schema):
    league_uuid = fields.UUID(missing=None, attribute='member.league_uuid')
    user_uuid = fields.UUID(attribute='member.user_uuid')
    member_uuid = fields.UUID(attribute='wallet.member_uuid')
    uuid = fields.UUID(attribute='wallet.uuid')
    balance = fields.Float(attribute='wallet.balance')

    @pre_dump
    def prepare(self, data, **kwargs):
        wallet = data['wallet']
        data['member'] = wallet.member
        return data
