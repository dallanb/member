import pytest

from src import services


@pytest.fixture(scope="function")
def seed_stat():
    pytest.stat = services.StatService().create(event_count=pytest.event_count, win_count=pytest.win_count,
                                                winning_total=pytest.winning_total, member=pytest.member)
