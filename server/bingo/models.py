from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager
from datetime import date
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.contrib.postgres.fields import ArrayField


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

    email = models.EmailField(
        max_length=320,
        unique=True,
        blank=False
    )
    EMAIL_FIELD = 'email'

    class Visibility(models.IntegerChoices):
        PUBLIC = (2, "Public")
        FRIENDS = (1, "Friends Only")
        BLUECREW = (0, "BlueCrew Only")
    visibility = models.IntegerField(
        choices=Visibility,
        blank=False,
        default=0
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
    #  A Bingo grid that holds an array of 16 challenge IDs.
    grid_id = models.AutoField(primary_key=True)
    # We store an array of integers (challenge IDs).
    challenges = ArrayField(
        base_field=models.IntegerField(),
        size=16,
        blank=True,
        default=list,
    )

    is_active = models.BooleanField(default=False)

    def clean(self):
        # Custom validation to ensure that at most one BingoGrid is active at a time.
        if self.is_active:
            active_count = BingoGrid.objects.filter(is_active=True).exclude(pk=self.pk).count()
            if active_count > 0:
                raise ValidationError("Another BingoGrid is already active.")
        super().clean()

    def __str__(self):
        return f"BingoGrid #{self.grid_id} (Active: {self.is_active})"
