from .models import Friendship


def check_access(current_user, target_user):
    permission = 'minimum_access'
    if current_user.is_staff():
        permission = "staff"
    elif (current_user.is_authenticated() and
          (Friendship.objects.get(requester=current_user, receiver=target_user or
                                  Friendship.objects.get(requester=current_user, receiver=target_user)))):
        permission = "friend"
    access_map = {
        'minimum_access': ['public'],
        'friend': ['public', 'friends_only'],
        'staff': ['public', 'friends_only', 'staff_only'],
    }
    # Check if the visibility is allowed for the given permission
    return target_user.visibility in access_map[permission]
