from django.core.management.base import BaseCommand
from django_q.models import Schedule


class Command(BaseCommand):
    help = "Schedule the task of deleting inactive users who have existed in the database for more than a day."

    def handle(self, *args, **options):
        if not Schedule.objects.filter(name="Start Matchmaking").exists():
            print("Schedule does not exist, making now")
            Schedule.objects.create(
                func='bingo.tasks.delete_inactive',
                name="Delete inactive users",
                schedule_type=Schedule.DAILY,
                repeats=-1
            )
        print(self.style.SUCCESS("Task schedule successfully created."))
