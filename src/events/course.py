import logging

from ..services import MemberService, StatService, WalletService


class Course:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.member_service = MemberService()
        self.stat_service = StatService()
        self.wallet_service = WalletService()

    def handle_event(self, key, data):
        if key == 'course_created':
            self.logger.info('course created')
        if key == 'course_approved':
            self.logger.info('course approved')
            members = self.member_service.find(user_uuid=data['created_by'], include=['wallet'])
            if members.total:
                for member in members.items:
                    self.wallet_service.add_transaction(instance=member.wallet, amount=100.0)
