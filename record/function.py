from .models import Group

def get_groups(user):
    return Group.objects.filter(users=user)