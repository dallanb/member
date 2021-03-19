import logging
from itertools import groupby

from ..common import sort_lowest_scoring_participant, ManualException, has_tie, realign_payouts
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

                payouts = realign_payouts(payouts=wager['party_payouts'], results=lowest_scorers)
                # payouts are only available to league members so we find all members belonging to a league
                lowest_scoring_members = [lowest_scorer['member_uuid'] for lowest_scorer in
                                          lowest_scorers[:len(wager[
                                                                  'party_payouts'])]]  # <- this is broken because we may have x users tied for 1st and only grab 1 user because of this! Overall refactor probably required here!
                members = self.member_service.find(league_uuid=data['league_uuid'],
                                                   within={'uuid': lowest_scoring_members},
                                                   include=['stat', 'wallet'])
                if members.total:
                    members_dict = {str(member.uuid): member for
                                    member in
                                    members.items}
                    idx = 0
                    for _, iterable in groupby(lowest_scorers[:len(wager['party_payouts'])], key=lambda x: x['score']):
                        for member in list(iterable):
                            member_stat = members_dict[member['member_uuid']].stat
                            member_wallet = members_dict[member['member_uuid']].wallet
                            payout = payouts[str(idx + 1)]
                            self.stat_service.apply(instance=member_stat,
                                                    winning_total=member_stat.winning_total + payout)
                            self.wallet_service.add_transaction(instance=member_wallet, amount=payout)
                        idx += len(list(iterable))
