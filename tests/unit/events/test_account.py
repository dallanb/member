import time

import pytest

from src import services, events


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


def test_account_account_active_async(reset_db, pause_notification, kafka_conn_custom_topics, mock_fetch_account):
    """
    GIVEN 0 member instance, 0 wallet instance and 0 stat instance in the database
    WHEN the ACCOUNT service notifies Kafka that an account is active
    THEN event account handle_event account_active adds 1 member, 1 wallet and 1 stat instance into the database
    """
    kafka_conn_custom_topics(['accounts_test'])
    time.sleep(1)

    key = 'account_active'
    value = {
        'uuid': str(pytest.account_uuid)
    }

    services.Base().notify(topic='accounts_test', value=value, key=key)
    time.sleep(1)

    members = services.MemberService().find()
    wallets = services.WalletService().find()
    stats = services.StatService().find()

    assert members.total == 1

    assert wallets.total == 1

    assert stats.total == 1
