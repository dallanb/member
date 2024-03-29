import logging
from http import HTTPStatus

from sqlalchemy.orm import aliased

from .base import Base
from ..decorators.notifications import member_notification
from ..external import Account as AccountExternal, League as LeagueExternal, Contest as ContestExternal, \
    Wager as WagerExternal
from ..models import Member as MemberModel, Stat as StatModel


class Member(Base):
    def __init__(self):
        Base.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.member_model = MemberModel
        self.stat_model = StatModel

    def find(self, **kwargs):
        return self._find(model=self.member_model, **kwargs)

    @member_notification(operation='create')
    def create(self, **kwargs):
        member = self._init(model=self.member_model, **kwargs)
        return self._save(instance=member)

    def update(self, uuid, **kwargs):
        members = self.find(uuid=uuid)
        if not members.total:
            self.error(code=HTTPStatus.NOT_FOUND)
        return self.apply(instance=members.items[0], **kwargs)

    # this will allow us to update all members that have a common user_uuid
    # since multiple members may share one user_uuid (different league_uuid's)
    @member_notification(operation='update_user')
    def update_by_user(self, user_uuid, **kwargs):
        query = self.db.clean_query(model=self.member_model, user_uuid=user_uuid)
        return self._update(query=query, **kwargs)

    @member_notification(operation='update')
    def apply(self, instance, **kwargs):
        # if member status is being updated we will trigger a notification
        member = self._assign_attr(instance=instance, attr=kwargs)
        return self._save(instance=member)

    # eventually integrate caching for these kinds of calls
    def fetch_league(self, uuid):
        try:
            res = LeagueExternal().fetch_league(uuid=uuid)
            league = res['data']['leagues']
            return league
        except TypeError:
            self.logger.error(f'fetch league failed for uuid: {uuid}')
            return None

    # eventually integrate caching for these kinds of calls
    def fetch_contest(self, uuid):
        try:
            res = ContestExternal().fetch_contest_materialized(uuid=uuid)
            contest = res['data']['contests']
            return contest
        except TypeError:
            self.logger.error(f'fetch contest failed for uuid: {uuid}')
            return None

    def fetch_account(self, uuid):
        try:
            res = AccountExternal().fetch_account(uuid=uuid, params={'include': ['address']})
            account = res['data']['accounts']
            return account
        except TypeError:
            self.logger.error(f'fetch account failed for uuid: {uuid}')
            return None

    def find_standings(self, sort_by=None, **kwargs):
        query = self.db.clean_query(model=self.member_model, **kwargs)
        # join aliased table
        if sort_by is not None:
            entity = aliased(self.stat_model)
            query = query.join(entity)
            query = self.db.apply_query_order_by(model=entity, query=query, sort_by=sort_by)
        return self.db.run_query(query=query)

    # eventually integrate caching for these kinds of calls
    def fetch_contest_wager(self, uuid):
        try:
            res = WagerExternal().fetch_contest_wager(uuid=uuid)
            contest = res['data']['contest']
            return contest
        except TypeError:
            self.logger.error(f'fetch contest_wager failed for uuid: {uuid}')
            return None

    # Used to update the status of any members with a league_uuid associated with an account that went from invited
    # to active
    def check_member_invites(self, instance):
        members = self.find(email=instance.email, status='invited')
        if members.total:
            for member in members.items:
                self.apply(instance=member, status='active', user_uuid=instance.user_uuid)
