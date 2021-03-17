from .schema import StatCreatedSchema
from ..base import Base


class stat_created(Base):
    key = 'stat_created'
    schema = StatCreatedSchema()

    def __init__(self, data):
        super().__init__(key=self.key, data=data)

    @classmethod
    def from_data(cls, stat):
        data = cls.schema.dump({'stat': stat})
        return stat_created(data=data)
