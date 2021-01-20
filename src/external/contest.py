from .base import Base
from .. import app


class Contest(Base):
    def __init__(self):
        Base.__init__(self)
        self.base_url = app.config['CONTEST_URL']

    def fetch_contest(self, uuid):
        url = f'{self.base_url}/contests/{uuid}'
        res = self.get(url=url)
        return res.json()

    def fetch_contests(self, params=None):
        url = f'{self.base_url}/contests'
        res = self.get(url=url, params=params)
        return res.json()

    def fetch_contest_materialized(self, uuid):
        url = f'{self.base_url}/contests/materialized/{uuid}'
        res = self.get(url=url)
        return res.json()

    def fetch_contests_materialized(self, params=None):
        url = f'{self.base_url}/contests/materialized'
        res = self.get(url=url, params=params)
        return res.json()
