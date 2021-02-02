import logging

from ..services import MemberService, StatService, WalletService


class League:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.member_service = MemberService()
        self.stat_service = StatService()
        self.wallet_service = WalletService()

    def handle_event(self, key, data):
        if key == 'member_created':
            self.logger.info('member created')
            params = {
                'user_uuid': data['user_uuid'],
                'email': data['email'],
                'league_uuid': data['league_uuid'],
                'status': 'invited',
            }
            # fill in shared fields with the league-less existing (root) user
            if data['user_uuid']:
                members = self.member_service.find(user_uuid=data['user_uuid'], league_uuid=None)
                if members.total:
                    existing_member = members.items[0]
                    params['display_name'] = existing_member.display_name
                    params['username'] = existing_member.username
                    params['country'] = existing_member.country
                    params['status'] = 'active'

            new_member = self.member_service.create(**params)
            _ = self.stat_service.create(member=new_member)
            _ = self.wallet_service.create(member=new_member)
