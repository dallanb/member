import logging
from http import HTTPStatus

from .base import Base
from ..decorators import wallet_notification
from ..models import Wallet as WalletModel
from .wallet_transaction import WalletTransaction as WalletTransactionService


class Wallet(Base):
    def __init__(self):
        Base.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.wallet_model = WalletModel
        self.wallet_transaction_service = WalletTransactionService()

    def find(self, **kwargs):
        return self._find(model=self.wallet_model, **kwargs)

    @wallet_notification(operation='create')
    def create(self, **kwargs):
        wallet = self._init(model=self.wallet_model, **kwargs)
        wallet = self._save(instance=wallet)
        # create a transaction
        _ = self.create_transaction(instance=wallet)
        return wallet

    def update(self, uuid, **kwargs):
        wallets = self.find(uuid=uuid)
        if not wallets.total:
            self.error(code=HTTPStatus.NOT_FOUND)
        return self.apply(instance=wallets.items[0], **kwargs)

    @wallet_notification(operation='update')
    def apply(self, instance, **kwargs):
        wallet = self._assign_attr(instance=instance, attr=kwargs)
        return self._save(instance=wallet)

    def create_transaction(self, instance):
        wallet_transactions = self.wallet_transaction_service.find(wallet_uuid=instance.uuid)
        if wallet_transactions.total > 0:
            self.error(code=HTTPStatus.BAD_REQUEST)
        return self.wallet_transaction_service.create(wallet=instance, balance=instance.balance,
                                                      amount=instance.balance,
                                                      next_transaction_uuid=None)

    def add_transaction(self, instance, amount):
        wallet_transactions = self.wallet_transaction_service.find(wallet_uuid=instance.uuid,
                                                                   next_transaction_uuid=None)
        if wallet_transactions.total == 0:
            self.error(code=HTTPStatus.NOT_FOUND)
        prev_wallet_transaction = wallet_transactions.items[0]
        wallet_transaction = self.wallet_transaction_service.create(balance=prev_wallet_transaction.balance + amount,
                                                                    amount=amount)
        self.wallet_transaction_service.apply(instance=prev_wallet_transaction, next_transaction=wallet_transaction)
        # update the wallet balance synchronously
        self.apply(instance=instance, balance=wallet_transaction.balance)
        return wallet_transaction
