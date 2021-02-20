import pytest

from src import services


@pytest.fixture(scope="function")
def seed_wallet():
    pytest.wallet = services.WalletService().create(balance=pytest.balance, member=pytest.member)
