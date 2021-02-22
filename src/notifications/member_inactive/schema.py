from marshmallow import Schema, pre_dump
from webargs import fields


class MemberInactiveSchema(Schema):
    uuid = fields.UUID(attribute='member.uuid')
    league_uuid = fields.UUID(attribute='member.league_uuid', missing=None)
    user_uuid = fields.UUID(attribute='member.user_uuid')
    email = fields.String(attribute='member.email')

    @pre_dump
    def prepare(self, data, **kwargs):
        data['message'] = ''
        return data
