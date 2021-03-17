from marshmallow import Schema, pre_dump
from webargs import fields

from src import services


class CountryUpdatedSchema(Schema):
    uuid = fields.UUID(attribute='member.uuid')
    user_uuid = fields.UUID(attribute='member.user_uuid')
    country = fields.String(attribute='member.country')

    @pre_dump
    def prepare(self, data, **kwargs):
        user_uuid = data['uuid']
        members = services.MemberService().find(user_uuid=user_uuid)
        data['member'] = members.items[0]
        return data
