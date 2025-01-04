from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager
from datetime import date
from django.db.models import Q
from django.core.exceptions import ValidationError


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
    indigenous_identity = models.BooleanField(
        choices=IndigenousIdentity,
        default=IndigenousIdentity.N
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


class ChallengeInteraction(models.Model):
    # Model to track an interaction between a user and a challenge.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)

    image = models.ImageField(
        upload_to="challenge_images/",  # idk where we want to put this atm
        blank=True
    )

    completed = models.BooleanField(default=False)
    consent = models.BooleanField(default=False)

    date_started = models.DateTimeField(auto_now_add=True)
    date_completed = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return (f"Interaction of {self.user.username} with challenge "
                f"'{self.challenge.name}' - Completed: {self.completed}")
