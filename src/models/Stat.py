from sqlalchemy_utils import UUIDType
from .. import db
from .mixins import BaseMixin


class Stat(db.Model, BaseMixin):
    events = db.Column(db.Integer, nullable=False, default=0)
    wins = db.Column(db.Integer, nullable=False, default=0)
    winnings = db.Column(db.BigInteger, nullable=False, default=0)
    # FK
    member_uuid = db.Column(UUIDType(binary=False), db.ForeignKey('member.uuid'), nullable=False)

    # Relationship
    member = db.relationship("Member", back_populates="stat")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


Stat.register()
