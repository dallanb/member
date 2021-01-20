from .base import Base
from .. import app


class League(Base):
    def __init__(self):
        Base.__init__(self)
        self.base_url = app.config['LEAGUE_URL']

    def fetch_league(self, uuid):
        url = f'{self.base_url}/leagues/{uuid}'
        res = self.get(url=url)
        return res.json()

    def fetch_leagues(self, params=None):
        url = f'{self.base_url}/leagues'
        res = self.get(url=url, params=params)
        return res.json()
