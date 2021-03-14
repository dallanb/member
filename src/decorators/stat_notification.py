from functools import wraps

from src.notifications import stat_created, stat_updated


class stat_notification:
    def __init__(self, operation):
        self.operation = operation

    def __call__(self, f):
        @wraps(f)
        def wrap(*args, **kwargs):
            new_instance = f(*args, **kwargs)

            if self.operation == 'create':
                self.create(new_instance=new_instance)
            if self.operation == 'update':
                self.update(new_instance=new_instance)

            return new_instance

        return wrap

    @staticmethod
    def create(new_instance):
        stat_created.from_data(stat=new_instance).notify()

    @staticmethod
    def update(new_instance):
        stat_updated.from_data(stat=new_instance).notify()
