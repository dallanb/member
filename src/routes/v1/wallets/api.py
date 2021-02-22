from flask import request
from flask_restful import marshal_with

from .schema import *
from ..base import Base
from ....common.response import DataResponse
from ....services import WalletService


class WalletsAPI(Base):
    def __init__(self):
        Base.__init__(self)
        self.wallet = WalletService()

    @marshal_with(DataResponse.marshallable())
    def get(self, uuid):
        data = self.clean(schema=fetch_schema, instance=request.args)
        wallets = self.wallet.find(uuid=uuid, **data)
        if not wallets.total:
            self.throw_error(http_code=self.code.NOT_FOUND)
        return DataResponse(
            data={
                'wallets': self.dump(
                    schema=dump_schema,
                    instance=wallets.items[0],
                    params={
                        'expand': data['expand']
                    }
                )
            }
        )


class WalletsMemberAPI(Base):
    def __init__(self):
        Base.__init__(self)
        self.wallet = WalletService()

    @marshal_with(DataResponse.marshallable())
    def get(self, member_uuid):
        data = self.clean(schema=fetch_schema, instance={**request.args,
                                                         'member_uuid': member_uuid})
        wallets = self.wallet.find(**data)
        if not wallets.total:
            self.throw_error(http_code=self.code.NOT_FOUND)
        return DataResponse(
            data={
                'wallets': self.dump(
                    schema=dump_schema,
                    instance=wallets.items[0],
                    params={
                        'expand': data['expand']
                    }
                )
            }
        )


class WalletsListAPI(Base):
    def __init__(self):
        Base.__init__(self)
        self.wallet = WalletService()

    @marshal_with(DataResponse.marshallable())
    def get(self):
        data = self.clean(schema=fetch_all_schema, instance=request.args)
        wallets = self.wallet.find(**data)
        return DataResponse(
            data={
                '_metadata': self.prepare_metadata(
                    total_count=wallets.total,
                    page_count=len(wallets.items),
                    page=data['page'],
                    per_page=data['per_page']),
                'wallets': self.dump(
                    schema=dump_many_schema,
                    instance=wallets.items,
                    params={
                        'expand': data['expand']
                    }
                )
            }
        )
