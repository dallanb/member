from .schema import StatUpdatedSchema
from ..base import Base


class stat_updated(Base):
    key = 'stat_updated'
    schema = StatUpdatedSchema()

    def __init__(self, data):
        super().__init__(key=self.key, data=data)

    @classmethod
    def from_data(cls, stat):
        data = cls.schema.dump({'stat': stat})
        return stat_updated(data=data)
