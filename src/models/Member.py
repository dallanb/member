from sqlalchemy_utils import EmailType, UUIDType
from sqlalchemy_utils.types import TSVectorType

from .mixins import BaseMixin
from .. import db
from ..common import StatusEnum


class Member(db.Model, BaseMixin):
    user_uuid = db.Column(UUIDType(binary=False), nullable=True)
    email = db.Column(EmailType, nullable=False)
    username = db.Column(db.String(15), nullable=True)
    league_uuid = db.Column(UUIDType(binary=False), nullable=True)
    display_name = db.Column(db.String(50), nullable=True)
    country = db.Column(db.String, nullable=True)
    # Search
    search_vector = db.Column(TSVectorType('display_name', 'username', weights={'display_name': 'A', 'username': 'B'}))

    # FK
    status = db.Column(db.Enum(StatusEnum), db.ForeignKey('status.name'), nullable=False)
    avatar_uuid = db.Column(UUIDType(binary=False), db.ForeignKey('avatar.uuid'), nullable=True)

    # Relationship
    member_status = db.relationship("Status")
    avatar = db.relationship("Avatar")
    stat = db.relationship("Stat", uselist=False, back_populates="member")
    wallet = db.relationship("Wallet", uselist=False, back_populates="member")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


Member.register()
