from functools import wraps


class invite_notification:
    def __init__(self, operation):
        self.operation = operation
        self.topic = 'members'
        self._service = None

    def __call__(self, f):
        @wraps(f)
        def wrap(*args, **kwargs):
            self.service = args[0]
            new_instance = f(*args, **kwargs)

            if self.operation == 'create':
                self.create(new_instance=new_instance)

            return new_instance

        wrap.__doc__ = f.__doc__
        wrap.__name__ = f.__name__
        return wrap

    @property
    def service(self):
        return self._service

    @service.setter
    def service(self, service):
        self._service = service

    def create(self, new_instance):
        key = 'member_invited'
        value = {
            'uuid': str(new_instance.uuid),
            'league_uuid': str(new_instance.league_uuid),
            'email': str(new_instance.email),
            'message': None
        }
        self.service.notify(topic=self.topic, value=value, key=key, )