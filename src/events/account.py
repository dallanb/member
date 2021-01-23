import logging

from ..services import MemberService, StatService


class Account:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.member_service = MemberService()
        self.stat_service = StatService()

    def handle_event(self, key, data):
        if key == 'account_created':
            self.logger.info('account created')
            member = self.member_service.create(user_uuid=data['user_uuid'], username=data['username'],
                                                email=data['email'], display_name=data['display_name'],
                                                country=data['country'], status='active')
            _ = self.stat_service.create(member=member)

            # we also need to check if there are any pending invites for this user
            invited_members = self.member_service.find(status='invited', email=data['email'])
            if invited_members.total:
                for invited_member in invited_members.items:
                    self.member_service.apply(instance=invited_member, user_uuid=data['user_uuid'],
                                              username=data['username'], display_name=data['display_name'],
                                              country=data['country'], status='active')
                    _ = self.stat_service.create(member=member)
