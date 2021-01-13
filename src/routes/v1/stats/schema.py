from marshmallow import Schema, post_dump
from webargs import fields

# from ..members.schema import DumpMemberSchema


class FetchStatSchema(Schema):
    expand = fields.DelimitedList(fields.String(), required=False, missing=[])


class FetchAllStatSchema(Schema):
    page = fields.Int(required=False, missing=1)
    per_page = fields.Int(required=False, missing=10)
    expand = fields.DelimitedList(fields.String(), required=False, missing=[])


class DumpStatsSchema(Schema):
    uuid = fields.UUID()
    ctime = fields.Integer()
    mtime = fields.Integer()
    win_count = fields.Integer()
    winning_total = fields.Integer()
    event_count = fields.Integer()
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


dump_schema = DumpStatsSchema()
dump_many_schema = DumpStatsSchema(many=True)
fetch_schema = FetchStatSchema()
fetch_all_schema = FetchAllStatSchema()
