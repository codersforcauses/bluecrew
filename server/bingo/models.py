from django.db import models # noqa


class Challenge(models.Model):
    CHALLENGE_TYPES = [
        ('connect', 'Connect'),
        ('understand', 'Understand'),
        ('act', 'Act'),
    ]

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    challenge_type = models.CharField(max_length=10, choices=CHALLENGE_TYPES)
    points = models.PositiveIntegerField()
    total_completions = models.PositiveIntegerField(default=0)

    def __str__(self):
        # Format when printed: Challenge ID: Name (Challenge Type)
        return f"Challenge {self.id}: {self.name} ({self.challenge_type})"
