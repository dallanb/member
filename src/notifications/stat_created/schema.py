from marshmallow import Schema
from webargs import fields


class StatCreatedSchema(Schema):
    member_uuid = fields.UUID(attribute='stat.member_uuid')
    uuid = fields.UUID(attribute='stat.uuid')
