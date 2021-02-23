import pytest

from src import services, ManualException
from tests.helpers import generate_uuid

member_service = services.MemberService()


###########
# Find
###########
def test_member_find(reset_db, pause_notification, seed_member):
    """
    GIVEN 1 member instance in the database
    WHEN the find method is called
    THEN it should return 1 member
    """

    members = member_service.find()
    assert members.total == 1
    assert len(members.items) == 1
    member = members.items[0]
    assert member.uuid == pytest.member.uuid


def test_member_find_by_uuid():
    """
    GIVEN 1 member instance in the database
    WHEN the find method is called with uuid
    THEN it should return 1 member
    """
    member = pytest.member
    uuid = member.uuid

    members = member_service.find(uuid=uuid)
    assert members.total == 1
    assert len(members.items) == 1
    member = members.items[0]
    assert member.uuid == uuid


def test_member_find_by_league_uuid():
    """
    GIVEN 1 member instance in the database
    WHEN the find method is called with league_uuid
    THEN it should return 1 member
    """
    member = pytest.member
    league_uuid = member.league_uuid

    members = member_service.find(league_uuid=league_uuid)
    assert members.total == 1
    assert len(members.items) == 1
    member = members.items[0]
    assert member.league_uuid == league_uuid


def test_member_find_by_user_uuid():
    """
    GIVEN 1 member instance in the database
    WHEN the find method is called with user_uuid
    THEN it should return 1 member
    """
    member = pytest.member
    user_uuid = member.user_uuid

    members = member_service.find(user_uuid=user_uuid)
    assert members.total == 1
    assert len(members.items) == 1
    member = members.items[0]
    assert member.user_uuid == user_uuid


def test_member_find_include_stat(pause_notification, seed_stat):
    """
    GIVEN 1 member instance in the database
    WHEN the find method is called with include argument to also return stat
    THEN it should return 1 member
    """
    members = member_service.find(include=['stat'])
    assert members.total == 1
    assert len(members.items) == 1
    member = members.items[0]

    assert member.stat is not None


def test_member_find_include_avatar(pause_notification, seed_avatar):
    """
    GIVEN 1 member instance in the database
    WHEN the find method is called with include argument to also return avatar
    THEN it should return 1 member
    """
    members = member_service.find(include=['avatar'])
    assert members.total == 1
    assert len(members.items) == 1
    member = members.items[0]
    assert member.avatar is not None


def test_member_find_include_wallet(pause_notification, seed_wallet):
    """
    GIVEN 1 member instance in the database
    WHEN the find method is called with include argument to also return wallet
    THEN it should return 1 member
    """
    members = member_service.find(include=['wallet'])
    assert members.total == 1
    assert len(members.items) == 1
    member = members.items[0]
    assert member.wallet is not None


def test_member_find_include_stat_include_avatar_include_wallet():
    """
    GIVEN 1 member instance in the database
    WHEN the find method is called with include argument to also return wallet, stat and avatar
    THEN it should return 1 member
    """
    members = member_service.find(include=['wallet', 'stat', 'avatar'])
    assert members.total == 1
    assert len(members.items) == 1
    member = members.items[0]
    assert member.stat is not None
    assert member.avatar is not None
    assert member.wallet is not None


def test_member_find_w_pagination(pause_notification, seed_other_member):
    """
    GIVEN 2 member instance in the database
    WHEN the find method is called with valid pagination
    THEN it should return the number of members defined in the pagination arguments
    """
    members_0 = member_service.find(page=1, per_page=1)
    assert members_0.total == 2
    assert len(members_0.items) == 1

    members_1 = member_service.find(page=2, per_page=1)
    assert members_1.total == 2
    assert len(members_1.items) == 1
    assert members_1.items[0] != members_0.items[0]

    members = member_service.find(page=1, per_page=2)
    assert members.total == 2
    assert len(members.items) == 2


def test_member_find_w_bad_pagination():
    """
    GIVEN 2 member instance in the database
    WHEN the find method is called with invalid pagination
    THEN it should return the 0 member
    """
    members = member_service.find(page=3, per_page=3)
    assert members.total == 2
    assert len(members.items) == 0


def test_member_find_by_league_uuid_none_found():
    """
    GIVEN 2 member instance in the database
    WHEN the find method is called with a random league_uuid
    THEN it should return the 0 member
    """
    members = member_service.find(league_uuid=generate_uuid())
    assert members.total == 0
    assert len(members.items) == 0


def test_member_find_by_non_existent_column():
    """
    GIVEN 2 member instance in the database
    WHEN the find method is called with a random column
    THEN it should return the 0 member and ManualException with code 400
    """
    try:
        _ = member_service.find(junk=generate_uuid())
    except ManualException as ex:
        assert ex.code == 400


def test_member_find_by_non_existent_include():
    """
    GIVEN 2 member instance in the database
    WHEN the find method is called with a random include
    THEN it should return the 0 member and ManualException with code 400
    """
    try:
        _ = member_service.find(include=['junk'])
    except ManualException as ex:
        assert ex.code == 400


def test_member_find_by_non_existent_expand():
    """
    GIVEN 2 member instance in the database
    WHEN the find method is called with a random expand
    THEN it should return the 0 member and ManualException with code 400
    """
    try:
        _ = member_service.find(expand=['junk'])
    except ManualException as ex:
        assert ex.code == 400


###########
# Create
###########
def test_member_create(reset_db, pause_notification):
    """
    GIVEN 0 member instance in the database
    WHEN the create method is called
    THEN it should return 1 member and add 1 member instance into the database
    """
    member = member_service.create(status='pending', user_uuid=pytest.user_uuid,
                                   email=pytest.email, username=pytest.username,
                                   league_uuid=pytest.league_uuid, display_name=pytest.display_name,
                                   country=pytest.country)

    assert member.uuid is not None
    assert member.user_uuid == pytest.user_uuid


def test_member_create_dup(pause_notification):
    """
    GIVEN 1 member instance in the database
    WHEN the create method is called with the exact same parameters of an existing member
    THEN it should return 0 member and add 0 member instance into the database and ManualException with code 500
    """
    try:
        _ = member_service.create(status='pending', user_uuid=pytest.user_uuid,
                                  email=pytest.email, username=pytest.username,
                                  league_uuid=pytest.league_uuid, display_name=pytest.display_name,
                                  country=pytest.country)
    except ManualException as ex:
        assert ex.code == 500


def test_member_create_w_bad_field(reset_db, pause_notification):
    """
    GIVEN 0 member instance in the database
    WHEN the create method is called with a non existent field
    THEN it should return 0 member and add 0 member instance into the database and ManualException with code 500
    """
    try:
        _ = member_service.create(status='pending', user_uuid=pytest.user_uuid,
                                  email=pytest.email, username=pytest.username,
                                  league_uuid=pytest.league_uuid, display_name=pytest.display_name,
                                  country=pytest.country, junk='junk')
    except ManualException as ex:
        assert ex.code == 500


###########
# Update
###########
def test_member_update(reset_db, pause_notification, seed_member):
    """
    GIVEN 1 member instance in the database
    WHEN the update method is called
    THEN it should return 1 member and update 1 member instance into the database
    """
    member = member_service.update(uuid=pytest.member.uuid, display_name='Junk Head')
    assert member.uuid is not None

    members = member_service.find(uuid=member.uuid)
    assert members.total == 1
    assert len(members.items) == 1


def test_member_update_w_bad_uuid(reset_db, pause_notification, seed_member):
    """
    GIVEN 1 member instance in the database
    WHEN the update method is called with random uuid
    THEN it should return 0 member and update 0 member instance into the database and ManualException with code 404
    """
    try:
        _ = member_service.update(uuid=generate_uuid(), display_name='Junk Head')
    except ManualException as ex:
        assert ex.code == 404


def test_member_update_w_bad_field(pause_notification):
    """
    GIVEN 1 member instance in the database
    WHEN the update method is called with bad field
    THEN it should return 0 member and update 0 member instance in the database and ManualException with code 400
    """
    try:
        _ = member_service.update(uuid=pytest.member.uuid, junk='junk')
    except ManualException as ex:
        assert ex.code == 400


###########
# Apply
###########
def test_member_apply(reset_db, pause_notification, seed_member):
    """
    GIVEN 1 member instance in the database
    WHEN the apply method is called
    THEN it should return 1 member and update 1 member instance in the database
    """
    member = member_service.apply(instance=pytest.member, display_name='Junk Head')
    assert member.uuid is not None

    members = member_service.find(uuid=member.uuid)
    assert members.total == 1
    assert len(members.items) == 1


def test_member_apply_w_bad_member(reset_db, pause_notification, seed_member):
    """
    GIVEN 1 member instance in the database
    WHEN the apply method is called with random uuid
    THEN it should return 0 member and update 0 member instance in the database and ManualException with code 404
    """
    try:
        _ = member_service.apply(instance=generate_uuid(), display_name='Junk Head')
    except ManualException as ex:
        assert ex.code == 400


def test_member_apply_w_bad_field(pause_notification):
    """
    GIVEN 1 member instance in the database
    WHEN the apply method is called with bad field
    THEN it should return 0 member and update 0 member instance in the database and ManualException with code 400
    """
    try:
        _ = member_service.apply(instance=pytest.member, junk='junk')
    except ManualException as ex:
        assert ex.code == 400


###########
# Misc
###########
def test_fetch_league(reset_db, mock_fetch_league):
    """
    GIVEN 0 instance in the db
    WHEN the fetch_league method is called
    THEN it should return a league
    """
    league = member_service.fetch_league(uuid=str(pytest.league_uuid))
    assert league['uuid'] == str(pytest.league_uuid)


def test_fetch_contest(mock_fetch_contest):
    """
    GIVEN 0 instance in the db
    WHEN the fetch_contest method is called
    THEN it should return a contest
    """
    contest = member_service.fetch_contest(uuid=str(pytest.contest_uuid))
    assert contest['uuid'] == str(pytest.contest_uuid)


def test_fetch_account(mock_fetch_account):
    """
    GIVEN 0 instance in the db
    WHEN the fetch_account method is called
    THEN it should return a account
    """
    account = member_service.fetch_account(uuid=str(pytest.account_uuid))
    assert account['uuid'] == str(pytest.account_uuid)


def test_find_standings(pause_notification, seed_member, seed_other_member, seed_stat, seed_other_stat):
    """
    GIVEN 2 member instance and 2 stat instance in the db
    WHEN the find_standings method is called
    THEN it should return both members
    """
    standings = member_service.find_standings(sort_by='event_count')
    assert standings.total == 2


def test_fetch_contest_wager(mock_fetch_contest_wager):
    """
    GIVEN 0 instance in the db
    WHEN the fetch_contest_wager method is called
    THEN it should return a contest_wager
    """
    contest_wager = member_service.fetch_contest_wager(uuid=str(pytest.contest_uuid))
    assert contest_wager['uuid'] == str(pytest.contest_uuid)


def test_check_member_invites(reset_db, pause_notification):
    """
    GIVEN 1 invited member instance in the db
    WHEN the check_member_invites method is called
    THEN it should update any member instances that are in an invited state to active
    """
    member = member_service.create(status='active', email=pytest.email, league_uuid=None, user_uuid=pytest.user_uuid)
    league_member = member_service.create(status='invited', email=pytest.email, league_uuid=pytest.league_uuid)
    member_service.check_member_invites(instance=member)

    members = member_service.find(uuid=league_member.uuid)
    assert members.items[0].status.name == 'active'
