from django.core.management.base import BaseCommand
from django_q.models import Schedule
from django.utils import timezone


class Command(BaseCommand):
    help = "Schedule the task of deleting inactive users who have existed in the database for more than a day."

    def handle(self, *args, **options):
        task_name = "Delete inactive users"
        if not Schedule.objects.filter(name=task_name).exists():
            self.stdout.write("Schedule does not exist, making now")
            Schedule.objects.create(
                func='bingo.tasks.delete_inactive',
                name=task_name,
                schedule_type=Schedule.DAILY,
                repeats=-1,
                next_run=timezone.now(),
            )
        self.stdout.write(self.style.SUCCESS(
            "Task schedule successfully created."))
