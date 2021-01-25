import logging
from http import HTTPStatus

from sqlalchemy.orm import aliased

from .base import Base
from ..decorators import member_notification
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
        return Base.find(self, model=self.member_model, **kwargs)

    @member_notification(operation='create')
    def create(self, **kwargs):
        member = self.init(model=self.member_model, **kwargs)
        return self.save(instance=member)

    def update(self, uuid, **kwargs):
        members = self.find(uuid=uuid)
        if not members.total:
            self.error(code=HTTPStatus.NOT_FOUND)
        return self.apply(instance=members.items[0], **kwargs)

    @member_notification(operation='update')
    def apply(self, instance, **kwargs):
        # if member status is being updated we will trigger a notification
        member = self.assign_attr(instance=instance, attr=kwargs)
        return self.save(instance=member)

    # eventually integrate caching for these kinds of calls
    def fetch_league(self, uuid):
        res = LeagueExternal().fetch_league(uuid=uuid)
        league = res['data']['leagues']
        return league

    # eventually integrate caching for these kinds of calls
    def fetch_contest(self, uuid):
        res = ContestExternal().fetch_contest_materialized(uuid=uuid)
        contest = res['data']['contests']
        return contest

    def fetch_account(self, uuid):
        res = AccountExternal().fetch_account(uuid=uuid, params={'include': ['address']})
        account = res['data']['accounts']
        return account

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
        res = WagerExternal().fetch_contest_wager(uuid=uuid)
        contest = res['data']['contest']
        return contest

    def check_member_invites(self, instance):
        members = self.find(email=instance.email, status='invited')
        if members.total:
            for member in members.items:
                self.apply(instance=member, status='active', user_uuid=instance.user_uuid)
