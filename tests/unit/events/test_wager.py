import time

import pytest

from src import services, events
from tests.helpers import generate_uuid


def test_wager_stake_created_sync(reset_db, pause_notification, seed_member, seed_wallet):
    """
    GIVEN 1 member instance, 0 wallet instance in the database
    WHEN directly calling event wager handle_event stake_created
    THEN event wager handle_event stake_created updates 1 member, 1 wallet in the database
    """
    key = 'stake_created'
    value = {
        'uuid': str(generate_uuid()),
        'member_uuid': str(pytest.member.uuid),
        'amount': 5.0
    }

    events.Wager().handle_event(key=key, data=value)

    members = services.MemberService().find()
    wallets = services.WalletService().find()

    assert members.total == 1

    assert wallets.total == 1
    assert wallets.items[0].balance == 195.0


def test_wager_stake_created_async(reset_db, pause_notification, kafka_conn_custom_topics, seed_member, seed_wallet):
    """
    GIVEN 1 member instance, 0 wallet instance in the database
    WHEN the WAGER service notifies Kafka that a stake has been created
    THEN event wager handle_event stake_created updates 1 member, 1 wallet in the database
    """
    kafka_conn_custom_topics(['wagers_test'])
    time.sleep(1)

    key = 'stake_created'
    value = {
        'uuid': str(generate_uuid()),
        'member_uuid': str(pytest.member.uuid),
        'amount': 5.0
    }

    services.Base().notify(topic='wagers_test', value=value, key=key)
    time.sleep(1)

    members = services.MemberService().find()
    wallets = services.WalletService().find()

    assert members.total == 1

    assert wallets.total == 1
    assert wallets.items[0].balance == 195.0
