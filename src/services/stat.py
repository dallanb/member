import logging
from http import HTTPStatus

from .base import Base
from ..models import Stat as StatModel


class Stat(Base):
    def __init__(self):
        Base.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.stat_model = StatModel

    def find(self, **kwargs):
        return Base.find(self, model=self.stat_model, **kwargs)

    def create(self, **kwargs):
        stat = self.init(model=self.stat_model, **kwargs)
        return self.save(instance=stat)

    def update(self, uuid, **kwargs):
        stats = self.find(uuid=uuid)
        if not stats.total:
            self.error(code=HTTPStatus.NOT_FOUND)
        return self.apply(instance=stats.items[0], **kwargs)

    def apply(self, instance, **kwargs):
        stat = self.assign_attr(instance=instance, attr=kwargs)
        return self.save(instance=stat)

    def destroy(self, uuid, ):
        stats = self.find(uuid=uuid)
        if not stats.total:
            self.error(code=HTTPStatus.NOT_FOUND)
        return Base.destroy(self, instance=stats.items[0])
