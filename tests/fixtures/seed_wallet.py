import pytest

from src import services


@pytest.fixture(scope="function")
def seed_wallet():
    pytest.wallet = services.WalletService().create(balance=pytest.balance, member=pytest.member)


@pytest.fixture(scope="function")
def seed_other_wallet():
    pytest.other_wallet = services.WalletService().create(balance=pytest.other_balance, member=pytest.other_member)
