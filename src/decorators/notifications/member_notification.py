from functools import wraps

from src.notifications import member_pending, member_invited, member_active, member_inactive, display_name_updated, \
    country_updated


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
            elif self.operation == 'update':
                self.update(prev_instance=prev_instance, new_instance=new_instance, args=kwargs)
            elif self.operation == 'update_user':
                self.update_user(res=new_instance, args=kwargs)

            return new_instance

        return wrap

    @staticmethod
    def create(new_instance):
        if new_instance.status.name == 'active':
            member_active.from_data(member=new_instance).notify()
        elif new_instance.status.name == 'pending':
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
        if prev_instance and prev_instance.get('display_name') and prev_instance[
            'display_name'] != new_instance.display_name:
            display_name_updated.from_data(member=new_instance).notify()

    @staticmethod
    # res identifies the number of updates that were actually made
    def update_user(res, args):
        user_uuid = args.get('user_uuid')
        if res > 0:
            if args.get('country'):
                country_updated.from_data(uuid=user_uuid).notify()
