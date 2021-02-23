import logging

from src.events import Account, Contest, League, Wager


def new_event_listener(event):
    topic = event.topic
    key = event.key
    data = event.value
    if topic == 'accounts_test':
        try:
            Account().handle_event(key=key, data=data)
        except Exception as ex:
            logging.error(ex)
            logging.error('account error')
    if topic == 'contests_test':
        try:
            Contest().handle_event(key=key, data=data)
        except Exception as ex:
            logging.error(ex)
            logging.error('contest error')
    if topic == 'leagues_test':
        try:
            League().handle_event(key=key, data=data)
        except Exception as ex:
            logging.error(ex)
            logging.error('league error')
    if topic == 'wagers_test':
        try:
            Wager().handle_event(key=key, data=data)
        except Exception as ex:
            logging.error(ex)
            logging.error('wager error')
