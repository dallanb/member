import time

import pytest
from src import services


def test_stat_notification_stat_created(reset_db, kafka_conn_last_msg):
    pytest.member = services.MemberService().create(status='pending', user_uuid=pytest.user_uuid,
                                                    email=pytest.email, username=pytest.username,
                                                    league_uuid=pytest.league_uuid, display_name=pytest.display_name,
                                                    country=pytest.country)
    pytest.stat = services.StatService().create(member=pytest.member)
    time.sleep(0.2)
    msg = kafka_conn_last_msg('members')
    assert msg.key is not None
    assert msg.key == 'stat_created'
    assert msg.value is not None
    assert msg.value['uuid'] == str(pytest.stat.uuid)


def test_stat_notification_stat_updated(kafka_conn_last_msg):
    _ = services.StatService().update(uuid=pytest.stat.uuid, event_count=2)
    time.sleep(0.2)
    msg = kafka_conn_last_msg('members')
    assert msg.key is not None
    assert msg.key == 'stat_updated'
    assert msg.value is not None
    assert msg.value['uuid'] == str(pytest.stat.uuid)
