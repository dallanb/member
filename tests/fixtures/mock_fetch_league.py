import pytest

from tests.helpers import fetch_league


@pytest.fixture
def mock_fetch_league(mocker):
    yield mocker.patch('src.services.MemberService.fetch_league', fetch_league)
