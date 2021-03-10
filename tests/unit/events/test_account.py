import time

import pytest

from src import services, events
from tests.helpers import generate_uuid


def test_account_account_active_sync(reset_db, pause_notification, mock_fetch_account):
    """
    GIVEN 0 member instance, 0 wallet instance and 0 stat instance in the database
    WHEN directly calling event account handle_event account_active
    THEN event account handle_event account_active adds 1 member, 1 wallet and 1 stat instance into the database
    """
    key = 'account_active'
    value = {
        'uuid': str(pytest.account_uuid)
    }

    events.Account().handle_event(key=key, data=value)

    members = services.MemberService().find()
    wallets = services.WalletService().find()
    stats = services.StatService().find()

    assert members.total == 1

    assert wallets.total == 1

    assert stats.total == 1


def test_account_country_updated_sync(reset_db, pause_notification, seed_member):
    """
    GIVEN 2 member instance in the database
    WHEN directly calling event account handle_event country_updated
    THEN event account handle_event country_updated updates 2 member in the database
    """
    league_uuid = generate_uuid()
    services.MemberService().create(status='pending', user_uuid=pytest.user_uuid,
                                    email=pytest.other_email, username=pytest.other_username,
                                    league_uuid=league_uuid,
                                    display_name=pytest.other_display_name,
                                    country=pytest.country)

    key = 'country_updated'
    value = {
        'uuid': str(pytest.account_uuid),
        'user_uuid': str(pytest.user_uuid),
        'country': 'US'
    }

    events.Account().handle_event(key=key, data=value)

    members = services.MemberService().find()
    for member in members.items:
        assert member.country == 'US'
