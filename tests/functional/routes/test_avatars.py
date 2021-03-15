import json

import pytest

from src import app, services


###########
# Create
###########
def test_create_avatar(reset_db, mock_upload_fileobj, pause_notification, seed_member):
    """
    GIVEN a Flask application configured for testing
    WHEN the POST endpoint 'avatars' is requested
    THEN check that the response is valid
    """
    member_uuid = pytest.member.uuid

    # Headers
    headers = {'X-Consumer-Custom-ID': pytest.user_uuid}

    # Payload
    payload = {'avatar': ''}

    # Request
    response = app.test_client().post(f'/members/{member_uuid}/avatars', data=payload,
                                      headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    avatars = response['data']['avatars']
    assert avatars['uuid'] is not None
    assert avatars['s3_filename'] == f"{str(member_uuid)}.jpeg"


def test_update_avatar(mock_upload_fileobj, pause_notification):
    """
    GIVEN a Flask application configured for testing
    WHEN the POST endpoint 'avatars' is requested
    THEN check that the response is valid
    """
    member = services.MemberService().find().items[0]
    member_uuid = member.uuid

    # Headers
    headers = {'X-Consumer-Custom-ID': pytest.user_uuid}

    # Payload
    payload = {'avatar': ''}

    # Request
    response = app.test_client().post(f'/members/{member_uuid}/avatars', data=payload,
                                      headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    avatars = response['data']['avatars']
    assert avatars['uuid'] is not None
    assert avatars['s3_filename'] == f"{str(member_uuid)}.jpeg"

    # ensure that we still only have one avatar instance in the database
    avatar = services.AvatarService().find()
    assert avatar.total == 1


def test_delete_avatar(mock_upload_fileobj, pause_notification):
    """
    GIVEN a Flask application configured for testing
    WHEN the DELETE endpoint 'avatar' is requested
    THEN check that the response is valid
    """
    avatar = services.AvatarService().find().items[0]
    avatar_uuid = avatar.uuid

    # Headers
    headers = {'X-Consumer-Custom-ID': pytest.user_uuid}

    # Request
    response = app.test_client().delete(f'/avatars/{avatar_uuid}', headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"

    member = services.MemberService().find().items[0]
    assert member.avatar is None

    assert services.AvatarService().find().total == 0
