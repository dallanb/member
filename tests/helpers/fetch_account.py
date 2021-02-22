import pytest


def fetch_account(self, uuid, params=None):
    # if params is None:
    #     params = {'include': ['address']}

    if uuid == str(pytest.account_uuid):
        return {
            'user_uuid': str(pytest.user_uuid),
            'uuid': uuid,
            'email': pytest.email,
            'status': 'active',
            'display_name': pytest.display_name,
            'username': pytest.username,
            'address': {
                'country': pytest.country
            }
        }
    elif uuid == str(pytest.other_account_uuid):
        return {
            'user_uuid': str(pytest.other_user_uuid),
            'uuid': uuid,
            'email': pytest.other_email,
            'status': 'active',
            'display_name': pytest.other_display_name,
            'username': pytest.other_username,
            'address': {
                'country': pytest.country
            }
        }
    else:
        return None
