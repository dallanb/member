from .schema import MemberInvitedSchema
from ..base import Base


class member_invited(Base):
    key = 'member_invited'
    schema = MemberInvitedSchema()

    def __init__(self, data):
        super().__init__(key=self.key, data=data)

    @classmethod
    def from_data(cls, member):
        data = cls.schema.dump({'member': member})
        return member_invited(data=data)
