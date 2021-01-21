from sqlalchemy_utils import EmailType, UUIDType

from .mixins import BaseMixin
from .. import db


class Invite(db.Model, BaseMixin):
    email = db.Column(EmailType, nullable=False)
    league_uuid = db.Column(UUIDType(binary=False), nullable=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


Invite.register()
