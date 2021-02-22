import pytest
from sqlalchemy import inspect


def fetch_contest(self, uuid):
    if uuid == str(pytest.contest_uuid):
        contest = {
            'league': str(pytest.league_uuid),
            'name': 'Super Contest',
            'uuid': uuid,
            'status': 'completed',
            'participants': {},
            'owner': str(pytest.user_uuid),
            'location': 'Northlands Golf Course',
        }
        if pytest.member is not None and not inspect(pytest.member).detached:
            contest['participants'][str(pytest.member.uuid)] = {
                'score': -1,
                'status': 'completed',
                'strokes': '72',
                'member_uuid': str(pytest.member.uuid),
                'display_name': pytest.display_name
            }
        if pytest.other_member is not None and not inspect(pytest.other_member).detached:
            contest['participants'][str(pytest.other_member.uuid)] = {
                'score': 1,
                'status': 'completed',
                'strokes': '74',
                'member_uuid': str(pytest.other_member.uuid),
                'display_name': pytest.other_display_name
            }
        return contest
    else:
        return None
