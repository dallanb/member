from .schema import WalletCreatedSchema
from ..base import Base


class wallet_created(Base):
    key = 'wallet_created'
    schema = WalletCreatedSchema()

    def __init__(self, data):
        super().__init__(key=self.key, data=data)

    @classmethod
    def from_data(cls, wallet):
        data = cls.schema.dump({'wallet': wallet})
        return wallet_created(data=data)
