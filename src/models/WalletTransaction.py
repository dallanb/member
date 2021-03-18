from sqlalchemy_utils import UUIDType

from .mixins import BaseMixin
from .. import db


class WalletTransaction(db.Model, BaseMixin):
    balance = db.Column(db.Float, nullable=False)
    amount = db.Column(db.Float, nullable=False, default=0.0)
    # eventually add a field(s) to give background information on the transaction

    # FK
    wallet_uuid = db.Column(UUIDType(binary=False), db.ForeignKey('wallet.uuid'), unique=False, nullable=False)
    next_transaction_uuid = db.Column(UUIDType(binary=False), db.ForeignKey('wallet_transaction.uuid'), unique=True,
                                      nullable=True)

    # Relationship
    wallet = db.relationship("Wallet", back_populates="transactions", lazy="joined")
    next_transaction = db.relationship("WalletTransaction")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


WalletTransaction.register()
