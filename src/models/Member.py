from sqlalchemy_utils import EmailType, UUIDType
from sqlalchemy_utils.types import TSVectorType

from .mixins import BaseMixin
from .. import db
from ..common import StatusEnum


class Member(db.Model, BaseMixin):
    membership_uuid = db.Column(UUIDType(binary=False), primary_key=True, nullable=False)
    email = db.Column(EmailType, unique=True, nullable=False)
    username = db.Column(db.String(15), unique=True, nullable=False)
    display_name = db.Column(db.String(50), nullable=True)

    # Search
    search_vector = db.Column(TSVectorType('display_name', 'username', weights={'display_name': 'A', 'username': 'B'}))

    # FK
    status = db.Column(db.Enum(StatusEnum), db.ForeignKey('status.name'), nullable=False)

    # Relationship
    member_status = db.relationship("Status")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


Member.register()
