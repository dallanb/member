import pytest
import time

from src import services


def test_wallet_notification_wallet_created(reset_db, kafka_conn_last_msg):
    pytest.member = services.MemberService().create(status='pending', user_uuid=pytest.user_uuid,
                                                    email=pytest.email, username=pytest.username,
                                                    league_uuid=pytest.league_uuid, display_name=pytest.display_name,
                                                    country=pytest.country)
    pytest.wallet = services.WalletService().create(member=pytest.member)
    time.sleep(0.5)
    msg = kafka_conn_last_msg('members')
    assert msg.key is not None
    assert msg.key == 'wallet_created'
    assert msg.value is not None
    assert msg.value['uuid'] == str(pytest.wallet.uuid)
    time.sleep(0.5)


def test_wallet_notification_wallet_updated(kafka_conn_last_msg):
    _ = services.WalletService().update(uuid=pytest.wallet.uuid, balance=205.0)
    msg = kafka_conn_last_msg('members')
    assert msg.key is not None
    assert msg.key == 'wallet_updated'
    assert msg.value is not None
    assert msg.value['uuid'] == str(pytest.wallet.uuid)
    time.sleep(0.5)
