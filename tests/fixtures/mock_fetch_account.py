import pytest

from tests.helpers import fetch_account


@pytest.fixture
def mock_fetch_account(mocker):
    yield mocker.patch('src.services.MemberService.fetch_account', fetch_account)
