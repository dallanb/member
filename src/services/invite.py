import logging

from .base import Base
from ..decorators import invite_notification
from ..models import Invite as InviteModel, Stat as StatModel


class Invite(Base):
    def __init__(self):
        Base.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.invite_model = InviteModel
        self.stat_model = StatModel

    def find(self, **kwargs):
        return Base.find(self, model=self.invite_model, **kwargs)

    @invite_notification(operation='create')
    def create(self, **kwargs):
        invite = self.init(model=self.invite_model, **kwargs)
        return self.save(instance=invite)
