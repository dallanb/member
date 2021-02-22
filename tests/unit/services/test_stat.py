import pytest

from src import services, ManualException
from tests.helpers import generate_uuid

stat_service = services.StatService()


###########
# Find
###########
def test_stat_find(reset_db, pause_notification, seed_member, seed_stat):
    """
    GIVEN 1 stat instance in the database
    WHEN the find method is called
    THEN it should return 1 stat
    """
    stats = stat_service.find()

    assert stats.total == 1
    assert len(stats.items) == 1


def test_stat_find_by_uuid():
    """
    GIVEN 1 stat instance in the database
    WHEN the find method is called with uuid
    THEN it should return 1 stat
    """

    stats = stat_service.find(uuid=pytest.stat.uuid)

    assert stats.total == 1
    assert len(stats.items) == 1
    stat = stats.items[0]
    assert stat.uuid == pytest.stat.uuid


def test_stat_find_expand_member():
    """
    GIVEN 1 stat instance in the database
    WHEN the find method is called with uuid and with expand argument to also return member
    THEN it should return 1 stat
    """

    stats = stat_service.find(uuid=pytest.stat.uuid, expand=['member'])

    assert stats.total == 1
    assert len(stats.items) == 1
    stat = stats.items[0]
    assert stat.member is not None
    assert stat.member.uuid is not None


def test_stat_find_by_member_uuid():
    """
    GIVEN 1 stat instance in the database
    WHEN the find method is called with member_uuid
    THEN it should return as many stat exist for that member_uuid
    """

    stats = stat_service.find(member_uuid=pytest.member.uuid)

    assert stats.total == 1
    assert len(stats.items) == 1


def test_stat_find_w_pagination(pause_notification, seed_other_member, seed_other_stat):
    """
    GIVEN 2 stat instance in the database
    WHEN the find method is called with valid pagination
    THEN it should return the number of stats defined in the pagination arguments
    """
    stats_0 = stat_service.find(page=1, per_page=1)
    assert stats_0.total == 2
    assert len(stats_0.items) == 1

    stats_1 = stat_service.find(page=2, per_page=1)
    assert stats_1.total == 2
    assert len(stats_1.items) == 1

    stats = stat_service.find(page=1, per_page=2)
    assert stats.total == 2
    assert len(stats.items) == 2


def test_stat_find_w_bad_pagination():
    """
    GIVEN 2 stat instance in the database
    WHEN the find method is called with invalid pagination
    THEN it should return the 0 stat
    """
    stats = stat_service.find(page=3, per_page=3)
    assert stats.total == 2
    assert len(stats.items) == 0


def test_stat_find_by_non_existent_column():
    """
    GIVEN 2 stat instance in the database
    WHEN the find method is called with a random column
    THEN it should return the 0 stat and ManualException with code 400
    """
    try:
        _ = stat_service.find(junk=generate_uuid())
    except ManualException as ex:
        assert ex.code == 400


def test_stat_find_by_non_existent_include():
    """
    GIVEN 2 stat instance in the database
    WHEN the find method is called with a random include
    THEN it should return the 0 stat and ManualException with code 400
    """
    try:
        _ = stat_service.find(include=['junk'])
    except ManualException as ex:
        assert ex.code == 400


def test_stat_find_by_non_existent_expand():
    """
    GIVEN 2 stat instance in the database
    WHEN the find method is called with a random expand
    THEN it should return the 0 stat and ManualException with code 400
    """
    try:
        _ = stat_service.find(expand=['junk'])
    except ManualException as ex:
        assert ex.code == 400


###########
# Create
###########
def test_stat_create(reset_db, pause_notification, seed_member):
    """
    GIVEN 0 stat instance in the database
    WHEN the create method is called
    THEN it should return 1 stat and add 1 stat instance into the database
    """

    stat = stat_service.create(member=pytest.member)
    assert stat.uuid is not None
    assert stat.member is not None


def test_stat_create_dup_member(pause_notification):
    """
    GIVEN 1 stat instance in the database
    WHEN the create method is called with duplicate member
    THEN it should return 0 stat and add 0 stat instance into the database and ManualException with code 500
    """

    try:
        _ = stat_service.create(member=pytest.member)
    except ManualException as ex:
        assert ex.code == 500


def test_stat_create_wo_member(pause_notification):
    """
    GIVEN 1 stat instance in the database
    WHEN the create method is called without member
    THEN it should return 0 stat and add 0 stat instance into the database and ManualException with code 500
    """

    try:
        _ = stat_service.create()
    except ManualException as ex:
        assert ex.code == 500


def test_stat_create_w_non_existent_member_uuid(pause_notification):
    """
    GIVEN 1 stat instance in the database
    WHEN the create method is called with non existent member uuid
    THEN it should return 0 stat and add 0 stat instance into the database and ManualException with code 500
    """

    try:
        _ = stat_service.create(member_uuid=generate_uuid())
    except ManualException as ex:
        assert ex.code == 500


def test_stat_create_w_bad_field(reset_db, pause_notification, seed_member):
    """
    GIVEN 0 stat instance in the database
    WHEN the create method is called with a non existent field
    THEN it should return 0 stat and add 0 stat instance into the database and ManualException with code 500
    """

    try:
        _ = stat_service.create(member=pytest.member, junk='junk')
    except ManualException as ex:
        assert ex.code == 500


###########
# Update
###########
def test_stat_update(reset_db, pause_notification, seed_member, seed_stat):
    """
    GIVEN 1 stat instance in the database
    WHEN the update method is called
    THEN it should return 1 stat and update 1 stat instance into the database
    """
    stat = stat_service.update(uuid=pytest.stat.uuid, event_count=pytest.stat.event_count + 1)
    assert stat.uuid is not None

    stats = stat_service.find(uuid=stat.uuid)
    assert stats.total == 1
    assert len(stats.items) == 1


def test_stat_update_w_bad_uuid(reset_db, pause_notification, seed_member, seed_stat):
    """
    GIVEN 1 stat instance in the database
    WHEN the update method is called with random uuid
    THEN it should return 0 stat and update 0 stat instance into the database and ManualException with code 404
    """
    try:
        _ = stat_service.update(uuid=generate_uuid(), event_count=pytest.stat.event_count + 1)
    except ManualException as ex:
        assert ex.code == 404


def test_stat_update_w_bad_field(pause_notification):
    """
    GIVEN 1 stat instance in the database
    WHEN the update method is called with bad field
    THEN it should return 0 stat and update 0 stat instance in the database and ManualException with code 400
    """
    try:
        _ = stat_service.update(uuid=pytest.stat.uuid, junk='junk')
    except ManualException as ex:
        assert ex.code == 400


###########
# Apply
###########
def test_stat_apply(reset_db, pause_notification, seed_member, seed_stat):
    """
    GIVEN 1 stat instance in the database
    WHEN the apply method is called
    THEN it should return 1 stat and update 1 stat instance in the database
    """
    stat = stat_service.apply(instance=pytest.stat, event_count=pytest.stat.event_count + 1)
    assert stat.uuid is not None

    stats = stat_service.find(uuid=stat.uuid)
    assert stats.total == 1
    assert len(stats.items) == 1


def test_stat_apply_w_bad_stat(reset_db, pause_notification, seed_member, seed_stat):
    """
    GIVEN 1 stat instance in the database
    WHEN the apply method is called with random uuid
    THEN it should return 0 stat and update 0 stat instance in the database and ManualException with code 404
    """
    try:
        _ = stat_service.apply(instance=generate_uuid(), event_count=pytest.stat.event_count + 1)
    except ManualException as ex:
        assert ex.code == 400


def test_stat_apply_w_bad_field(pause_notification):
    """
    GIVEN 1 stat instance in the database
    WHEN the apply method is called with bad field
    THEN it should return 0 stat and update 0 stat instance in the database and ManualException with code 400
    """
    try:
        _ = stat_service.apply(instance=pytest.stat, junk='junk')
    except ManualException as ex:
        assert ex.code == 400
