from django.core.management.base import BaseCommand
from bingo.models import Challenge, BingoGrid


class Command(BaseCommand):
    help = "Create a placeholder bingo grid."

    def handle(self, *args, **options):
        if BingoGrid.objects.filter(is_active=True).exists():
            self.stdout.write(self.style.WARNING(
                "This command is only intended to be used when there is no active bingo grid. "
                "An active bingo grid was found, so no action was taken."))
        else:
            placeholder_challenges = []
            challenge_types = ("connect", "understand", "act")
            lorem_ipsum = ("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna "
                           "aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis "
                           "aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint "
                           "occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")
            for i in range(16):
                placeholder_challenges.append(Challenge.objects.create(
                    name=f"Placeholder Challenge #{i}", challenge_type=challenge_types[i % 3], description=lorem_ipsum, points=(i*20)))
            new_grid = BingoGrid.objects.create(is_active=True)
            new_grid.challenges.add(*placeholder_challenges)
            self.stdout.write(self.style.SUCCESS(
                "Placeholder grid successfully added."))
