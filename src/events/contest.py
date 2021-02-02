import logging

from ..common import sort_lowest_scoring_participant
from ..services import MemberService, StatService, WalletService


class Contest:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.member_service = MemberService()
        self.stat_service = StatService()
        self.wallet_service = WalletService()

    def handle_event(self, key, data):
        if key == 'participant_active' or key == 'owner_active':
            self.logger.info('participant active')
            members = self.member_service.find(uuid=data['member_uuid'], include=['stat', 'wallet'])
            if members.total:
                member = members.items[0]
                self.stat_service.apply(instance=member.stat, event_count=member.stat.event_count + 1)
        if key == 'contest_completed':
            self.logger.info('contest completed')
            contest = self.member_service.fetch_contest(uuid=data['uuid'])
            participants = contest['participants']
            lowest_scorers = sort_lowest_scoring_participant(participants)
            stats = self.stat_service.find(member_uuid=lowest_scorers[0]['member_uuid'])
            if stats.total:
                stat = stats.items[0]
                self.stat_service.apply(instance=stat, win_count=stat.win_count + 1)
            if data['league_uuid']:
                wager = self.member_service.fetch_contest_wager(uuid=data['uuid'])
                payouts = wager['party_payouts']
                # payouts are only available to league members so we find all members belonging to a league
                lowest_scoring_members = [lowest_scorer['member_uuid'] for lowest_scorer in
                                          lowest_scorers[:len(payouts)]]
                members = self.member_service.find(league_uuid=data['league_uuid'],
                                                   within={'uuid': lowest_scoring_members},
                                                   include=['stat', 'wallet'])
                if members.total:
                    members_dict = {str(member.uuid): member for
                                    member in
                                    members.items}
                    for index, member in enumerate(lowest_scoring_members):
                        member_stat = members_dict[member].stat
                        member_wallet = members_dict[member].wallet
                        payout = payouts[str(index + 1)]
                        self.stat_service.apply(instance=member_stat, winning_total=member_stat.winning_total + payout)
                        self.wallet_service.apply(instance=member_wallet, balance=member_wallet.balance + payout)
