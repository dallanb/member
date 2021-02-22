import pytest

from src import services


@pytest.fixture(scope="function")
def seed_member():
    pytest.member = services.MemberService().create(status='pending', user_uuid=pytest.user_uuid,
                                                    email=pytest.email, username=pytest.username,
                                                    league_uuid=pytest.league_uuid, display_name=pytest.display_name,
                                                    country=pytest.country)


@pytest.fixture(scope="function")
def seed_other_member():
    pytest.other_member = services.MemberService().create(status='pending', user_uuid=pytest.other_user_uuid,
                                                          email=pytest.other_email, username=pytest.other_username,
                                                          league_uuid=pytest.league_uuid,
                                                          display_name=pytest.other_display_name,
                                                          country=pytest.country)
