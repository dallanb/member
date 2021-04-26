import logging
from http import HTTPStatus

from .base import Base
from ..decorators.notifications import stat_notification
from ..models import Stat as StatModel, Member as MemberModel


class Stat(Base):
    def __init__(self):
        Base.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.stat_model = StatModel
        self.member_model = MemberModel

    def find(self, **kwargs):
        return self._find(model=self.stat_model, **kwargs)

    @stat_notification(operation='create')
    def create(self, **kwargs):
        stat = self._init(model=self.stat_model, **kwargs)
        return self._save(instance=stat)

    def update(self, uuid, **kwargs):
        stats = self.find(uuid=uuid)
        if not stats.total:
            self.error(code=HTTPStatus.NOT_FOUND)
        return self.apply(instance=stats.items[0], **kwargs)

    @stat_notification(operation='update')
    def apply(self, instance, **kwargs):
        stat = self._assign_attr(instance=instance, attr=kwargs)
        return self._save(instance=stat)
