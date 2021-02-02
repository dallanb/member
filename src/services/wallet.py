import logging
from http import HTTPStatus

from .base import Base
from ..decorators import wallet_notification
from ..models import Wallet as WalletModel, Member as MemberModel


class Wallet(Base):
    def __init__(self):
        Base.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.wallet_model = WalletModel
        self.member_model = MemberModel

    def find(self, **kwargs):
        return Base.find(self, model=self.wallet_model, **kwargs)

    @wallet_notification(operation='create')
    def create(self, **kwargs):
        wallet = self.init(model=self.wallet_model, **kwargs)
        return self.save(instance=wallet)

    def update(self, find, **kwargs):
        wallets = self.find(**find)
        if not wallets.total:
            self.error(code=HTTPStatus.NOT_FOUND)
        return self.apply(instance=wallets.items[0], **kwargs)

    @wallet_notification(operation='update')
    def apply(self, instance, **kwargs):
        wallet = self.assign_attr(instance=instance, attr=kwargs)
        self.logger.info("HEY WALLET HERE")
        self.logger.info(wallet)
        return self.save(instance=wallet)

    def destroy(self, uuid, ):
        wallets = self.find(uuid=uuid)
        if not wallets.total:
            self.error(code=HTTPStatus.NOT_FOUND)
        return Base.destroy(self, instance=wallets.items[0])
