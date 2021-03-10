from .schema import CountryUpdatedSchema
from ..base import Base


class country_updated(Base):
    key = 'country_updated'
    schema = CountryUpdatedSchema()

    def __init__(self, data):
        super().__init__(key=self.key, data=data)

    @classmethod
    def from_data(cls, uuid):
        data = cls.schema.dump({'uuid': uuid})
        return country_updated(data=data)
