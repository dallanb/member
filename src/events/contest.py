import logging
from itertools import groupby

from ..common import sort_lowest_scoring_participant, ManualException, has_tie
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
        if key == 'participant_completed':
            self.logger.info('participant completed')
            members = self.member_service.find(uuid=data['member_uuid'], include=['stat', 'wallet'])
            if members.total:
                member = members.items[0]
                self.stat_service.apply(instance=member.stat, event_count=member.stat.event_count + 1)
        if key == 'contest_completed':
            self.logger.info('contest completed')
            contest = self.member_service.fetch_contest(uuid=data['uuid'])
            if contest is None:
                raise ManualException(err=f'contest with uuid: {data["uuid"]} not found')

            participants = contest['participants']
            lowest_scorers = sort_lowest_scoring_participant(participants)
            # if there was a winner than credit a win
            if not has_tie(sorted_participants=lowest_scorers):
                stats = self.stat_service.find(member_uuid=lowest_scorers[0]['member_uuid'])
                if stats.total:
                    stat = stats.items[0]
                    self.stat_service.apply(instance=stat, win_count=stat.win_count + 1)
            if data['league_uuid']:
                wager = self.member_service.fetch_contest_wager(uuid=data['uuid'])
                if wager is None:
                    raise ManualException(err=f'contest_wager with uuid: {data["uuid"]} not found')

                payouts = {}
                scorers = {}
                idx = 0
                for _, v in groupby(lowest_scorers, key=lambda x: x['score']):
                    if wager['party_payouts'].get(str(idx + 1), None) is not None:
                        v_members = list(v)
                        ties = len(v_members)
                        payouts[str(idx + 1)] = sum(
                            [wager['party_payouts'].get(str(j + 1), 0.0) for j in range(idx, idx + ties)]) / ties
                        scorers[str(idx + 1)] = v_members
                        idx += ties

                # payouts are only available to league members so we find all members belonging to a league
                scorer_members = []
                for scorer in scorers.values():
                    for scorer_item in scorer:
                        scorer_members.append(scorer_item['member_uuid'])

                members = self.member_service.find(league_uuid=data['league_uuid'],
                                                   within={'uuid': scorer_members},
                                                   include=['stat', 'wallet'])
                if members.total:
                    members_dict = {str(member.uuid): member for
                                    member in
                                    members.items}
                    for k, v in scorers.items():
                        for member in v:
                            member_stat = members_dict[member['member_uuid']].stat
                            member_wallet = members_dict[member['member_uuid']].wallet
                            payout = payouts[k]
                            self.stat_service.apply(instance=member_stat,
                                                    winning_total=member_stat.winning_total + payout)
                            self.wallet_service.add_transaction(instance=member_wallet, amount=payout)
