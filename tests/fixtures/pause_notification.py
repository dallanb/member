import pytest


@pytest.fixture(scope="function")
def pause_notification(mock_member_notification_create, mock_member_notification_update,
                       mock_wallet_notification_create, mock_wallet_notification_update):
    return True
