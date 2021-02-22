from uuid import uuid4

import pytest
from .fixtures import *

def pytest_configure(config):
    pytest.member = None
    pytest.wallet = None
    pytest.stat = None
    pytest.avatar = None
    pytest.account_uuid = uuid4()
    pytest.user_uuid = uuid4()
    pytest.email = 'dallan.bhatti@techtapir.com'
    pytest.username = 'dallanbhatti'
    pytest.display_name = 'Dallan Bhatti'
    pytest.balance = 200.00  # this is the db default
    pytest.event_count = 0
    pytest.win_count = 0
    pytest.winning_total = 0

    pytest.other_member = None
    pytest.other_wallet = None
    pytest.other_stat = None
    pytest.other_avatar = None
    pytest.other_account_uuid = uuid4()
    pytest.other_user_uuid = uuid4()
    pytest.other_email = 'dallanbhatti@gmail.com'
    pytest.other_username = 'babyd'
    pytest.other_display_name = 'Baby D'
    pytest.other_balance = 200.00  # this is the db default
    pytest.other_event_count = 0
    pytest.other_win_count = 0
    pytest.other_winning_total = 0

    pytest.league_uuid = uuid4()
    pytest.contest_uuid = uuid4()
    pytest.country = 'CA'
    pytest.buy_in = 5.0
    pytest.payout = [0.75, 0.25]
