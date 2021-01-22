from marshmallow import Schema
from webargs import fields


class CreateInviteSchema(Schema):
    league_uuid = fields.UUID()
    email = fields.String()


class DumpInviteSchema(Schema):
    uuid = fields.UUID()
    ctime = fields.Integer()
    mtime = fields.Integer()
    email = fields.String()
    league_uuid = fields.UUID(missing=None)


class FetchInviteSchema(Schema):
    email = fields.String(required=False)
    league_uuid = fields.UUID(required=False)


class FetchAllInviteSchema(Schema):
    page = fields.Int(required=False, missing=1)
    per_page = fields.Int(required=False, missing=10)
    email = fields.String(required=False)
    league_uuid = fields.UUID(required=False, missing=None)


create_schema = CreateInviteSchema()
dump_schema = DumpInviteSchema()
dump_many_schema = DumpInviteSchema(many=True)
fetch_schema = FetchInviteSchema()
fetch_all_schema = FetchAllInviteSchema()
