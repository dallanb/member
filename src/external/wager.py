from .base import Base
from .. import app


class Wager(Base):
    def __init__(self):
        Base.__init__(self)
        self.base_url = app.config['WAGER_URL']

    def fetch_wager(self, uuid, params=None):
        url = f'{self.base_url}/wagers/{uuid}'
        res = self.get(url=url, params=params)
        return res.json()

    def fetch_contest_wager(self, uuid, params=None):
        url = f'{self.base_url}/contests/{uuid}/complete'
        res = self.get(url=url, params=params)
        return res.json()

    def fetch_wagers(self, params=None):
        url = f'{self.base_url}/wagers'
        res = self.get(url=url, params=params)
        return res.json()
