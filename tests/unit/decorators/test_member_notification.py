import time

import pytest

from src import services


def test_member_notification_member_invited(reset_db, kafka_conn_last_msg):
    pytest.member = services.MemberService().create(status='invited', email=pytest.email)
    time.sleep(0.2)
    msg = kafka_conn_last_msg('members')
    assert msg.key is not None
    assert msg.key == 'member_invited'
    assert msg.value is not None
    assert msg.value['uuid'] == str(pytest.member.uuid)


def test_member_notification_member_pending(reset_db, kafka_conn_last_msg):
    pytest.member = services.MemberService().create(status='pending', user_uuid=pytest.user_uuid,
                                                    email=pytest.email, username=pytest.username,
                                                    league_uuid=pytest.league_uuid, display_name=pytest.display_name,
                                                    country=pytest.country)
    time.sleep(0.2)
    msg = kafka_conn_last_msg('members')
    assert msg.key is not None
    assert msg.key == 'member_pending'
    assert msg.value is not None
    assert msg.value['uuid'] == str(pytest.member.uuid)


def test_member_notification_member_active(kafka_conn_last_msg):
    pytest.member = services.MemberService().update(uuid=pytest.member.uuid, status='active')
    time.sleep(0.2)
    msg = kafka_conn_last_msg('members')
    assert msg.key is not None
    assert msg.key == 'member_active'
    assert msg.value is not None
    assert msg.value['uuid'] == str(pytest.member.uuid)


def test_member_notification_member_inactive(kafka_conn_last_msg):
    pytest.member = services.MemberService().update(uuid=pytest.member.uuid, status='inactive')
    time.sleep(0.2)
    msg = kafka_conn_last_msg('members')
    assert msg.key is not None
    assert msg.key == 'member_inactive'
    assert msg.value is not None
    assert msg.value['uuid'] == str(pytest.member.uuid)





def test_member_notification_display_name_updated(kafka_conn_last_msg):
    display_name = 'Test User'
    pytest.member = services.MemberService().update(uuid=pytest.member.uuid, display_name=display_name)
    time.sleep(0.2)
    msg = kafka_conn_last_msg('members')
    assert msg.key is not None
    assert msg.key == 'display_name_updated'
    assert msg.value is not None
    assert msg.value['display_name'] == display_name


def test_member_notification_country_updated(kafka_conn_last_msg):
    country = 'US'
    _ = services.MemberService().update_by_user(user_uuid=pytest.user_uuid, country=country)
    time.sleep(0.2)
    msg = kafka_conn_last_msg('members')
    assert msg.key is not None
    assert msg.key == 'country_updated'
    assert msg.value is not None
    assert msg.value['uuid'] == str(pytest.member.uuid)
    assert msg.value['user_uuid'] == str(pytest.user_uuid)
    assert msg.value['country'] == country
