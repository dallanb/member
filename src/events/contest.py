import logging

from ..common import find_lowest_scoring_participant, sort_lowest_scoring_participant
from ..services import MemberService, StatService


class Contest:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.member_service = MemberService()
        self.stat_service = StatService()

    def handle_event(self, key, data):
        if key == 'participant_active' or key == 'owner_active':
            self.logger.info('participant active')
            members = self.member_service.find(uuid=data['member_uuid'])
            if members.total:
                member = members.items[0]
                stats = self.stat_service.find(member_uuid=member.uuid)
                if stats.total:
                    stat = stats.items[0]
                    self.stat_service.apply(instance=stat, event_count=stat.event_count + 1)
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
                members = [lowest_scorer['member_uuid'] for lowest_scorer in lowest_scorers[:len(payouts)]]
                member_stats = self.stat_service.find_league_member_stats(league_uuid=data['league_uuid'],
                                                                          members=members)
                if member_stats.total:
                    member_stats_dict = {str(member_stat_item.member_uuid): member_stat_item for member_stat_item in
                                         member_stats.items}
                    for index, payout in enumerate(payouts):
                        member_uuid = members[index]
                        member_stat = member_stats_dict[member_uuid]
                        self.stat_service.apply(instance=member_stat, winning_total=member_stat.winning_total + payout)
