from functools import wraps


class member_notification:
    def __init__(self, operation):
        self.operation = operation
        self.topic = 'members'
        self._service = None

    def __call__(self, f):
        @wraps(f)
        def wrap(*args, **kwargs):
            self.service = args[0]
            prev_instance = {**kwargs.get('instance').__dict__} if kwargs.get('instance') else None
            new_instance = f(*args, **kwargs)

            if self.operation == 'create':
                self.create(new_instance=new_instance)
            if self.operation == 'update':
                self.update(prev_instance=prev_instance, new_instance=new_instance, args=kwargs)

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
        key = f'member_{new_instance.status.name}'
        value = {
            'uuid': str(new_instance.uuid),
            'league_uuid': str(new_instance.league_uuid) if new_instance.league_uuid else None,
            'user_uuid': str(new_instance.user_uuid) if new_instance.user_uuid else None,
            'email': str(new_instance.email),
            'message': self.generate_message(key=key)
        }
        self.service.notify(topic=self.topic, value=value, key=key)

    def update(self, prev_instance, new_instance,
               args):
        if prev_instance and prev_instance.get('status') and prev_instance['status'].name != new_instance.status.name:
            self.service.check_member_invites(instance=new_instance)
            key = f'member_{new_instance.status.name}'
            value = {
                'uuid': str(new_instance.uuid),
                'league_uuid': str(new_instance.league_uuid),
                'user_uuid': str(new_instance.user_uuid),
                'email': str(new_instance.email),
                'message': self.generate_message(key=key, member=new_instance)
            }
            self.service.notify(topic=self.topic, value=value, key=key)
        if args.get('avatar'):
            key = 'avatar_created'
            value = {
                'uuid': str(args['avatar'].uuid),
                'member_uuid': str(new_instance.uuid),
                'league_uuid': str(new_instance.league_uuid) if new_instance.league_uuid else None,
                'user_uuid': str(new_instance.user_uuid),
                's3_filename': str(args['avatar'].s3_filename)
            }
            self.service.notify(topic=self.topic, value=value, key=key)
        if prev_instance and prev_instance.get('display_name') and prev_instance[
            'display_name'] != new_instance.display_name:
            key = 'display_name_updated'
            value = {
                'uuid': str(new_instance.uuid),
                'user_uuid': str(new_instance.user_uuid),
                'league_uuid': str(new_instance.league_uuid) if new_instance.league_uuid else None,
                'display_name': new_instance.display_name
            }
            self.service.notify(topic=self.topic, value=value, key=key)

    def generate_message(self, key, **kwargs):
        if key == 'member_invited':
            return f"You have been invited to join Tech Tapir"
        else:
            return ''
