from sqlalchemy_utils import UUIDType

from .mixins import BaseMixin
from .. import db


class Stat(db.Model, BaseMixin):
    event_count = db.Column(db.Integer, nullable=False, default=0)
    win_count = db.Column(db.Integer, nullable=False, default=0)
    winning_total = db.Column(db.BigInteger, nullable=False, default=0)

    # FK
    member_uuid = db.Column(UUIDType(binary=False), db.ForeignKey('member.uuid'), nullable=False)

    # Relationship
    member = db.relationship("Member", back_populates="stat", lazy="joined")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


Stat.register()
