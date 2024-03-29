import logging

from .. import ManualException
from ..services import MemberService, StatService, WalletService


class Account:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.member_service = MemberService()
        self.stat_service = StatService()
        self.wallet_service = WalletService()

    def handle_event(self, key, data):
        if key == 'account_active':
            self.logger.info('account active')
            account = self.member_service.fetch_account(uuid=data['uuid'])
            if account is None:
                raise ManualException(err=f'account with uuid: {data["uuid"]} not found')
            member = self.member_service.create(user_uuid=account['user_uuid'], username=account['username'],
                                                email=account['email'], display_name=account['display_name'],
                                                country=account['address']['country'], status=account['status'])
            _ = self.wallet_service.create(member=member)
            _ = self.stat_service.create(member=member)

            # we also need to check if there are any pending invites for this user
            invited_members = self.member_service.find(status='invited', email=account['email'])
            if invited_members.total:
                for invited_member in invited_members.items:
                    self.member_service.apply(instance=invited_member, user_uuid=account['user_uuid'],
                                              username=account['username'], display_name=account['display_name'],
                                              country=account['address']['country'], status=account['status'])
        elif key == 'display_name_updated':
            self.logger.info('display_name updated')
            # we only need to handle the update of league-less display_name
            members = self.member_service.find(user_uuid=data['user_uuid'],
                                               league_uuid=None)
            if not members.total:
                raise ManualException(err=f'member with user_uuid: {data["user_uuid"]} and league_uuid: None not found')
            member = members.items[0]
            self.member_service.apply(instance=member, display_name=data['display_name'])
        elif key == 'country_updated':
            self.logger.info('country updated')
            self.member_service.update_by_user(user_uuid=data['user_uuid'], country=data['country'])
