from marshmallow import Schema, post_dump, post_load
from marshmallow_enum import EnumField
from webargs import fields

from ..avatars.schema import DumpAvatarSchema
from ..stats.schema import DumpStatsSchema
from ..wallets.schema import DumpWalletsSchema
from ....common import StatusEnum


class DumpMemberSchema(Schema):
    uuid = fields.UUID()
    ctime = fields.Integer()
    mtime = fields.Integer()
    user_uuid = fields.UUID()
    league_uuid = fields.UUID(missing=None)
    email = fields.String()
    username = fields.String()
    display_name = fields.String()
    country = fields.String()
    status = EnumField(StatusEnum)
    avatar = fields.Nested(DumpAvatarSchema)
    stat = fields.Nested(DumpStatsSchema)
    wallet = fields.Nested(DumpWalletsSchema)

    def get_attribute(self, obj, attr, default):
        if attr == 'avatar':
            return getattr(obj, attr, default) or {} if any(
                attr in include for include in self.context.get('include', [])) else None
        if attr == 'stat':
            return getattr(obj, attr, default) or {} if any(
                attr in include for include in self.context.get('include', [])) else None
        if attr == 'wallet':
            return getattr(obj, attr, default) or {} if any(
                attr in include for include in self.context.get('include', [])) else None
        else:
            return getattr(obj, attr, default)

    @post_dump
    def make_obj(self, data, **kwargs):
        if data.get('avatar', False) is None:
            del data['avatar']
        if data.get('stat', False) is None:
            del data['stat']
        if data.get('wallet', False) is None:
            del data['wallet']
        return data


class UpdateMemberSchema(Schema):
    display_name = fields.Str(required=False)


class FetchMemberSchema(Schema):
    user_uuid = fields.UUID(required=False)
    league_uuid = fields.UUID(required=False, missing=None)
    include = fields.DelimitedList(fields.String(), required=False, missing=[])


class FetchAllMemberSchema(Schema):
    page = fields.Int(required=False, missing=1)
    per_page = fields.Int(required=False, missing=10)
    include = fields.DelimitedList(fields.String(), required=False, missing=[])
    search = fields.String(required=False, missing=None)
    user_uuid = fields.UUID(required=False)
    email = fields.Email(required=False)
    league_uuid = fields.UUID(required=False, missing=None)
    status = fields.Str(required=False)


class FetchAllMemberStandingsSchema(Schema):
    # page = fields.Int(required=False, missing=1)
    # per_page = fields.Int(required=False, missing=10)
    sort_by = fields.String(required=False)
    include = fields.DelimitedList(fields.String(), required=False, missing=[])
    league_uuid = fields.UUID(required=False, missing=None)
    status = fields.String(required=False)


class _BulkMemberWithinSchema(Schema):
    key = fields.String(required=True)
    value = fields.List(fields.String(), required=True)

    @post_load
    def clean_within(self, in_data, **kwargs):
        return {in_data['key']: in_data['value']}


class BulkMemberSchema(Schema):
    page = fields.Int(required=False, missing=1)
    per_page = fields.Int(required=False, missing=10)
    within = fields.Nested(_BulkMemberWithinSchema)
    include = fields.DelimitedList(fields.String(), required=False, missing=[])


dump_schema = DumpMemberSchema()
dump_many_schema = DumpMemberSchema(many=True)
update_schema = UpdateMemberSchema()
fetch_schema = FetchMemberSchema()
fetch_all_schema = FetchAllMemberSchema()
fetch_all_standings_schema = FetchAllMemberStandingsSchema()
bulk_schema = BulkMemberSchema()
