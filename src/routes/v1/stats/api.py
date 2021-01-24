from flask import request
from flask_restful import marshal_with

from .schema import *
from ..base import Base
from ....common.response import DataResponse
from ....services import StatService


class StatsAPI(Base):
    def __init__(self):
        Base.__init__(self)
        self.stat = StatService()

    @marshal_with(DataResponse.marshallable())
    def get(self, uuid):
        data = self.clean(schema=fetch_schema, instance=request.args)
        stats = self.stat.find(uuid=uuid, **data)
        if not stats.total:
            self.throw_error(http_code=self.code.NOT_FOUND)
        return DataResponse(
            data={
                'stats': self.dump(
                    schema=dump_schema,
                    instance=stats.items[0],
                    params={
                        'expand': data['expand']
                    }
                )
            }
        )


class StatsMemberAPI(Base):
    def __init__(self):
        Base.__init__(self)
        self.stat = StatService()

    @marshal_with(DataResponse.marshallable())
    def get(self, member_uuid):
        data = self.clean(schema=fetch_schema, instance={**request.args,
                                                         'member_uuid': member_uuid})  # not cleaning user_uuid at base request level so make sure it is cleaned here
        stats = self.stat.find(**data)
        if not stats.total:
            self.throw_error(http_code=self.code.NOT_FOUND)
        return DataResponse(
            data={
                'stats': self.dump(
                    schema=dump_schema,
                    instance=stats.items[0],
                    params={
                        'include': data['include']
                    }
                )
            }
        )


class StatsListAPI(Base):
    def __init__(self):
        Base.__init__(self)
        self.stat = StatService()

    @marshal_with(DataResponse.marshallable())
    def get(self):
        data = self.clean(schema=fetch_all_schema, instance=request.args)
        stats = self.stat.find(**data)
        return DataResponse(
            data={
                '_metadata': self.prepare_metadata(
                    total_count=stats.total,
                    page_count=len(stats.items),
                    page=data['page'],
                    per_page=data['per_page']),
                'stats': self.dump(
                    schema=dump_many_schema,
                    instance=stats.items,
                    params={
                        'expand': data['expand']
                    }
                )
            }
        )
