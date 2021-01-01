import logging

from .events import *


def new_event_listener(event):
    topic = event.topic
    key = event.key
    data = event.value
    if topic == 'accounts':
        try:
            Account().handle_event(key=key, data=data)
        except Exception:
            logging.error('Account event err')
