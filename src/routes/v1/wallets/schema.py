from marshmallow import Schema, post_dump
from webargs import fields


class FetchWalletSchema(Schema):
    member_uuid = fields.UUID(required=False)
    expand = fields.DelimitedList(fields.String(), required=False, missing=[])


class FetchAllWalletSchema(Schema):
    page = fields.Int(required=False, missing=1)
    per_page = fields.Int(required=False, missing=10)
    expand = fields.DelimitedList(fields.String(), required=False, missing=[])


class DumpWalletsSchema(Schema):
    uuid = fields.UUID()
    ctime = fields.Integer()
    mtime = fields.Integer()
    balance = fields.Integer()
    member = fields.Nested('DumpMemberSchema', include=('uuid', 'ctime', 'mtime', 'username'))

    def get_attribute(self, obj, attr, default):
        if attr == 'member':
            return getattr(obj, attr, default) if any(
                attr in expand for expand in self.context.get('expand', [])) else None
        else:
            return getattr(obj, attr, default)

    @post_dump
    def make_obj(self, data, **kwargs):
        if data.get('member', False) is None:
            del data['member']
        return data


dump_schema = DumpWalletsSchema()
dump_many_schema = DumpWalletsSchema(many=True)
fetch_schema = FetchWalletSchema()
fetch_all_schema = FetchAllWalletSchema()
