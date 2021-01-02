from .v1 import MembersAPI, MembersUserAPI, MembersListAPI, MembersListBulkAPI
from .v1 import PingAPI
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
