import logging
import time

import pytest

from src import services, events


def test_contest_participant_completed_sync(reset_db, pause_notification, seed_member, seed_stat):
    """
    GIVEN 1 member instance and 1 stat instance in the database
    WHEN directly calling event contest handle_event participant_completed
    THEN event contest handle_event participant_completed updates 1 stat instance in the database
    """
    key = 'participant_completed'
    value = {
        'member_uuid': str(pytest.member.uuid)  # add the rest of the fields as you need them
    }

    events.Contest().handle_event(key=key, data=value)

    stats = services.StatService().find()

    assert stats.total == 1
    assert stats.items[0].event_count == 1


def test_contest_contest_completed_sync(reset_db, pause_notification, mock_fetch_contest, mock_fetch_contest_wager,
                                        seed_member, seed_wallet, seed_stat, seed_other_member, seed_other_wallet,
                                        seed_other_stat):
    """
    GIVEN 2 member instance, 2 wallet instance and 2 stat instance in the database
    WHEN directly calling event contest handle_event contest_completed
    THEN event contest handle_event contest_completed updates 1 stat, 1 member and 1 wallet instance in the database
    """
    key = 'contest_completed'
    value = {
        'uuid': str(pytest.contest_uuid),
        'league_uuid': str(pytest.league_uuid),
        'owner_uuid': str(pytest.user_uuid)
    }

    events.Contest().handle_event(key=key, data=value)

    _ = services.MemberService().find()
    wallets = services.WalletService().find()
    stats = services.StatService().find()

    for wallet in wallets.items:
        assert wallet.balance is not pytest.balance

    for stat in stats.items:
        assert stat.winning_total is not pytest.winning_total


def test_contest_contest_completed_async(reset_db, pause_notification, kafka_conn_custom_topics, mock_fetch_contest,
                                         mock_fetch_contest_wager,
                                         seed_member, seed_wallet, seed_stat, seed_other_member, seed_other_wallet,
                                         seed_other_stat):
    """
    GIVEN 2 member instance, 2 wallet instance and 2 stat instance in the database
    WHEN directly calling event contest handle_event contest_completed
    THEN event contest handle_event contest_completed updates 1 stat, 1 member and 1 wallet instance in the database
    """

    kafka_conn_custom_topics(['contests_test'])
    time.sleep(1)

    key = 'contest_completed'
    value = {
        'uuid': str(pytest.contest_uuid),
        'league_uuid': str(pytest.league_uuid),
        'owner_uuid': str(pytest.user_uuid)
    }

    services.Base().notify(topic='contests_test', value=value, key=key)
    time.sleep(1)

    _ = services.MemberService().find()
    wallets = services.WalletService().find()
    stats = services.StatService().find()

    for wallet in wallets.items:
        assert wallet.balance is not pytest.balance

    for stat in stats.items:
        assert stat.winning_total is not pytest.winning_total
