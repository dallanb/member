import logging

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
