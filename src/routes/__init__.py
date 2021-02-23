from .v1 import AvatarsAPI
from .v1 import MembersAPI, MembersUserAPI, MembersListAPI, MembersListBulkAPI, MembersListStandingsAPI
from .v1 import PingAPI
from .v1 import StatsListAPI, StatsAPI, StatsMemberAPI
from .v1 import WalletsListAPI, WalletsAPI, WalletsMemberAPI
from .. import api

# Ping
api.add_resource(PingAPI, '/ping', methods=['GET'])

# Members
api.add_resource(MembersAPI, '/members/<uuid:uuid>', endpoint="member")
api.add_resource(MembersUserAPI, '/members/user/<user_uuid>',
                 endpoint="member_user")  # user_uuid may be 'me' see we will not enforce uuid here
api.add_resource(MembersListAPI, '/members', endpoint="members")
api.add_resource(MembersListBulkAPI, '/members/bulk',
                 endpoint="members_bulk")  # this call could be avoided if i added a contests table?
api.add_resource(MembersListStandingsAPI, '/members/standings', endpoint="members_standings")

# Stats
api.add_resource(StatsAPI, '/stats/<uuid:uuid>', endpoint="stat")
api.add_resource(StatsMemberAPI, '/stats/member/<uuid:member_uuid>', endpoint="stat_member")
api.add_resource(StatsListAPI, '/stats', endpoint="stats")

# Wallets
api.add_resource(WalletsAPI, '/wallets/<uuid:uuid>', endpoint="wallet")
api.add_resource(WalletsMemberAPI, '/wallets/member/<uuid:member_uuid>', endpoint="wallet_member")
api.add_resource(WalletsListAPI, '/wallets', endpoint="wallets")

# Avatars
api.add_resource(AvatarsAPI, '/members/<uuid>/avatars', endpoint="avatar")
