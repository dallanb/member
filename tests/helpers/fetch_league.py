import pytest


def fetch_league(self, uuid):
    if uuid == str(pytest.league_uuid):
        return {
            'name': "Big Baller Brand",
            'uuid': uuid,
            'status': "active",
            'owner_uuid': str(pytest.user_uuid)
        }
    else:
        return None
