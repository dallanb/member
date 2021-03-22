import pytest

from tests.helpers import fetch_contest, fetch_contest_tie


@pytest.fixture
def mock_fetch_contest(mocker):
    yield mocker.patch('src.services.MemberService.fetch_contest', fetch_contest)


@pytest.fixture
def mock_fetch_contest_tie(mocker):
    yield mocker.patch('src.services.MemberService.fetch_contest', fetch_contest_tie)
