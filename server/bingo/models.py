from django_resized import ResizedImageField
from django.utils.safestring import mark_safe
from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager
from datetime import date
from django.db.models import Q
from django.core.exceptions import ValidationError
from sortedm2m.fields import SortedManyToManyField


class UserManager(BaseUserManager):

    def create_user(self, username, email, password, **extra_fields):

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        user = self.create_user(
            username=username,
            email=email,
            password=password,
            **extra_fields
        )
        user.is_superuser = True
        user.save(using=self.db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    REQUIRED_FIELDS = ["email"]

    user_id = models.AutoField(primary_key=True)

    username = models.CharField(max_length=30, unique=True)
    USERNAME_FIELD = "username"

    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    bio = models.CharField(max_length=300, blank=True)
    total_points = models.IntegerField(default=0)
    birthdate = models.DateField(default=date(2000, 1, 1))
    created_at = models.DateTimeField(auto_now_add=True)

    email = models.EmailField(
        max_length=320,
        unique=True,
        blank=False
    )
    EMAIL_FIELD = 'email'

    class Visibility(models.IntegerChoices):
        PUBLIC = (2, "Public")
        FRIENDS = (1, "Friends Only")
        STAFF = (0, "Staff Only")
    visibility = models.IntegerField(
        choices=Visibility,
        blank=False,
        default=1
    )

    class Gender(models.IntegerChoices):
        MALE = (0, "Male")
        FEMALE = (1, "Female")
        NB = (2, "Non-Binary")
        OTHER = (3, "Other")
        NA = (4, "Prefer not to say")
    gender_identity = models.IntegerField(
        choices=Gender,
        blank=False,
        default=Gender.NA
    )

    class IndigenousIdentity(models.IntegerChoices):
        NA = (0, "Prefer not to say")
        Y = (1, "Yes")
        N = (2, "No")
    indigenous_identity = models.IntegerField(
        choices=IndigenousIdentity,
        blank=False,
        default=IndigenousIdentity.NA
    )

    avatar = models.IntegerField(default=0, choices=map(
        lambda i: (i, f"Avatar {i}"), range(6)))

    is_active = models.BooleanField(default=True)

    objects = UserManager()

    @property
    def is_staff(self):
        return self.is_superuser

    def __str__(self):
        return self.username

    class Meta:
        ordering = ["-total_points", "username"]
        indexes = [models.Index(fields=["-total_points"])]


class Challenge(models.Model):
    CHALLENGE_TYPES = [
        ('connect', 'Connect'),
        ('understand', 'Understand'),
        ('act', 'Act'),
    ]

    # django has automatic primary key id field
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    challenge_type = models.CharField(max_length=10, choices=CHALLENGE_TYPES)
    points = models.PositiveIntegerField()
    total_completions = models.PositiveIntegerField(default=0)

    def __str__(self):
        # Format when printed: Challenge ID: Name (Challenge Type)
        return f"Challenge {self.id}: {self.name} ({self.challenge_type.capitalize()})"


class Friendship(models.Model):
    id = models.AutoField(primary_key=True)
    requester = models.ForeignKey(
        User, related_name="sent_requests", on_delete=models.CASCADE)
    receiver = models.ForeignKey(
        User, related_name="received_requests", on_delete=models.CASCADE)

    PENDING = "pending"
    ACCEPTED = "accepted"
    STATUS = [
        (PENDING, "Pending"),
        (ACCEPTED, "Accepted")
    ]
    status = models.CharField(
        max_length=10,
        choices=STATUS,
        default=PENDING
    )

    class Meta:
        # Ensure the combination of requester and receiver is unique
        constraints = [
            models.UniqueConstraint(
                fields=["requester", "receiver"], name="unique_friendship"
            )
        ]

    def clean(self):
        # Ensure no reverse friendships exist
        if Friendship.objects.filter(
            Q(requester=self.receiver, receiver=self.requester)
        ).exists():
            raise ValidationError("A reverse friendship already exists.")

            # Ensure requester and receiver are not the same
        if self.requester == self.receiver:
            raise ValidationError(
                "Requester and receiver cannot be the same user.")

    def __str__(self):
        return f"Friend request from {self.requester} to {self.receiver} ({self.status.capitalize()})"


class BingoGrid(models.Model):
    # A Bingo grid that references exactly 16 Challenge objects

    grid_id = models.AutoField(primary_key=True)

    # The sorted M2M field preserves order of challenges
    challenges = SortedManyToManyField(Challenge)

    is_active = models.BooleanField(default=False)

    def clean(self):
        # Ensure exactly 16 challenges
        # This only makes sense if the object is saved at least once (has a PK).
        # If it's brand new, you won't have the M2M relationships set until after save.
        if self.pk:
            if self.challenges.count() != 16:
                raise ValidationError(
                    f"BingoGrid must have exactly 16 challenges (found {
                        self.challenges.count()})."
                )

        # Ensure only one active BingoGrid
        if self.is_active:
            active_count = BingoGrid.objects.filter(
                is_active=True).exclude(pk=self.pk).count()
            if active_count > 0:
                raise ValidationError("Another BingoGrid is already active.")

    def __str__(self):
        return f"BingoGrid #{self.grid_id} (Active: {self.is_active})"


def file_size(value):
    limit = 5 * 1024 * 1024
    if value.size > limit:
        raise ValidationError(
            'Please upload an image with size less than 5MB.')


class TileInteraction(models.Model):
    # A model to represent a user's interaction with a challenge in a specific bingo grid.

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # The position of the tile/challenge in the bingo grid
    position = models.PositiveSmallIntegerField()
    # The bingo grid that this interaction concerns
    grid = models.ForeignKey(BingoGrid, on_delete=models.CASCADE)
    # Optional description field for users to add notes about their interaction
    description = models.TextField(max_length=500, blank=True)

    image = ResizedImageField(
        upload_to="",
        blank=True,
        keep_meta=False,
        validators=[file_size]
    )

    completed = models.BooleanField(default=False)
    consent = models.BooleanField(default=False)

    date_started = models.DateTimeField(auto_now_add=True)
    date_completed = models.DateTimeField(blank=True, null=True)

    class Meta:
        constraints = [
            # Position must be between 0-15
            models.CheckConstraint(
                condition=Q(position__lte=15),
                name='position_lte_15'
            ),
            # A user may not have more than 1 interaction with the same challenge in the same grid.
            models.UniqueConstraint(
                fields=['user', 'grid', 'position'], name='unique_user_grid_challenge')
        ]

    def get_image_html(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="100%" height="auto">')
        return None

    def __str__(self):
        return (f'Interaction of {self.user.username} with bingo grid '
                f'{self.grid.grid_id} - Challenge in position {self.position} - Completed: {self.completed}')
