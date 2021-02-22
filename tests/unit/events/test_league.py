import time

import pytest

from src import services, events


def test_league_member_created_sync(reset_db, pause_notification):
    """
    GIVEN 0 member instance, 0 wallet instance and 0 stat instance in the database
    WHEN directly calling event league handle_event member_created
    THEN event league handle_event member_created adds 1 member, 1 wallet and 1 stat instance into the database
    """
    key = 'member_created'
    value = {
        'uuid': str(pytest.account_uuid),
        'user_uuid': str(pytest.user_uuid),
        'league_uuid': str(pytest.league_uuid),
        'email': pytest.email,
        'owner_uuid': str(pytest.user_uuid),
    }

    events.League().handle_event(key=key, data=value)

    members = services.MemberService().find()
    wallets = services.WalletService().find()
    stats = services.StatService().find()

    assert members.total == 1

    assert wallets.total == 1

    assert stats.total == 1


def test_league_member_created_async(reset_db, pause_notification, kafka_conn_custom_topics):
    """
    GIVEN 0 member instance, 0 wallet instance and 0 stat instance in the database
    WHEN the LEAGUE service notifies Kafka that a member has been created
    THEN event league handle_event member_created adds 1 member, 1 wallet and 1 stat instance into the database
    """
    kafka_conn_custom_topics(['leagues_test'])
    time.sleep(1)

    key = 'member_created'
    value = {
        'uuid': str(pytest.account_uuid),
        'user_uuid': str(pytest.user_uuid),
        'league_uuid': str(pytest.league_uuid),
        'email': pytest.email,
        'owner_uuid': str(pytest.user_uuid),
    }

    services.Base().notify(topic='leagues_test', value=value, key=key)
    time.sleep(1)

    members = services.MemberService().find()
    wallets = services.WalletService().find()
    stats = services.StatService().find()

    assert members.total == 1

    assert wallets.total == 1

    assert stats.total == 1
