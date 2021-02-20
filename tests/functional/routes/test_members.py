import json

import pytest

#############
# SUCCESS
#############

###########
# Fetch
###########
from src import app


def test_fetch_member(reset_db, mock_fetch_member_user, mock_fetch_member, mock_fetch_member_batch,
                      mock_fetch_location, mock_create_batch_threaded, pause_notification):
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'member' is requested
    THEN check that the response is valid
    """
    member_uuid = pytest.member_uuid

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
    assert members['owner_uuid'] == str(pytest.owner_user_uuid)
    assert members['name'] == pytest.name
    assert members['start_time'] == pytest.start_time
    assert members['league_uuid'] == str(pytest.league_uuid)
    assert members['location_uuid'] == str(pytest.location_uuid)

    # confirm sport creation
    sports = services.SportService().find()
    assert sports.total == 1

    sport = sports.items[0]
    assert sport.sport_uuid == pytest.sport_uuid
    assert str(sport.member_uuid) == members['uuid']

    # confirm owner creation
    participants = services.ParticipantService().find(member_uuid=pytest.owner_member_uuid)
    assert participants.total == 1

    owner = participants.items[0]
    assert str(owner.member_uuid) == members['uuid']
    assert owner.status.name == 'active'
