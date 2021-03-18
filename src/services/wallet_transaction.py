import logging
from http import HTTPStatus

from .base import Base
from ..models import WalletTransaction as WalletTransactionModel


class WalletTransaction(Base):
    def __init__(self):
        Base.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.wallet_transaction_model = WalletTransactionModel

    def find(self, **kwargs):
        return self._find(model=self.wallet_transaction_model, **kwargs)

    def create(self, **kwargs):
        wallet_transaction = self._init(model=self.wallet_transaction_model, **kwargs)
        return self._save(instance=wallet_transaction)

    def update(self, uuid, **kwargs):
        wallet_transactions = self.find(uuid=uuid)
        if not wallet_transactions.total:
            self.error(code=HTTPStatus.NOT_FOUND)
        return self.apply(instance=wallet_transactions.items[0], **kwargs)

    def apply(self, instance, **kwargs):
        wallet_transaction = self._assign_attr(instance=instance, attr=kwargs)
        return self._save(instance=wallet_transaction)
