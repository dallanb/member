import time

import pytest

from src import services, events
from tests.helpers import generate_uuid


def test_course_course_approved_sync(reset_db, pause_notification, seed_member, seed_wallet, seed_stat):
    """
    GIVEN 1 member instance, 1 wallet instance and 1 stat instance in the database
    WHEN directly calling event course handle_event course_approved
    THEN event course handle_event course_approved updates 1 wallet instance in the database
    """
    key = 'course_approved'
    value = {
        'uuid': str(generate_uuid()),
        'created_by': str(pytest.user_uuid)
    }

    events.Course().handle_event(key=key, data=value)

    wallets = services.WalletService().find()
    wallet = wallets.items[0]
    assert wallet.balance == pytest.balance + 100.0


def test_course_course_approved_async(reset_db, pause_notification, kafka_conn_custom_topics, seed_member, seed_wallet,
                                      seed_stat):
    """
    GIVEN 1 member instance, 1 wallet instance and 1 stat instance in the database
    WHEN directly calling event course handle_event course_approved
    THEN event course handle_event course_approved updates 1 wallet instance in the database
    """

    kafka_conn_custom_topics(['courses_test'])
    time.sleep(1)

    key = 'course_approved'
    value = {
        'uuid': str(generate_uuid()),
        'created_by': str(pytest.user_uuid)
    }

    services.Base().notify(topic='courses_test', value=value, key=key)
    time.sleep(1)

    wallets = services.WalletService().find()
    wallet = wallets.items[0]
    assert wallet.balance == pytest.balance + 100.0
