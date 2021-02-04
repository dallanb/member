import logging

from ..services import WalletService


class Wager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.wallet_service = WalletService()

    def handle_event(self, key, data):
        if key == 'stake_created':
            self.logger.info('stake created')
            wallets = self.wallet_service.find(member_uuid= data['member_uuid'])
            if wallets.total:
                wallet = wallets.items[0]
                self.wallet_service.apply(instance=wallet, balance=wallet.balance - data['amount'])
