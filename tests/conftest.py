import pytest
from uuid import uuid4

from .fixtures import *


def pytest_configure(config):
    pytest.member = None
    pytest.wallet = None
    pytest.stat = None
    pytest.avatar = None
    pytest.user_uuid = uuid4()
    pytest.member_uuid = uuid4()
    pytest.email = 'dallan.bhatti@techtapir.com'
    pytest.username = 'dallanbhatti'
    pytest.display_name = 'Dallan Bhatti'
    pytest.league_uuid = uuid4()
    pytest.country = 'CA'
    pytest.balance = 200.00  # this is the db default
    pytest.event_count = 0
    pytest.win_count = 0
    pytest.winning_total = 0
