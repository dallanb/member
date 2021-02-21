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
def test_fetch_wallet(reset_db, pause_notification, seed_member, seed_wallet):
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'wallet' is requested
    THEN check that the response is valid
    """
    wallet_uuid = pytest.wallet.uuid

    # Header
    headers = {'X-Consumer-Custom-ID': pytest.user_uuid}

    # Request
    response = app.test_client().get(f'/wallets/{wallet_uuid}', headers=headers)
    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    wallets = response['data']['wallets']
    assert wallets['uuid'] == str(wallet_uuid)
    assert wallets['balance'] == pytest.balance


def test_fetch_wallet_member():
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'wallet_member' is requested
    THEN check that the response is valid
    """
    members = services.MemberService().find()
    member_uuid = members.items[0].uuid

    # Header
    headers = {'X-Consumer-Custom-ID': pytest.user_uuid}

    # Request
    response = app.test_client().get(f'/wallets/member/{member_uuid}', headers=headers)
    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    wallets = response['data']['wallets']
    assert wallets['uuid'] is not None
    assert wallets['balance'] == pytest.balance


###########
# Fetch All
###########
def test_fetch_all_wallet():
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'wallets' is requested
    THEN check that the response is valid
    """
    # Header
    headers = {'X-Consumer-Custom-ID': pytest.user_uuid}

    # Request
    response = app.test_client().get(f'/wallets', headers=headers)
    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    assert len(response['data']['wallets']) == 1
    wallets = response['data']['wallets'][0]
    assert wallets['uuid'] is not None
    assert wallets['balance'] == pytest.balance
