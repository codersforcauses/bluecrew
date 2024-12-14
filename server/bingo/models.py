from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager
from datetime import date


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
        default=4
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
