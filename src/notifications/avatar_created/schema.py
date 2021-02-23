from marshmallow import Schema
from webargs import fields


class AvatarCreatedSchema(Schema):
    league_uuid = fields.UUID(missing=None, attribute='member.league_uuid')
    user_uuid = fields.UUID(attribute='member.user_uuid')
    member_uuid = fields.UUID(attribute='member.uuid')
    uuid = fields.UUID(attribute='avatar.uuid')
    s3_filename = fields.Str(attribute='avatar.s3_filename')
