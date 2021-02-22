import pytest

from tests.helpers import fetch_contest_wager


@pytest.fixture
def mock_fetch_contest_wager(mocker):
    yield mocker.patch('src.services.MemberService.fetch_contest_wager', fetch_contest_wager)
