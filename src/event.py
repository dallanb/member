import logging
import traceback

from .events import *


def new_event_listener(event):
    topic = event.topic
    key = event.key
    data = event.value
    if topic == 'accounts':
        try:
            Account().handle_event(key=key, data=data)
        except Exception as ex:
            logging.error(traceback.format_exc())
            logging.error('Account event err')
    if topic == 'contests':
        try:
            Contest().handle_event(key=key, data=data)
        except Exception as ex:
            logging.error(traceback.format_exc())
            logging.error('Contest event err')
    if topic == 'courses':
        try:
            Course().handle_event(key=key, data=data)
        except Exception as ex:
            logging.error(traceback.format_exc())
            logging.error('Course event err')
    if topic == 'leagues':
        try:
            League().handle_event(key=key, data=data)
        except Exception as ex:
            logging.error(traceback.format_exc())
            logging.error('League event err')
    if topic == 'wagers':
        try:
            Wager().handle_event(key=key, data=data)
        except Exception as ex:
            logging.error(traceback.format_exc())
            logging.error('Wager event err')
