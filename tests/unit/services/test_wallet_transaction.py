import pytest

from src import services, ManualException
from tests.helpers import generate_uuid

wallet_transaction_service = services.WalletTransactionService()


###########
# Find
###########
def test_wallet_transaction_find(reset_db, pause_notification, seed_member, seed_wallet):
    """
    GIVEN 1 transaction instance in the database
    WHEN the find method is called
    THEN it should return 1 transaction
    """
    transactions = wallet_transaction_service.find()

    assert transactions.total == 1
    assert len(transactions.items) == 1
    pytest.transaction = transactions.items[0]


def test_wallet_transaction_find_by_uuid():
    """
    GIVEN 1 transaction instance in the database
    WHEN the find method is called with uuid
    THEN it should return 1 transaction
    """

    transactions = wallet_transaction_service.find(uuid=pytest.transaction.uuid)

    assert transactions.total == 1
    assert len(transactions.items) == 1
    transaction = transactions.items[0]
    assert transaction.uuid == pytest.transaction.uuid


def test_wallet_transaction_find_expand_wallet():
    """
    GIVEN 1 transaction instance in the database
    WHEN the find method is called with uuid and with expand argument to also return wallet
    THEN it should return 1 transaction
    """

    transactions = wallet_transaction_service.find(uuid=pytest.transaction.uuid, expand=['wallet'])

    assert transactions.total == 1
    assert len(transactions.items) == 1
    transaction = transactions.items[0]
    assert transaction.wallet is not None
    assert transaction.wallet.uuid is not None


def test_wallet_transaction_find_by_wallet_uuid():
    """
    GIVEN 1 transaction instance in the database
    WHEN the find method is called with wallet_uuid
    THEN it should return as many transaction exist for that wallet_uuid
    """

    transactions = wallet_transaction_service.find(wallet_uuid=pytest.wallet.uuid)

    assert transactions.total == 1
    assert len(transactions.items) == 1


def test_wallet_transaction_find_by_next_transaction_uuid():
    """
    GIVEN 2 transaction instance in the database
    WHEN the find method is called with next_transaction_uuid
    THEN it should return 1 transaction
    """
    transaction = services.WalletService().add_transaction(instance=pytest.wallet, amount=5.0)
    transactions = wallet_transaction_service.find(next_transaction_uuid=transaction.uuid)

    assert transactions.total == 1
    assert len(transactions.items) == 1


def test_wallet_transaction_find_w_pagination(reset_db, pause_notification, seed_member, seed_wallet, seed_other_member,
                                              seed_other_wallet):
    """
    GIVEN 2 transaction instance in the database
    WHEN the find method is called with valid pagination
    THEN it should return the number of transactions defined in the pagination arguments
    """
    transactions_0 = wallet_transaction_service.find(page=1, per_page=1)
    assert transactions_0.total == 2
    assert len(transactions_0.items) == 1

    transactions_1 = wallet_transaction_service.find(page=2, per_page=1)
    assert transactions_1.total == 2
    assert len(transactions_1.items) == 1

    transactions = wallet_transaction_service.find(page=1, per_page=2)
    assert transactions.total == 2
    assert len(transactions.items) == 2


def test_wallet_transaction_find_w_bad_pagination():
    """
    GIVEN 2 transaction instance in the database
    WHEN the find method is called with invalid pagination
    THEN it should return the 0 transaction
    """
    transactions = wallet_transaction_service.find(page=3, per_page=3)
    assert transactions.total == 2
    assert len(transactions.items) == 0


def test_wallet_transaction_find_by_non_existent_column():
    """
    GIVEN 2 transaction instance in the database
    WHEN the find method is called with a random column
    THEN it should return the 0 transaction and ManualException with code 400
    """
    try:
        _ = wallet_transaction_service.find(junk=generate_uuid())
    except ManualException as ex:
        assert ex.code == 400


def test_wallet_transaction_find_by_non_existent_include():
    """
    GIVEN 2 transaction instance in the database
    WHEN the find method is called with a random include
    THEN it should return the 0 transaction and ManualException with code 400
    """
    try:
        _ = wallet_transaction_service.find(include=['junk'])
    except ManualException as ex:
        assert ex.code == 400


def test_wallet_transaction_find_by_non_existent_expand():
    """
    GIVEN 2 transaction instance in the database
    WHEN the find method is called with a random expand
    THEN it should return the 0 transaction and ManualException with code 400
    """
    try:
        _ = wallet_transaction_service.find(expand=['junk'])
    except ManualException as ex:
        assert ex.code == 400


###########
# Create
###########
def test_wallet_transaction_create(reset_db, pause_notification, seed_member):
    """
    GIVEN 0 transaction instance in the database
    WHEN the create method is called
    THEN it should return 1 transaction and add 1 transaction instance into the database
    """
    instance = services.WalletService()._init(model=services.WalletService().wallet_model, member=pytest.member)
    wallet = services.WalletService()._save(instance=instance)

    transaction = wallet_transaction_service.create(wallet=wallet, amount=wallet.balance, balance=wallet.balance)
    assert transaction.uuid is not None
    assert transaction.wallet is not None


def test_wallet_transaction_create_wo_wallet(reset_db, pause_notification, seed_member):
    """
    GIVEN 1 transaction instance in the database
    WHEN the create method is called without member
    THEN it should return 0 transaction and add 0 transaction instance into the database and ManualException with code 500
    """

    try:
        _ = wallet_transaction_service.create(balance=pytest.balance, amount=pytest.balance)
    except ManualException as ex:
        assert ex.code == 500


def test_wallet_transaction_create_w_non_existent_member_uuid(pause_notification):
    """
    GIVEN 1 transaction instance in the database
    WHEN the create method is called with non existent member uuid
    THEN it should return 0 transaction and add 0 transaction instance into the database and ManualException with code 500
    """

    try:
        _ = wallet_transaction_service.create(member_uuid=generate_uuid(), balance=pytest.balance,
                                              amount=pytest.balance)
    except ManualException as ex:
        assert ex.code == 500


def test_wallet_transaction_create_w_bad_field(reset_db, pause_notification, seed_member):
    """
    GIVEN 0 transaction instance in the database
    WHEN the create method is called with a non existent field
    THEN it should return 0 transaction and add 0 transaction instance into the database and ManualException with code 500
    """

    try:
        _ = wallet_transaction_service.create(member=pytest.member, balance=pytest.balance,
                                              amount=pytest.balance, junk='junk')
    except ManualException as ex:
        assert ex.code == 500


###########
# Update
###########
def test_wallet_transaction_update(reset_db, pause_notification, seed_member, seed_wallet):
    """
    GIVEN 1 transaction instance in the database
    WHEN the update method is called
    THEN it should return 1 transaction and update 1 transaction instance into the database
    """
    transaction = wallet_transaction_service.update(uuid=pytest.wallet.transactions[0].uuid,
                                                    amount=pytest.buy_in + 1)
    assert transaction.uuid is not None

    transactions = wallet_transaction_service.find(uuid=transaction.uuid)
    assert transactions.total == 1
    assert len(transactions.items) == 1


def test_wallet_transaction_update_w_bad_uuid(reset_db, pause_notification, seed_member, seed_wallet):
    """
    GIVEN 1 transaction instance in the database
    WHEN the update method is called with random uuid
    THEN it should return 0 transaction and update 0 transaction instance into the database and ManualException with code 404
    """
    try:
        _ = wallet_transaction_service.update(uuid=generate_uuid(), amount=pytest.buy_in + 1)
    except ManualException as ex:
        assert ex.code == 404


def test_wallet_transaction_update_w_bad_field(pause_notification):
    """
    GIVEN 1 transaction instance in the database
    WHEN the update method is called with bad field
    THEN it should return 0 transaction and update 0 transaction instance in the database and ManualException with code 400
    """
    try:
        _ = wallet_transaction_service.update(uuid=pytest.wallet.transactions[0].uuid, junk='junk')
    except ManualException as ex:
        assert ex.code == 400


###########
# Apply
###########
def test_wallet_transaction_apply(reset_db, pause_notification, seed_member, seed_wallet):
    """
    GIVEN 1 transaction instance in the database
    WHEN the apply method is called
    THEN it should return 1 transaction and update 1 transaction instance in the database
    """
    transaction = wallet_transaction_service.apply(instance=pytest.wallet.transactions[0],
                                                   amount=pytest.buy_in + 1)
    assert transaction.uuid is not None

    transactions = wallet_transaction_service.find(uuid=transaction.uuid)
    assert transactions.total == 1
    assert len(transactions.items) == 1


def test_wallet_transaction_apply_w_bad_wallet(reset_db, pause_notification, seed_member, seed_wallet):
    """
    GIVEN 1 transaction instance in the database
    WHEN the apply method is called with random uuid
    THEN it should return 0 transaction and update 0 transaction instance in the database and ManualException with code 404
    """
    try:
        _ = wallet_transaction_service.apply(instance=generate_uuid(), amount=pytest.buy_in + 1)
    except ManualException as ex:
        assert ex.code == 400


def test_wallet_transaction_apply_w_bad_field(pause_notification):
    """
    GIVEN 1 transaction instance in the database
    WHEN the apply method is called with bad field
    THEN it should return 0 transaction and update 0 transaction instance in the database and ManualException with code 400
    """
    try:
        _ = wallet_transaction_service.apply(instance=pytest.wallet.transactions[0], junk='junk')
    except ManualException as ex:
        assert ex.code == 400
