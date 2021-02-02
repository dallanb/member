import logging
from http import HTTPStatus

from sqlalchemy.orm import aliased

from .base import Base
from ..models import Wallet as WalletModel, Member as MemberModel


class Wallet(Base):
    def __init__(self):
        Base.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.wallet_model = WalletModel
        self.member_model = MemberModel

    def find(self, **kwargs):
        return Base.find(self, model=self.wallet_model, **kwargs)

    def create(self, **kwargs):
        wallet = self.init(model=self.wallet_model, **kwargs)
        return self.save(instance=wallet)

    def update(self, find, **kwargs):
        wallets = self.find(**find)
        if not wallets.total:
            self.error(code=HTTPStatus.NOT_FOUND)
        return self.apply(instance=wallets.items[0], **kwargs)

    def apply(self, instance, **kwargs):
        wallet = self.assign_attr(instance=instance, attr=kwargs)
        return self.save(instance=wallet)

    def destroy(self, uuid, ):
        wallets = self.find(uuid=uuid)
        if not wallets.total:
            self.error(code=HTTPStatus.NOT_FOUND)
        return Base.destroy(self, instance=wallets.items[0])

    def find_league_member_wallets(self, league_uuid, members):
        query = self.db.clean_query(model=self.wallet_model, within={'member_uuid': members})
        entity = aliased(self.member_model)
        query = query.join(entity).filter(entity.league_uuid == league_uuid)
        return self.db.run_query(query=query)
