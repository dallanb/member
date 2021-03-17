import json

import pytest

###########
# Fetch
###########
from src import app


#############
# SUCCESS
#############

###########
# Fetch
###########
def test_fetch_member(reset_db, pause_notification, seed_member, seed_wallet, seed_stat):
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'member' is requested
    THEN check that the response is valid
    """
    member_uuid = pytest.member.uuid

    # Header
    headers = {'X-Consumer-Custom-ID': pytest.user_uuid}

    # Request
    response = app.test_client().get(f'/members/{member_uuid}', headers=headers)
    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    members = response['data']['members']
    assert members['status'] == 'pending'
    assert members['uuid'] == str(member_uuid)
    assert members['user_uuid'] == str(pytest.user_uuid)
    assert members['username'] == pytest.username
    assert members['display_name'] == pytest.display_name
    assert members['country'] == pytest.country
    assert members['league_uuid'] == str(pytest.league_uuid)


def test_fetch_member_user(reset_db, pause_notification, seed_member, seed_wallet, seed_stat):
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'member_user' is requested
    THEN check that the response is valid
    """
    user_uuid = pytest.user_uuid

    # Header
    headers = {'X-Consumer-Custom-ID': pytest.user_uuid}

    # Params
    params = {'league_uuid': pytest.league_uuid}

    # Request
    response = app.test_client().get(f'/members/user/{user_uuid}', headers=headers, query_string=params)
    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    members = response['data']['members']
    assert members['status'] == 'pending'
    assert members['uuid'] == str(pytest.member.uuid)
    assert members['user_uuid'] == str(pytest.user_uuid)
    assert members['username'] == pytest.username
    assert members['display_name'] == pytest.display_name
    assert members['country'] == pytest.country
    assert members['league_uuid'] == str(pytest.league_uuid)


def test_fetch_my_member_user(reset_db, pause_notification, seed_member, seed_wallet, seed_stat):
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'member_user' is requested
    THEN check that the response is valid
    """
    user_uuid = pytest.user_uuid

    # Header
    headers = {'X-Consumer-Custom-ID': pytest.user_uuid}

    # Params
    params = {'league_uuid': pytest.league_uuid}

    # Request
    response = app.test_client().get(f'/members/user/me', headers=headers, query_string=params)
    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    members = response['data']['members']
    assert members['status'] == 'pending'
    assert members['uuid'] == str(pytest.member.uuid)
    assert members['user_uuid'] == str(pytest.user_uuid)
    assert members['username'] == pytest.username
    assert members['display_name'] == pytest.display_name
    assert members['country'] == pytest.country
    assert members['league_uuid'] == str(pytest.league_uuid)


###########
# Fetch All
###########
def test_fetch_all_member(reset_db, pause_notification, seed_member, seed_wallet, seed_stat):
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'members' is requested
    THEN check that the response is valid
    """
    # Header
    headers = {'X-Consumer-Custom-ID': pytest.user_uuid}

    # Params
    params = {'league_uuid': pytest.league_uuid}

    # Request
    response = app.test_client().get(f'/members', headers=headers, query_string=params)
    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    assert len(response['data']['members']) == 1
    members = response['data']['members'][0]
    assert members['status'] == 'pending'
    assert members['uuid'] == str(pytest.member.uuid)
    assert members['user_uuid'] == str(pytest.user_uuid)
    assert members['username'] == pytest.username
    assert members['display_name'] == pytest.display_name
    assert members['country'] == pytest.country
    assert members['league_uuid'] == str(pytest.league_uuid)


def test_fetch_all_member_search(reset_db, pause_notification, seed_member, seed_wallet, seed_stat):
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'members' is requested
    THEN check that the response is valid
    """
    # Header
    headers = {'X-Consumer-Custom-ID': pytest.user_uuid}

    # Params
    params = {'league_uuid': pytest.league_uuid, 'search': pytest.display_name[:4]}

    # Request
    response = app.test_client().get(f'/members', headers=headers, query_string=params)
    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    assert len(response['data']['members']) == 1
    members = response['data']['members'][0]
    assert members['status'] == 'pending'
    assert members['uuid'] == str(pytest.member.uuid)
    assert members['user_uuid'] == str(pytest.user_uuid)
    assert members['username'] == pytest.username
    assert members['display_name'] == pytest.display_name
    assert members['country'] == pytest.country
    assert members['league_uuid'] == str(pytest.league_uuid)


def test_fetch_all_member_standings(reset_db, pause_notification, seed_member, seed_wallet, seed_stat):
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'members_standings' is requested
    THEN check that the response is valid
    """
    # Header
    headers = {'X-Consumer-Custom-ID': pytest.user_uuid}

    # Params
    params = {'league_uuid': pytest.league_uuid, 'include': 'stat'}

    # Request
    response = app.test_client().get(f'/members/standings', headers=headers, query_string=params)
    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    assert len(response['data']['members']) == 1
    members = response['data']['members'][0]
    assert members['status'] == 'pending'
    assert members['uuid'] == str(pytest.member.uuid)
    assert members['user_uuid'] == str(pytest.user_uuid)
    assert members['username'] == pytest.username
    assert members['display_name'] == pytest.display_name
    assert members['country'] == pytest.country
    assert members['league_uuid'] == str(pytest.league_uuid)
    stats = members['stat']
    assert stats is not None


def test_fetch_all_member_bulk(reset_db, pause_notification, seed_member, seed_wallet, seed_stat):
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'members_bulk' is requested
    THEN check that the response is valid
    """
    # Header
    headers = {'X-Consumer-Custom-ID': pytest.user_uuid}

    # Payload
    payload = {
        "within": {
            "key": "uuid",
            "value": [pytest.member.uuid]
        }
    }

    # Request
    response = app.test_client().post(f'/members/bulk', headers=headers, json=payload)
    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    assert len(response['data']['members']) == 1
    members = response['data']['members'][0]
    assert members['status'] == 'pending'
    assert members['uuid'] == str(pytest.member.uuid)
    assert members['user_uuid'] == str(pytest.user_uuid)
    assert members['username'] == pytest.username
    assert members['display_name'] == pytest.display_name
    assert members['country'] == pytest.country
    assert members['league_uuid'] == str(pytest.league_uuid)


###########
# Update
###########
def test_update_member(reset_db, pause_notification, seed_member, seed_wallet, seed_stat):
    """
    GIVEN a Flask application configured for testing
    WHEN the PUT endpoint 'member' is requested
    THEN check that the response is valid
    """
    member_uuid = pytest.member.uuid
    display_name = 'Baby D'

    # Headers
    headers = {'X-Consumer-Custom-ID': pytest.user_uuid}

    # Payload
    payload = {'display_name': display_name}

    # Request
    response = app.test_client().put(f'/members/{member_uuid}', json=payload, headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    members = response['data']['members']
    assert members['uuid'] is not None
    assert members['display_name'] == display_name


#############
# FAIL
#############


###########
# Update
###########
def test_update_member_fail(reset_db, pause_notification, seed_member, seed_wallet, seed_stat):
    """
    GIVEN a Flask application configured for testing
    WHEN the PUT endpoint 'member' is requested
    THEN check that the response is valid
    """
    member_uuid = pytest.member.uuid
    status = 'active'

    # Headers
    headers = {'X-Consumer-Custom-ID': pytest.user_uuid}

    # Payload
    payload = {'status': status}

    # Request
    response = app.test_client().put(f'/members/{member_uuid}', json=payload, headers=headers)

    # Response
    assert response.status_code == 400
