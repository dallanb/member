from flask import request
from flask_restful import marshal_with

from .schema import *
from ..base import Base
from ....common.auth import assign_user
from ....common.response import DataResponse
from ....services import MemberService


class MembersAPI(Base):
    def __init__(self):
        Base.__init__(self)
        self.member = MemberService()

    @marshal_with(DataResponse.marshallable())
    def get(self, uuid):
        data = self.clean(schema=fetch_schema, instance=request.args)
        members = self.member.find(uuid=uuid, **data)
        if not members.total:
            self.throw_error(http_code=self.code.NOT_FOUND)
        return DataResponse(
            data={
                'members': self.dump(
                    schema=dump_schema,
                    instance=members.items[0],
                    params={
                        'include': data['include']
                    }
                )
            }
        )

    @marshal_with(DataResponse.marshallable())
    def put(self, uuid):
        data = self.clean(schema=update_schema, instance=request.get_json())
        member = self.member.update(uuid=uuid, **data)
        return DataResponse(
            data={
                'members': self.dump(
                    schema=dump_schema,
                    instance=member
                )
            }
        )


class MembersUserAPI(Base):
    def __init__(self):
        Base.__init__(self)
        self.member = MemberService()

    @marshal_with(DataResponse.marshallable())
    @assign_user
    def get(self, user_uuid):
        data = self.clean(schema=fetch_schema, instance={**request.args,
                                                         'user_uuid': user_uuid})  # not cleaning user_uuid at base request level so make sure it is cleaned here
        members = self.member.find(**data)
        if not members.total:
            self.throw_error(http_code=self.code.NOT_FOUND)
        return DataResponse(
            data={
                'members': self.dump(
                    schema=dump_schema,
                    instance=members.items[0],
                    params={
                        'include': data['include']
                    }
                )
            }
        )


class MembersListAPI(Base):
    def __init__(self):
        Base.__init__(self)
        self.member = MemberService()

    @marshal_with(DataResponse.marshallable())
    def get(self):
        data = self.clean(schema=fetch_all_schema, instance=request.args)
        members = self.member.find(**data)
        return DataResponse(
            data={
                '_metadata': self.prepare_metadata(
                    total_count=members.total,
                    page_count=len(members.items),
                    page=data['page'],
                    per_page=data['per_page']),
                'members': self.dump(
                    schema=dump_many_schema,
                    instance=members.items,
                    params={
                        'include': data['include']
                    }
                )
            }
        )


class MembersListBulkAPI(Base):
    def __init__(self):
        Base.__init__(self)
        self.member = MemberService()

    @marshal_with(DataResponse.marshallable())
    def post(self):
        data = self.clean(schema=bulk_schema, instance={**request.get_json(), **request.args.to_dict()})
        members = self.member.find(**data)
        return DataResponse(
            data={
                '_metadata': self.prepare_metadata(
                    total_count=members.total,
                    page_count=len(members.items),
                    page=data['page'],
                    per_page=data['per_page']),
                'members': self.dump(
                    schema=dump_many_schema,
                    instance=members.items,
                    params={
                        'include': data['include']
                    }
                )
            }
        )
