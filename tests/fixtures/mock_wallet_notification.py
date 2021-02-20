import pytest

from tests.helpers import wallet_notification_create, wallet_notification_update


@pytest.fixture
def mock_wallet_notification_create(mocker):
    yield mocker.patch('src.decorators.wallet_notification.create', wallet_notification_create)


@pytest.fixture
def mock_wallet_notification_update(mocker):
    yield mocker.patch('src.decorators.wallet_notification.update', wallet_notification_update)
