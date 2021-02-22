from .schema import WalletUpdatedSchema
from ..base import Base


class wallet_updated(Base):
    key = 'wallet_updated'
    schema = WalletUpdatedSchema()

    def __init__(self, data):
        super().__init__(key=self.key, data=data)

    @classmethod
    def from_data(cls, wallet):
        data = cls.schema.dump({'wallet': wallet})
        return wallet_updated(data=data)
