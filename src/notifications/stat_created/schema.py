from marshmallow import Schema, pre_dump
from webargs import fields


class StatCreatedSchema(Schema):
    league_uuid = fields.UUID(missing=None, attribute='member.league_uuid')
    user_uuid = fields.UUID(attribute='member.user_uuid')
    member_uuid = fields.UUID(attribute='stat.member_uuid')
    uuid = fields.UUID(attribute='stat.uuid')

    @pre_dump
    def prepare(self, data, **kwargs):
        stat = data['stat']
        data['member'] = stat.member
        return data
