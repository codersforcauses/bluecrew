from .models import User
from datetime import timedelta
from django.utils import timezone
import logging

logger = logging.getLogger(__file__)


def delete_inactive():
    to_delete = User.objects.filter(is_active=False, created_at__lte=(
        timezone.now() - timedelta(days=1)))
    if to_delete.exists():
        deleted_count, _ = to_delete.delete()
        logger.info(f"{deleted_count} inactive users deleted.")
    else:
        logger.info("There are currently no inactive users.")
