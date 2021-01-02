from marshmallow import Schema, post_dump
from marshmallow_enum import EnumField
from webargs import fields

from ..avatars.schema import DumpAvatarSchema
from ....common import StatusEnum






class CreateMemberSchema(Schema):
    user_uuid = fields.UUID()
    league_uuid = fields.UUID(missing=None)


class DumpMemberSchema(Schema):
    uuid = fields.UUID()
    ctime = fields.Integer()
    mtime = fields.Integer()
    user_uuid = fields.UUID()
    league_uuid = fields.UUID(missing=None)
    status = EnumField(StatusEnum)
    avatar = fields.Nested(DumpAvatarSchema)

    def get_attribute(self, obj, attr, default):
        if attr == 'avatar':
            return getattr(obj, attr, default) or {} if any(
                attr in include for include in self.context.get('include', [])) else None
        else:
            return getattr(obj, attr, default)

    @post_dump
    def make_obj(self, data, **kwargs):
        if data.get('avatar', False) is None:
            del data['avatar']
        return data


class UpdateMemberSchema(Schema):
    status = fields.Str(required=True)


class FetchMemberSchema(Schema):
    user_uuid = fields.UUID(required=False)
    league_uuid = fields.UUID(required=False, missing=None)
    include = fields.DelimitedList(fields.String(), required=False, missing=[])


class FetchAllMemberSchema(Schema):
    page = fields.Int(required=False, missing=1)
    per_page = fields.Int(required=False, missing=10)
    include = fields.DelimitedList(fields.String(), required=False, missing=[])
    user_uuid = fields.UUID(required=False)
    league_uuid = fields.UUID(required=False, missing=None)


create_schema = CreateMemberSchema()
dump_schema = DumpMemberSchema()
dump_many_schema = DumpMemberSchema(many=True)
update_schema = UpdateMemberSchema()
fetch_schema = FetchMemberSchema()
fetch_all_schema = FetchAllMemberSchema()
