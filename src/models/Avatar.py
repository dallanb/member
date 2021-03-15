from .mixins import BaseMixin
from .. import db


class Avatar(db.Model, BaseMixin):
    s3_filename = db.Column(db.String, nullable=False)

    # Relationship
    member = db.relationship("Member", back_populates="avatar", uselist=False, lazy="joined")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


Avatar.register()
