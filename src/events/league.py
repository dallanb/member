import logging

from ..services import MemberService, StatService


class League:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.member_service = MemberService()
        self.stat_service = StatService()

    def handle_event(self, key, data):
        if key == 'member_created':
            self.logger.info('member created')
            member = self.member_service.create(user_uuid=data['user_uuid'], username=data['username'],
                                                email=data['email'], display_name=data['display_name'],
                                                league_uuid=data['league_uuid'], country=data['country'],
                                                status='active' if data.get('is_owner', False) else 'pending')
            _ = self.stat_service.create(member=member)
