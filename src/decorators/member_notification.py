from functools import wraps

from src.notifications import member_pending, member_invited, member_active, member_inactive, avatar_created, \
    display_name_updated


class member_notification:
    def __init__(self, operation):
        self.operation = operation

    def __call__(self, f):
        @wraps(f)
        def wrap(*args, **kwargs):
            prev_instance = {**kwargs.get('instance').__dict__} if kwargs.get('instance') else None
            new_instance = f(*args, **kwargs)

            if self.operation == 'create':
                self.create(new_instance=new_instance)
            if self.operation == 'update':
                self.update(prev_instance=prev_instance, new_instance=new_instance, args=kwargs)

            return new_instance

        return wrap

    @staticmethod
    def create(new_instance):
        if new_instance.status.name == 'pending':
            member_pending.from_data(member=new_instance).notify()
        elif new_instance.status.name == 'invited':
            member_invited.from_data(member=new_instance).notify()

    @staticmethod
    def update(prev_instance, new_instance,
               args):
        if prev_instance and prev_instance.get('status') and prev_instance['status'].name != new_instance.status.name:
            if new_instance.status.name == 'active':
                member_active.from_data(member=new_instance).notify()
            elif new_instance.status.name == 'inactive':
                member_inactive.from_data(member=new_instance).notify()
        if args.get('avatar'):
            avatar_created.from_data(member=new_instance, avatar=args['avatar']).notify()
        if prev_instance and prev_instance.get('display_name') and prev_instance[
            'display_name'] != new_instance.display_name:
            display_name_updated.from_data(member=new_instance).notify()
