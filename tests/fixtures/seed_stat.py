import pytest

from src import services


@pytest.fixture(scope="function")
def seed_stat():
    pytest.stat = services.StatService().create(event_count=pytest.event_count, win_count=pytest.win_count,
                                                winning_total=pytest.winning_total, member=pytest.member)


@pytest.fixture(scope="function")
def seed_other_stat():
    pytest.other_stat = services.StatService().create(event_count=pytest.other_event_count,
                                                      win_count=pytest.other_win_count,
                                                      winning_total=pytest.other_winning_total,
                                                      member=pytest.other_member)
