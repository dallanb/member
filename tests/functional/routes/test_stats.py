import json

import pytest
from src import app, services


###########
# Fetch
###########


#############
# SUCCESS
#############

###########
# Fetch
###########
def test_fetch_stat(reset_db, pause_notification, seed_member, seed_stat):
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'stat' is requested
    THEN check that the response is valid
    """
    stat_uuid = pytest.stat.uuid

    # Header
    headers = {'X-Consumer-Custom-ID': pytest.user_uuid}

    # Request
    response = app.test_client().get(f'/stats/{stat_uuid}', headers=headers)
    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    stats = response['data']['stats']
    assert stats['uuid'] == str(stat_uuid)
    assert stats['win_count'] == pytest.win_count
    assert stats['winning_total'] == pytest.winning_total
    assert stats['event_count'] == pytest.event_count


def test_fetch_stat_member():
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'stat_member' is requested
    THEN check that the response is valid
    """
    members = services.MemberService().find()
    member_uuid = members.items[0].uuid

    # Header
    headers = {'X-Consumer-Custom-ID': pytest.user_uuid}

    # Request
    response = app.test_client().get(f'/stats/member/{member_uuid}', headers=headers)
    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    stats = response['data']['stats']
    assert stats['uuid'] is not None
    assert stats['win_count'] == pytest.win_count
    assert stats['winning_total'] == pytest.winning_total
    assert stats['event_count'] == pytest.event_count


###########
# Fetch All
###########
def test_fetch_all_stat():
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'stats' is requested
    THEN check that the response is valid
    """
    # Header
    headers = {'X-Consumer-Custom-ID': pytest.user_uuid}

    # Request
    response = app.test_client().get(f'/stats', headers=headers)
    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    assert len(response['data']['stats']) == 1
    stats = response['data']['stats'][0]
    assert stats['uuid'] is not None
    assert stats['win_count'] == pytest.win_count
    assert stats['winning_total'] == pytest.winning_total
    assert stats['event_count'] == pytest.event_count
