from marshmallow import Schema
from webargs import fields


class StatUpdatedSchema(Schema):
    member_uuid = fields.UUID(attribute='stat.member_uuid')
    uuid = fields.UUID(attribute='stat.uuid')
