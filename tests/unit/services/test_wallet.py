import pytest

from src import services, ManualException
from tests.helpers import generate_uuid

wallet_service = services.WalletService()


###########
# Find
###########
def test_wallet_find(reset_db, pause_notification, seed_member, seed_wallet):
    """
    GIVEN 1 wallet instance in the database
    WHEN the find method is called
    THEN it should return 1 wallet
    """
    wallets = wallet_service.find()

    assert wallets.total == 1
    assert len(wallets.items) == 1


def test_wallet_find_by_uuid():
    """
    GIVEN 1 wallet instance in the database
    WHEN the find method is called with uuid
    THEN it should return 1 wallet
    """

    wallets = wallet_service.find(uuid=pytest.wallet.uuid)

    assert wallets.total == 1
    assert len(wallets.items) == 1
    wallet = wallets.items[0]
    assert wallet.uuid == pytest.wallet.uuid


def test_wallet_find_expand_member():
    """
    GIVEN 1 wallet instance in the database
    WHEN the find method is called with uuid and with expand argument to also return member
    THEN it should return 1 wallet
    """

    wallets = wallet_service.find(uuid=pytest.wallet.uuid, expand=['member'])

    assert wallets.total == 1
    assert len(wallets.items) == 1
    wallet = wallets.items[0]
    assert wallet.member is not None
    assert wallet.member.uuid is not None


def test_wallet_find_by_member_uuid():
    """
    GIVEN 1 wallet instance in the database
    WHEN the find method is called with member_uuid
    THEN it should return as many wallet exist for that member_uuid
    """

    wallets = wallet_service.find(member_uuid=pytest.member.uuid)

    assert wallets.total == 1
    assert len(wallets.items) == 1


def test_wallet_find_w_pagination(pause_notification, seed_other_member, seed_other_wallet):
    """
    GIVEN 2 wallet instance in the database
    WHEN the find method is called with valid pagination
    THEN it should return the number of wallets defined in the pagination arguments
    """
    wallets_0 = wallet_service.find(page=1, per_page=1)
    assert wallets_0.total == 2
    assert len(wallets_0.items) == 1

    wallets_1 = wallet_service.find(page=2, per_page=1)
    assert wallets_1.total == 2
    assert len(wallets_1.items) == 1

    wallets = wallet_service.find(page=1, per_page=2)
    assert wallets.total == 2
    assert len(wallets.items) == 2


def test_wallet_find_w_bad_pagination():
    """
    GIVEN 2 wallet instance in the database
    WHEN the find method is called with invalid pagination
    THEN it should return the 0 wallet
    """
    wallets = wallet_service.find(page=3, per_page=3)
    assert wallets.total == 2
    assert len(wallets.items) == 0


def test_wallet_find_by_non_existent_column():
    """
    GIVEN 2 wallet instance in the database
    WHEN the find method is called with a random column
    THEN it should return the 0 wallet and ManualException with code 400
    """
    try:
        _ = wallet_service.find(junk=generate_uuid())
    except ManualException as ex:
        assert ex.code == 400


def test_wallet_find_by_non_existent_include():
    """
    GIVEN 2 wallet instance in the database
    WHEN the find method is called with a random include
    THEN it should return the 0 wallet and ManualException with code 400
    """
    try:
        _ = wallet_service.find(include=['junk'])
    except ManualException as ex:
        assert ex.code == 400


def test_wallet_find_by_non_existent_expand():
    """
    GIVEN 2 wallet instance in the database
    WHEN the find method is called with a random expand
    THEN it should return the 0 wallet and ManualException with code 400
    """
    try:
        _ = wallet_service.find(expand=['junk'])
    except ManualException as ex:
        assert ex.code == 400


###########
# Create
###########
def test_wallet_create(reset_db, pause_notification, seed_member):
    """
    GIVEN 0 wallet instance in the database
    WHEN the create method is called
    THEN it should return 1 wallet and add 1 wallet instance into the database
    """

    wallet = wallet_service.create(member=pytest.member)
    assert wallet.uuid is not None
    assert wallet.member is not None


def test_wallet_create_dup_member(pause_notification):
    """
    GIVEN 1 wallet instance in the database
    WHEN the create method is called with duplicate member
    THEN it should return 0 wallet and add 0 wallet instance into the database and ManualException with code 500
    """

    try:
        _ = wallet_service.create(member=pytest.member)
    except ManualException as ex:
        assert ex.code == 500


def test_wallet_create_wo_member(pause_notification):
    """
    GIVEN 1 wallet instance in the database
    WHEN the create method is called without member
    THEN it should return 0 wallet and add 0 wallet instance into the database and ManualException with code 500
    """

    try:
        _ = wallet_service.create()
    except ManualException as ex:
        assert ex.code == 500


def test_wallet_create_w_non_existent_member_uuid(pause_notification):
    """
    GIVEN 1 wallet instance in the database
    WHEN the create method is called with non existent member uuid
    THEN it should return 0 wallet and add 0 wallet instance into the database and ManualException with code 500
    """

    try:
        _ = wallet_service.create(member_uuid=generate_uuid())
    except ManualException as ex:
        assert ex.code == 500


def test_wallet_create_w_bad_field(reset_db, pause_notification, seed_member):
    """
    GIVEN 0 wallet instance in the database
    WHEN the create method is called with a non existent field
    THEN it should return 0 wallet and add 0 wallet instance into the database and ManualException with code 500
    """

    try:
        _ = wallet_service.create(member=pytest.member, junk='junk')
    except ManualException as ex:
        assert ex.code == 500


###########
# Update
###########
def test_wallet_update(reset_db, pause_notification, seed_member, seed_wallet):
    """
    GIVEN 1 wallet instance in the database
    WHEN the update method is called
    THEN it should return 1 wallet and update 1 wallet instance into the database
    """
    wallet = wallet_service.update(uuid=pytest.wallet.uuid, balance=pytest.wallet.balance + 1)
    assert wallet.uuid is not None

    wallets = wallet_service.find(uuid=wallet.uuid)
    assert wallets.total == 1
    assert len(wallets.items) == 1


def test_wallet_update_w_bad_uuid(reset_db, pause_notification, seed_member, seed_wallet):
    """
    GIVEN 1 wallet instance in the database
    WHEN the update method is called with random uuid
    THEN it should return 0 wallet and update 0 wallet instance into the database and ManualException with code 404
    """
    try:
        _ = wallet_service.update(uuid=generate_uuid(), balance=pytest.wallet.balance + 1)
    except ManualException as ex:
        assert ex.code == 404


def test_wallet_update_w_bad_field(pause_notification):
    """
    GIVEN 1 wallet instance in the database
    WHEN the update method is called with bad field
    THEN it should return 0 wallet and update 0 wallet instance in the database and ManualException with code 400
    """
    try:
        _ = wallet_service.update(uuid=pytest.wallet.uuid, junk='junk')
    except ManualException as ex:
        assert ex.code == 400


###########
# Apply
###########
def test_wallet_apply(reset_db, pause_notification, seed_member, seed_wallet):
    """
    GIVEN 1 wallet instance in the database
    WHEN the apply method is called
    THEN it should return 1 wallet and update 1 wallet instance in the database
    """
    wallet = wallet_service.apply(instance=pytest.wallet, balance=pytest.wallet.balance + 1)
    assert wallet.uuid is not None

    wallets = wallet_service.find(uuid=wallet.uuid)
    assert wallets.total == 1
    assert len(wallets.items) == 1


def test_wallet_apply_w_bad_wallet(reset_db, pause_notification, seed_member, seed_wallet):
    """
    GIVEN 1 wallet instance in the database
    WHEN the apply method is called with random uuid
    THEN it should return 0 wallet and update 0 wallet instance in the database and ManualException with code 404
    """
    try:
        _ = wallet_service.apply(instance=generate_uuid(), balance=pytest.wallet.balance + 1)
    except ManualException as ex:
        assert ex.code == 400


def test_wallet_apply_w_bad_field(pause_notification):
    """
    GIVEN 1 wallet instance in the database
    WHEN the apply method is called with bad field
    THEN it should return 0 wallet and update 0 wallet instance in the database and ManualException with code 400
    """
    try:
        _ = wallet_service.apply(instance=pytest.wallet, junk='junk')
    except ManualException as ex:
        assert ex.code == 400
