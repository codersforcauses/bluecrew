from .models import User
from datetime import timedelta
from django.utils import timezone


def delete_inactive():
    to_delete = User.objects.filter(is_active=False, created_at__lte=(
        timezone.now() - timedelta(days=1)))
    if count := to_delete.count():
        to_delete.delete()
        print(f"{count} inactive users deleted.")
    else:
        print("There are currently no inactive users.")
