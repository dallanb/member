import pytest

from tests.helpers import stat_notification_create, stat_notification_update


@pytest.fixture
def mock_stat_notification_create(mocker):
    yield mocker.patch('src.decorators.notifications.stat_notification.create', stat_notification_create)


@pytest.fixture
def mock_stat_notification_update(mocker):
    yield mocker.patch('src.decorators.notifications.stat_notification.update', stat_notification_update)
