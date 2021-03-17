import pytest


@pytest.fixture(scope="function")
def pause_notification(mock_member_notification_create, mock_member_notification_update,
                       mock_member_notification_update_user, mock_wallet_notification_create,
                       mock_wallet_notification_update, mock_stat_notification_create,
                       mock_stat_notification_update, mock_avatar_notification_create,
                       mock_avatar_notification_delete, mock_avatar_notification_update):
    return True
