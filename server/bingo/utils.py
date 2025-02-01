from .models import Friendship


def check_access(current_user, target_user):
    if current_user.is_staff:
        return True  # Can view any
    elif (current_user.is_authenticated and
          (Friendship.objects.filter(requester=current_user, receiver=target_user).exists() or
           Friendship.objects.filter(requester=target_user, receiver=current_user).exists())):
        return target_user.visibility != 0  # Can view any except staff
    return target_user.visibility == 2  # Only can view public
