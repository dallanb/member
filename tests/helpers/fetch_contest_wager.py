import pytest


def fetch_contest_wager(self, uuid):
    if uuid == str(pytest.contest_uuid):
        return {
            'party_payouts': {
                '1': 7.5,
                '2': 2.5
            },
            'uuid': uuid,
            'total_payout': 10.0,
            'parties': 2,
            'buy_in': 5.0,
            'payout_proportions': {
                '1': 0.75,
                '2': 0.25
            }
        }
    else:
        return None
