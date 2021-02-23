from marshmallow import Schema
from webargs import fields


class DisplayNameUpdatedSchema(Schema):
    uuid = fields.UUID(attribute='member.uuid')
    user_uuid = fields.UUID(attribute='member.user_uuid')
    league_uuid = fields.UUID(attribute='member.league_uuid', missing=None)
    display_name = fields.String(attribute='member.display_name')
