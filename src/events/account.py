import logging

from ..services import MemberService


class Account:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.member_service = MemberService()

    def handle_event(self, key, data):
        if key == 'account_created':
            self.logger.info('account created')
            _ = self.member_service.create(user_uuid=data['user_uuid'], username=data['username'],
                                           email=data['email'], display_name=data['display_name'],
                                           country=data['country'], status='active')