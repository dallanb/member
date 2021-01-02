import logging

from ..services import MemberService


class League:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.member_service = MemberService()

    def handle_event(self, key, data):
        if key == 'member_created':
            self.logger.info('member created')
            _ = self.member_service.create(user_uuid=data['user_uuid'], username=data['username'],
                                           email=data['email'], display_name=data['display_name'],
                                           league_uuid=data['league_uuid'], country=data['country'], status='pending')
