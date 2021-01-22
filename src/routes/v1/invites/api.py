from flask import request
from flask_restful import marshal_with

from .schema import *
from ..base import Base
from ....common.response import DataResponse
from ....services import InviteService


class InvitesAPI(Base):
    def __init__(self):
        Base.__init__(self)
        self.invite = InviteService()

    @marshal_with(DataResponse.marshallable())
    def get(self, uuid):
        data = self.clean(schema=fetch_schema, instance=request.args)
        invites = self.invite.find(uuid=uuid, **data)
        if not invites.total:
            self.throw_error(http_code=self.code.NOT_FOUND)
        return DataResponse(
            data={
                'invites': self.dump(
                    schema=dump_schema,
                    instance=invites.items[0],
                    params={
                        'include': data['include']
                    }
                )
            }
        )


class InvitesListAPI(Base):
    def __init__(self):
        Base.__init__(self)
        self.invite = InviteService()

    @marshal_with(DataResponse.marshallable())
    def get(self):
        data = self.clean(schema=fetch_all_schema, instance=request.args)
        invites = self.invite.find(**data)
        return DataResponse(
            data={
                '_metadata': self.prepare_metadata(
                    total_count=invites.total,
                    page_count=len(invites.items),
                    page=data['page'],
                    per_page=data['per_page'],
                    search=data['search']),
                'invites': self.dump(
                    schema=dump_many_schema,
                    instance=invites.items,
                    params={
                        'include': data['include']
                    }
                )
            }
        )

    @marshal_with(DataResponse.marshallable())
    def post(self):
        data = self.clean(schema=create_schema, instance=request.get_json())
        invite = self.invite.create(**data)
        return DataResponse(
            data={
                'invites': self.dump(
                    schema=dump_schema,
                    instance=invite
                )
            }
        )
