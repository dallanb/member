from sqlalchemy_utils import UUIDType

from .mixins import BaseMixin
from .. import db


class Wallet(db.Model, BaseMixin):
    balance = db.Column(db.Float, nullable=False, default=200.00)

    # FK
    member_uuid = db.Column(UUIDType(binary=False), db.ForeignKey('member.uuid'), nullable=False)

    # Relationship
    member = db.relationship("Member", back_populates="wallet", lazy="joined")
    transactions = db.relationship("WalletTransaction", back_populates="wallet")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


Wallet.register()
